from fastapi import FastAPI
from pydantic import BaseModel
import re


# Define a request model
class Input(BaseModel):
    account_number: str
    password: str



app = FastAPI()

books = [
    {"title": "Book 1", "author": "Author 1"},
    {"title": "Book 2", "author": "Author 2"},
    {"title": "Book 3", "author": "Author 3"},
    {"title": "Book 4", "author": "Author 4"},
    {"title": "Book 5", "author": "Author 5"},
    {"title": "Book 6", "author": "Author 6"},
    {"title": "Book 7", "author": "Author 7"},
    {"title": "Book 8", "author": "Author 8"},
    {"title": "Book 9", "author": "Author 9"},
    {"title": "Book 10", "author": "Author 10"},
]

def get_all_books():
    return books


def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_book_by_title(book_title):
    new_books = []
    for book in books:
        if book_title.lower() == book["title"].lower():
            new_books.append(book)
    return new_books


@app.get("/")
def read_root():
    return {"Python is the best programming language!"}


@app.get("/all-books")
def all_books():
    response = get_all_books()
    return response


@app.post("/get-book-by-name")
def book_by_name(request:dict):
    book_name = request["book_name"]
    response = get_book_by_title(book_name)
    return response


@app.post("/get-books-by-author")
def book_by_author(request:dict):
  author = request["author_name"]
  new_books = []
  for book in books:
      if author.lower() == book["author"].lower():
          new_books.append(book)
  return new_books

@app.post("/add-book")
def add_book(request:dict):
  title = request["book_name"]
  author = request["author_name"]
  for book in books:
    if (title.lower() == book["title"].lower()) and (author.lower() == book["author"].lower()):
      return "Book already exists"
        
  books.append({"title": title, "author": author})
  return {"reply":"New book added", "books": books}


@app.get("/get-prime-suffix")
def get_books_with_prime_suffix():
  new_books = []
  for book in books:
    title = book["title"]
    match = re.search(r"book\s*(\d+)", title, re.IGNORECASE)
    if match:
      number = int(match.group(1))
      
      if is_prime(number):
        new_books.append(book)

  return new_books

@app.post("/delete-by-name")
def delete_by_book_name(request:dict):
  index = 0
  title = request["book_name"]
  for book in books:
    if title.lower() == book["title"].lower():
      # print(book)
      del books[index]
    index += 1
  return books


# print(update_list({"book_name": "Book 3", "author_name": "Author 1"}))

