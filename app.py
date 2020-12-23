import os
import sys
import requests
import json

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from datetime import datetime, time

from sqlalchemy import *  # create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *  # scoped_session, sessionmaker
from werkzeug.debug import DebuggedApplication


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")
app.config["SESSION_TYPE"] = "filesystem"
app.config['development'] = True
app.config['SECRET_KEY'] = '#RR#'
Session(app)
user = ""
EmailAccess = ""
Fname = ""
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# engine = create_engine("postgres://uvzriayrtbengf:003c06b304340ce57dd5f14d97b848b8dcf07ba3c68e7ce9f9144e748dab07de@ec2-54-152-40-168.compute-1.amazonaws.com:5432/d5oa914l0lfkcv")
db = scoped_session(sessionmaker(bind=engine))
print(engine.table_names(), file=sys.stdout)
# db=SQLAlchemy(app)

Base = declarative_base()



class Users(Base):
    __tablename__ = "USERS"
    email = Column(String, primary_key=True, nullable=False)
    fname = Column(String)
    lname = Column(String)
    pwrd = Column(String)
    date = Column(DateTime)


class Books(Base):
    __tablename__ = "BOOKS"
    isbn = Column(String, primary_key=True, nullable=False)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)


class Admin(Base):
    __tablename__ = "ADMIN"
    email = Column(String, primary_key=True, nullable=False)
    admin = Column(Boolean)


class Reviews(Base):
    __tablename__ = 'REVIEWS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    review = Column(String)
    rating = Column(String)
    fname = Column(String)
    date = Column(DateTime)
    email = Column(String, ForeignKey('USERS.email'))
    isbn = Column(String, ForeignKey('BOOKS.isbn'))


@app.route("/")
def index():
    return render_template('index.html', email=None)


@app.route("/home")
def home():
    if 'email' in session:
        return render_template('index.html', email=session['email'])
    return render_template('base.html', email=None)


@app.route("/register")
def register():
    # If table don't exist, Create.
    if not engine.dialect.has_table(engine, "USERS"):
        # db_engine = connect_db()
        # path='./static/css/style.css'
        Users.__table__.create(bind=engine, checkfirst=True)

    if not engine.dialect.has_table(engine, "ADMIN"):
        Admin.__table__.create(bind=engine, checkfirst=True)

    if "email" in session:
        print("session present while registrering")
        return render_template('register.html', email=session['email'])
    return render_template('register.html', email=None)


@app.route("/registration", methods=["POST"])
def registration():
    rfname = request.form.get("first_name")
    rlname = request.form.get("last_name")
    remail = request.form.get("email")
    rpassword = request.form.get("password")
    rcpassword = request.form.get("confirm_password")

    if "login" in request.form:
        try:
            print('in login')
            db = scoped_session(sessionmaker(bind=engine))
            query = db.query(Users).filter(Users.email == remail)
            name = query.first()
            # print(name.email)
            if name is not None and name.email == remail and name.pwrd == rpassword:
                print('session created')
                session['email'] = name.email
                EmailAccess = name.email
                Fname = name.fname
                print("EmailAccess =", EmailAccess, "Fname =", Fname)
                session['fname'] = name.fname
                user = name.email
                query = db.query(Admin).filter(Admin.email == remail)
                name = query.first()

                if name is not None:
                    return redirect(url_for('main', email=user))

                return render_template('search.html', email=user, fname=session['fname'])
            elif name is not None and name.email == remail and name.pwrd != rpassword:
                print('Incorrect password, try again')
                # session['email'] = name.email
                flash('Incorrect password, try again')
                # s = session['email']
                return redirect(url_for('register'))
            else:
                print('User not registered,register before you login')
                flash('User not registered,register before you login')
                # return redirect(url_for('register'))
                return redirect(url_for('register'))
        except SQLAlchemyError as e:
            print(e)
            return render_template('fail.html', path='./static/css/style.css')
        finally:
            db.close()
    else:
        print("in register method")
        if rpassword == rcpassword:
            # data = {'a': 5566, 'b': 9527, 'c': 183}
            try:
                db = scoped_session(sessionmaker(bind=engine))
                query = db.query(Users).filter(Users.email == remail)
                print(remail)
                if query.first() != None:
                    print('User already exists')
                    flash('User already exists')
                    return redirect(url_for('register'))
                else:
                    print('Inserting user')
                    now = datetime.now()
                    db = scoped_session(sessionmaker(bind=engine))
                    row = Users(email=remail, fname=rfname, lname=rlname, pwrd=rpassword, date=now)
                    db.add(row)
                    db.commit()
                    return render_template('index.html', email=None)

            except SQLAlchemyError as e:
                print(e)
                return render_template('fail.html', path='./static/css/style.css')
            finally:
                db.close()
                # return render_template('success.html',path='./static/css/styles.min.css')
        else:
            print("confirmation does not match")
            flash('confirmation password does not match with the Entered password, Try again')
            return redirect(url_for('register'))


