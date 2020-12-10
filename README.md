# Project 1-WEB_API
"import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": "0590554107"})
print(res.json())

key: iNR9v978MfG0fz9pCcaFQ
secret: JSaSytSB9xQn76bFQN7v4YqPTfTHO7ZWRUbfNZzY"

Web Programming with Python Flask SqlAlchemy and  JavaScript 

Web API for Search and Book Details


Add three new routes to your application.py /api/search, /api/book and /api/submit_review
Use the search, book details page, and submit review functions developed in the previous task to return the results for the /api requests in the JSON format. A good practice is to send relevant response codes, i.e., if the search query is successful you could send 200 and in case of any exception or errors send 400 or 500 as applicable, i.e., 400 if the book is not found and 500 if there is an unexpected failure such as database connection issues.
Update the test_application.py to add tests for the /api/search and /api/book and verify if the HTTP requests are working as expected.
Use postman (https://www.postman.com/product/api-client) to test if the web APIs.

Single Page and Implementation

Task 1 - Single page user home
Edit the user home jinja template such it displays only the book search user interface
Setup the route for the userhome so that it renders this new template
Task 2 - Display search results
Write a javascript function to make a AJAX call to /api/search
Parse the JSON returned by the API to display the books that match the search result
Update the DOM to display the book search results
Task 3 - Display book details
Write a javascript function to make a AJAX call to /api/book_details
Parse the JSON returned by the API to display the book details
Update the DOM to display the book details
Task 4 - Submit book review
Write a javascript function to make a AJAX call to /api/submit_review
Parse the JSON returned by the API to display the book details
Update the DOM to display the book details