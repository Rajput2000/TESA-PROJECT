from fastapi import FastAPI
from model.bookrequest import *
from services.service import *


app = FastAPI()


@app.get("/")
def read_root():
    """home page"""
    return {"Python is the best programming language!"}


@app.get("/all-books")
def all_books():
    """Get all books"""
    response = get_all_books()
    return response


@app.post("/get-book-by-name")
def book_by_name(request:BookNameRequest):
    """Get all books by a specific title."""
    book_name = request["book_name"]
    response = get_book_by_title(book_name)
    return response


@app.post("/get-books-by-author")
def book_by_author(request:BookAuthorRequest):
  """Get all books by a specific author."""
  author = request["author_name"]
  response = get_book_by_author(author)

  return response


@app.post("/add-book")
def add_book(request:BookFullRequest):
  """Add a new book if it doesn't already exist."""
  book_id = request["book_id"]
  title = request["book_name"]
  author = request["author_name"]
  response = add_book(book_id, title, author)
  
  return response


@app.get("/get-prime-suffix")
def get_books_with_prime_suffix():
  """Return books whose title ends with a prime number."""
  response = get_books_with_prime_suffix()
  
  return response


@app.post("/delete-by-name")
def delete_book_by_name(request:BookNameRequest):
  """delete book by title"""
  title = request["book_name"]
  response = delete_book_by_name(title)
  
  return response


@app.post("/borrow-book-by-author")
def borrow_book_by_author(request:BookAuthorRequest):
  """borrow by book author"""
  author = request["author_name"]
  response = borrow_book_by_author(author)

  return response


@app.post("/borrow-book-by-title")
def borrow_book_by_title(request:BookNameRequest):
  """Borrow a book using title."""
  title = request["book_name"]
  response = borrow_book_by_title(title)

  return response


@app.post("/return-book-by-author")
def return_book_by_author(request:BookAuthorRequest):
  """Return a borrowed book by author."""
  author = request["author_name"]
  response = return_book_by_author(author)

  return response


@app.post("/return-book-by-title")
def return_book_by_title(request:BookNameRequest):
  """Return a borrowed book by title."""
  title = request["book_name"]
  response = return_book_by_title(title)

  return response


@app.get("/get-borrowed-books")
def get_borrowed_books():
  """Return books that are currently borrowed."""
  response = get_borrowed_books()

  return response


@app.get("/get-available-books")
def get_available_books():
  """Return books that are currently in shelf."""
  response = get_available_books()
  
  return response


@app.get("/most-borrowed-book")
def most_borrowed_book():
  """Return book(s) that have been borrowed the most."""
  response = most_borrowed_book()

  return response