@app.route("/api/searchapi/<string:search>/", methods=["POST", "GET"])
def searchapi(search):
    try:
        db = scoped_session(sessionmaker(bind=engine))
        search = '%' + search + '%'
        query = db.query(Books).filter(
            or_(Books.isbn.ilike(search), Books.title.ilike(search), Books.author.ilike(search)))
        if query != None:
            row = query.all()
            html = content(row)
        else:
            html = '<p>No Results found for the entered getails</p>'
        html = json.dumps({'content': html})
        return html, 200
    except SQLAlchemyError as e:
        print(e)
        return '<p>No Results found for the entered details</p>', 400
    finally:
        db.close()

def content(row):
    html = '''<table class="table">
      <thead class="thead-dark">
        <tr>
          <th scope="col">ISBN</th>
          <th scope="col">Title</th>
        </tr>
      </thead>
      <tbody>'''
    for r in row:
        print(type(r.isbn))
        html += '''<tr>
          <td><a onclick="bookdetails(''' + str(r.isbn) + ''')">''' + str(r.isbn) + '''</a></td>

          <td><a onclick="bookdetails(''' + str(r.isbn) + ''')">''' + str(r.title) + '''</a></td>
        </tr>'''

    html += '''</tbody>
    </table>
    </div>'''

    return html




@app.route("/bookApi")
def bookApi():
    pass




@app.route("/reviewApi")
def reviewApi():
    pass



@app.route("/searchtest", methods=["POST", "GET"])
def searchtest():
    if 'email' in session:
        return render_template('search.html', email=session['email'],fname=session['fname'])
    return render_template('index.html', email=None)

@app.route("/api/booksapi/<string:isbn>/", methods=["POST", "GET"])
def booksearch(isbn):
    db = scoped_session(sessionmaker(bind=engine))
    if 'email' in session:
        print('length of isbn', len(isbn))
        if len(isbn)<10:
            isbn = "0" + isbn
            # booksearch(isbn)
        print("isbn = ", isbn)

        html = ''
        try:
            if not engine.dialect.has_table(engine, "REVIEWS"):  # If table don't exist, Create.
                Reviews.__table__.create(bind=engine, checkfirst=True)
            # query = db.query(Books).filter(Books.isbn==isbn)
            query = db.query(Books).filter(Books.isbn == isbn)
            if query != None:
                # r = query.all()
                # print(r)
                # for book in r:
                #     print(f"added{book.title} with number {book.isbn} written by {book.author} published in the year {book.year}")
                booksquery = db.query(Reviews).filter(Reviews.isbn == isbn)
                print(booksquery)
                res = requests.get("https://www.goodreads.com/book/review_counts.json",
                                   params={"key": "aLvwXAjKk7bi8mYKzi0mw", "isbns": isbn})
                data = res.text
                print(data)

                # parsed = res.json()
                # print(parsed)
                res = {}
                if data != 'No books match those ISBNs.':
                    parsed = json.loads(data)
                    print(parsed)
                    for i in parsed:
                        for j in (parsed[i]):
                            res = j
                else:
                    res['isbn'] = "_"
                    res["average_rating"] = "_"
                    res["reviews_count"] = "_"

                print('res :')
                print(res)
                book = query.first()


                html = '''
                       <div class="container-fluid">
                       <div class="container">
                       <div class="row">
                       <div class="col-md">
                       <center>
                       <img src="http://covers.openlibrary.org/b/isbn/''' + str(isbn) + '''-L.jpg" class="img-fluid" alt="Responsive image">
                       </center>
                       </div>
                       </div>
                       <div class="row">
                       <div class="col-md">
                       <center>
                       <h1 class="text-uppercase">''' + str(book.title) + '''</h1>
                       </center>
                       </div>
                       </div>
                       <div class="row">
                       <div class="col-sm">
                       <b>ISBN</b>
                       </div>
                       <div class="col-sm">
                       <b>Author</b>
                       </div>
                       <div class="col-sm">
                       <b>Rating</b>
                       </div>
                       <div class="col-sm">
                       <b>Year Published</b>
                       </div>
                       <div class="col-sm">
                       <b>Review Count</b>
                       </div>
                       </div>
                       <div class="row">
                       <div class="col-sm">''' + str(res["isbn"]) + '''
                       </div>
                       <div class="col-sm">''' + str(book.author) + '''
                       </div>
                       <div class="col-sm">''' + str(res["average_rating"]) + '''</div>
                       <div class="col-sm">''' + str(book.year) + '''
                       </div>
                       <div class="col-sm">''' + str(res["reviews_count"]) + '''
                       </div>
                       </div>
                       </div>
                       <hr>
                       <center>
                       <div class="w-50 p-3">
                       <h2>Reviews</h2>
                       <p class="hint-text">Review the book</p>
                       <div class="form-check form-check-inline">
                       <input type="radio" id="star5" name="rating" value="5 Stars" class="form-check-input" />
                       <label for="star5" class="form-check-label" title="text">5 stars</label>
                       </div>
                       <div class="form-check form-check-inline">
                       <input type="radio" id="star4" name="rating" value="4 Stars" class="form-check-input" />
                       <label for="star4" class="form-check-label" title="text">4 stars</label>
                       </div>
                       <div class="form-check form-check-inline">
                       <input type="radio" id="star3" name="rating" value="3 Stars" class="form-check-input" />
                       <label for="star3" class="form-check-label" title="text">3 stars</label>
                       </div>
                       <div class="form-check form-check-inline">
                       <input type="radio" id="star2" name="rating" value="2 Stars" class="form-check-input" />
                       <label for="star2" class="form-check-label" title="text">2 stars</label>
                       </div>
                       <div class="form-check form-check-inline">
                       <input type="radio" id="star1" name="rating" value="1 Star" class="form-check-input" />
                       <label for="star1" class="form-check-label" title="text">1 star</label>
                       </div>
                       <div class="form-group">
                       <textarea id="Review" name="review" placeholder="Write your review.." class="form-control"></textarea>
                       </div>
                       <div class="form-group">
                       <button type="submit" class="btn btn-success btn-lg btn-block" name="login" value="login" id="Reviewbtn" onclick="review(''' + str(
                    isbn) + ''')">submit</button>
                       </div>
                       </div>
                       </center>'''
                if booksquery != None:
                    review = booksquery.all()
                    if review != None:
                        for i in review:
                            html += ''' <div style="background:#faf3dd" class="jumbotron jumbotron-fluid .bg-gradient-primary">
                                   <div class="container .bg-gradient-primary">
                                   <h1 class="display-8"><b>''' + str(i.fname) + '''</b></h1>
                                   <p class="lead">''' + str(i.date) + '''<br>
                                   ''' + str(i.review) + '''</p>
                                   </div>
                                   </div>
                                   </div>'''

                    else:
                        html = "<p>there are no books available for this book</p>"
                print('returning html')
                html = json.dumps({'content': html})
                return html, 200

        except SQLAlchemyError as e:
            print(e)
            return '<p>No Results found for the selected book</p>', 400
        except Exception as e:
            print(e)
        finally:
            db.close()
        # print('html :',html)
        # return html,200
    else:
        return render_template('index.html', email=None)


