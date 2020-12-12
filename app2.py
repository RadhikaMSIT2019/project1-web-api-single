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
import os
import csv
import time
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
# from models import *
import requests
import json
from flask.json import jsonify
active = 'active'
data = []
app = Flask(__name__)
if __name__ == '__main__':
    app.run()
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
# db = scoped_session(sessionmaker(bind=engine))
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
def index2():
    return redirect(url_for('home'))


@app.route("/home")
def home():
    if 'email' in session:
        return render_template('index.html', email=session['email'])
    return render_template('base.html', email=None)


@app.route("/base")
def base():
    return render_template('base.html')


@app.route("/index")
def index():
    if 'email' in session:
        return render_template('index.html', email=session['email'])
    else:
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

#
# @app.route("/registration", methods=["POST"])
# def registration():
#     rfname = request.form.get("first_name")
#     rlname = request.form.get("last_name")
#     remail = request.form.get("email")
#     rpassword = request.form.get("password")
#     rcpassword = request.form.get("confirm_password")
#
#     if "login" in request.form:
#         try:
#             print('in login')
#             db = scoped_session(sessionmaker(bind=engine))
#             query = db.query(Users).filter(Users.email == remail)
#             name = query.first()
#             # print(name.email)
#             if name is not None and name.email == remail and name.pwrd == rpassword:
#                 print('session created in login')
#                 session['email'] = name.email
#                 EmailAccess = name.email
#                 Fname = name.fname
#                 print("EmailAccess =", EmailAccess, "Fname =", Fname)
#                 session['fname'] = name.fname
#                 user = name.email
#
#                 query = db.query(Admin).filter(Admin.email == remail)
#                 name = query.first()
#
#                 if name is not None:
#                     return redirect(url_for('main', email=user))
#
#                 # return render_template('search.html', email=user)
#                 return render_template('search.html', email=user, fname=session['fname'])
#             elif name is not None and name.email == remail and name.pwrd != rpassword:
#                 print('Incorrect password, try again')
#                 # session['email'] = name.email
#                 flash('Incorrect password, try again')
#                 # s = session['email']
#                 # return render_template('register.html', email=None)
#                 return  redirect(url_for('register'))
#             else:
#                 print('User not registered,register before you login')
#                 flash('User not registered,register before you login')
#                 return redirect(url_for('register'))
#
#         except SQLAlchemyError as e:
#             print(e)
#             return render_template('fail.html', path='./static/css/style.css')
#         finally:
#             db.close()
#     else:
#         print("in register method")
#         if rpassword == rcpassword:
#             # data = {'a': 5566, 'b': 9527, 'c': 183}
#             try:
#                 db = scoped_session(sessionmaker(bind=engine))
#                 query = db.query(Users).filter(Users.email == remail)
#                 print(remail)
#                 if query.first() != None:
#                     print('User already exists')
#                     flash('User already exists')
#                     return render_template('register.html', email=None)
#                 else:
#                     print('Inserting user')
#                     now = datetime.now()
#                     db = scoped_session(sessionmaker(bind=engine))
#                     row = Users(email=remail, fname=rfname,
#                                 lname=rlname, pwrd=rpassword, date=now)
#                     db.add(row)
#                     db.commit()
#                     # flash('USer successfully registered into DataBase')
#                     # return render_template('register.html', email=None)
#                     return render_template('index.html', email=None)
#
#             except SQLAlchemyError as e:
#                 print(e)
#                 return render_template('fail.html', path='./static/css/style.css')
#             finally:
#                 db.close()
#                 # return render_template('success.html',path='./static/css/styles.min.css')
#         else:
#             print("confirmation does not match")
#             flash(
#                 'confirmation password does not match with the Entered password, Try again')
#             # return render_template('register.html')
#             return redirect(url_for('register'))


@ app.route("/registration", methods=["POST"])
# rfname = request.form.get("first_name")
#     rlname = request.form.get("last_name")
#     remail = request.form.get("email")
#     rpassword = request.form.get("password")
#     rcpassword = request.form.get("confirm_password")
def registration():
    if 'fname' not in session:
        rowName = ['fname', 'lname', 'email',
                   'pwrd', 'date']

        # email = Column(String, primary_key=True, nullable=False)
    # fname = Column(String)
    # lname = Column(String)
    # pwrd = Column(String)
    # date = Column(DateTime)
        row = []
        for i in rowName:
            s = request.form.get(i)
            row.append(s)
            print(s)
        Uname = db.query(Users).filter_by(fname=row[1]).first()
        email = db.query(Users).filter_by(email=row[2]).first()
        if(Uname != None and Uname.fname == row[1]):
            flash('username already exist,please login', 'warning')
            return redirect(url_for('index'))
        elif(email != None and email.email == row[2]):
            flash('Email already exist,please login', 'warning')
            return redirect(url_for('index'))

        user = Users(fname=row[0], lname=row[1], email=row[2],
                    pwd=row[3], date=time.ctime(time.time()))
        try:
            db.add(user)
            db.commit()
            flash(f"HI {row[0]} account created sucessfully", 'success')
        except:
            # e = sys.exc_info()
            # print(e)
            flash("error occured", 'danger')
        finally:
            db.remove()
            db.close()
        return render_template('register.html', register=active)

    flash("user already exist", 'warning')
    return redirect(url_for('index'))


@ app.route("/logout")
def logout():
    session.pop('Username', None)
    return redirect(url_for('index'))


@ app.route("/loginNow", methods=["POST"])
def loginNow():
    rowName = ['email', 'pwrd']
    row = []
    for i in rowName:
        s = request.form.get(i)
        # print(s)
        if(s == ''):
            flash("please fill all details", 'warning')
            return render_template('login.html',login=active)
        else:
            row.append(s)
    row.append(request.form.get('check'))
    # print(row)
    Username = db.query(Users).filter_by(email=row[0]).first()
    # print(Uname)
    # print(Uname.Password)
    # print(row[1])
    # print(Uname.Password == row[1])
    if(Username != None and Username.Password == row[1]):
        flash("login success", "success")
        session[rowName[0]] = row[0]
        return redirect(url_for('userHome', user=row[0]))
    else:
        flash("account does not exist register now", "danger")
        return redirect(url_for('register'))


@app.route("/api/search/", methods=["POST"])
def search_api():

    if request.method == "POST":
        var = request.json

        res = var["search"]
        res = "%" + res + "%"

        result = db.query(Books).filter(or_(Books.title.ilike(res), Books.author.ilike(res), Books.isbn.ilike(res))
                                        ).all()

        if result is None:
            return jsonify({"error": "Book not found"}), 400

        book_ISBN = []
        book_TITLE = []
        book_AUTHOR = []
        book_YEAR = []

        for eachresult in result:
            book_ISBN.append(eachresult.isbn)
            book_TITLE.append(eachresult.title)
            book_AUTHOR.append(eachresult.author)
            book_YEAR.append(eachresult.year)

        dict = {
            "isbn": book_ISBN,
            "title": book_TITLE,
            "author": book_AUTHOR,
            "year": book_YEAR,
        }
        print("returning")
        print(dict)
        return jsonify(dict), 200
    return "<h1>Come again</h1>"


@app.route("/api/book/", methods=["POST"])
def book_api():

    if request.method == "POST":
        var = request.json
        res = var["isbn"]
        isbn = res

        book = db.query(Books).filter_by(isbn=isbn).first()
        res = requests.get(
            "https://www.goodreads.com/book/review_counts.json",
            params={"key": "2VIV9mRWiAq0OuKcOPiA", "isbns": isbn},
        )

        # Parsing the data
        data = res.text
        parsed = json.loads(data)
        print(parsed)
        res = {}
        for i in parsed:
            for j in parsed[i]:
                res = j

        allreviews = db.query(Reviews).filter_by(isbn=isbn).all()
        rew = []
        time = []
        usr = []
        for rev in allreviews:
            rew.append(rev.review)
            time.append(rev.time_stamp)
            usr.append(rev.username)

        if book is None:
            return jsonify({"error": "Book not found"}), 400

        dict = {
            "isbn": isbn,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "average_rating": res["average_rating"],
            "average_reviewcount": res["reviews_count"],
            "review": rew,
            "time_stamp": time,
            "username": usr,
        }
        return jsonify(dict), 200


@app.route("/api/submit_review/", methods=["POST"])
def review_api():
    if request.method == "POST":

        var = request.json
        # print("-------------------", var)
        isbn = var["isbn"]
        username = var["username"]
        rating = var["rating"]
        reviews = var["reviews"]
        print(isbn, username, rating, reviews)

        # id = Column(Integer, primary_key=True, autoincrement=True)
        # review = Column(String)
        # rating = Column(String)
        # fname = Column(String)
        # date = Column(DateTime)
        # email = Column(String, ForeignKey('USERS.email'))
        # isbn = Column(String, ForeignKey('BOOKS.isbn'))

        # check if the paticular user given review before
        rev_From_db = db.query(Reviews).filter(
            Reviews.isbn.like(isbn), Reviews.username.like(username)
        ).first()
        print("first", str(rev_From_db))

        # if the user doesnt give the review for that book
        if rev_From_db is None:

            try:
                # bring the book details
                book = Books.query.filter_by(isbn=isbn).first()
                print("book", str(book))
            except:
                message = "Enter valid ISBN"
                return jsonify(message), 404

            timestamp = time.ctime(time.time())
            title = book.title
            user = Reviews(
                isbn=isbn,
                review=reviews,
                rating=rating,
                time_stamp=timestamp,
                title=title,
                username=username,
            )
            db.session.add(user)
            db.session.commit()

            allreviews = db.query(Reviews).filter_by(isbn=isbn).all()
            rew = []
            timeStamp = []
            usr = []
            for rev in allreviews:
                rew.append(rev.review)
                timeStamp.append(rev.time_stamp)
                usr.append(rev.username)

            dict = {
                "isbn": isbn,
                "review": rew,
                "time_stamp": timeStamp,
                "username": usr,
                "message": "You reviewed this book.",
            }

            return jsonify(dict), 200
        else:
            dict = {"message": "You already reviewed this book."}
            return jsonify(dict), 200