@app.route("/api/reviewsapi/<string:isbn>/<string:review>/<string:rating>/<string:email>/<string:fname>/",
           methods=["GET", "POST"])
def review(isbn, review, rating, email, fname):
    # print('review length of isbn', len(isbn))
    # while len(isbn) < 10:
    #     isbn = "0" + isbn
    # print("review isbn = ", isbn)
    #
    # print(isbn, review, rating, email, fname);
    # print("inside review")
    # print(email)
    # now = datetime.now()
    # print(fname)
    print("inside review")
    print(email)
    now = datetime.now()
    print(fname)

    print('review length of isbn', len(isbn))
    while len(isbn) < 10:
        isbn = "0" + isbn
    print("review isbn = ", isbn)

    try:
        db = scoped_session(sessionmaker(bind=engine))
        query = db.query(Reviews).filter(Reviews.email == email)
        html = ""

        if query != None:
            rbooks = []
            for r in query.all():
                rbooks.append(r.isbn)
            # bquery = book_query(isbn,author,title)
            if isbn not in rbooks:
                # query = db.query(Users).filter(Users.email==email)
                row = Reviews(email=email, fname=fname, review=review, date=now, isbn=isbn, rating=rating)
                db.add(row)
                db.commit()
                html = '<center><p class="fs-1">Review Submitted</p></center>'
            else:
                html = '<center><p class="fs-1">You already reviewed the book, try to review another book</p></center>'
        else:
            row = Reviews(email=email, fname=fname, review=review, date=now, isbn=isbn, rating=rating)
            db.add(row)
            db.commit()
            html = '<center><p class="fs-1">Review Submitted</p></center>'

        print("html=",html)
        html = json.dumps({'content': html})
        return html, 200
    except SQLAlchemyError as e:
        print(e)
        return render_template('fail.html', path='./static/css/style.css')
    finally:
        db.close()


def book_query(isbn):
    try:
        db = scoped_session(sessionmaker(bind=engine))
        bquery = db.query(Books).filter(Books.isbn == isbn)

    except SQLAlchemyError as e:
        print(e)
        return render_template('fail.html', path='./static/css/style.css')
    finally:
        db.close()

    return bquery.first()




@app.route("/login", methods=["POST"])
def login():
    return render_template('login.html', path='./static/css/style.css')


@app.route("/login_form")
def login_form():
    session.clear()
    session.pop('email', None)
    return render_template('index.html', path='./static/css/style.css', email=None)


@app.route("/main")
def main():
    if 'email' in session:
        try:
            db = scoped_session(sessionmaker(bind=engine))
            query = db.query(Users).order_by(Users.date)
            return render_template('main.html', row=query.all())
        except SQLAlchemyError as e:
            print(e)
            return render_template('fail.html', path='./static/css/style.css')
        finally:
            db.close()
    else:
        return render_template('index.html', email=None)






if __name__ == "__main__":
    # app.secret_key = "#RR#"
    app.run(debug=True)
    # Session(app)
