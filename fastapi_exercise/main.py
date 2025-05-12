from fastapi import FastAPI
from pydantic import BaseModel
import re
from datetime import datetime


# Define a request model
class BookFullRequest(BaseModel):
    """Model for complete book data including ID."""
    book_name: str
    author_name: str
    book_id: int

    def __getitem__(self, item):  # allow dict-style access
        return getattr(self, item)

class BookRequest(BaseModel):
    """Model for book data with name and author."""
    book_name: str
    author_name: str

    def __getitem__(self, item):  # allow dict-style access
        return getattr(self, item)

class BookNameRequest(BaseModel):
    """Model for requests using only book name."""
    book_name: str

    def __getitem__(self, item):
        return getattr(self, item)

class BookAuthorRequest(BaseModel):
    """Model for requests using only author name."""
    author_name: str

    def __getitem__(self, item):
        return getattr(self, item)


books = [
    {"id": 101, "title": "The Pragmatic Programmer 1", "author": "Andrew Hunt", "in_shelf": True, "times_borrowed": 5},
    {"id": 203, "title": "Clean Code 4", "author": "Robert C. Martin", "in_shelf": False, "times_borrowed": 12, "borrow_date": datetime(2025, 4, 1)},
    {"id": 283, "title": "Introduction to Algorithms 5", "author": "Thomas H. Cormen", "in_shelf": True, "times_borrowed": 7},
    {"id": 428, "title": "Design Patterns 6", "author": "Erich Gamma", "in_shelf": True, "times_borrowed": 4},
    {"id": 285, "title": "Python Crash Course 2", "author": "Eric Matthes", "in_shelf": False, "times_borrowed": 8, "borrow_date": datetime(2025, 4, 15)},
    {"id": 628, "title": "Data Science from Scratch 7", "author": "Joel Grus", "in_shelf": True, "times_borrowed": 3},
    {"id": 773, "title": "You Don't Know JS 3", "author": "Kyle Simpson", "in_shelf": True, "times_borrowed": 6},
    {"id": 838, "title": "Deep Learning 9", "author": "Ian Goodfellow", "in_shelf": True, "times_borrowed": 2},
    {"id": 937, "title": "Fluent Python 8", "author": "Luciano Ramalho", "in_shelf": True, "times_borrowed": 12},
    {"id": 100, "title": "Effective Java 10", "author": "Joshua Bloch", "in_shelf": False, "times_borrowed": 9, "borrow_date": datetime(2025, 4, 25)},
]


def get_all_books():
    """Return the list of all books."""
    return books


def is_prime(n):
    """Check if a number is prime."""
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
    """Retrieve books that match the given title (case-insensitive)."""
    new_books = []
    for book in books:
      if book_title.lower() == book["title"].lower():
        new_books.append(book)
    if len(new_books) == 0:
      return "Book not Found"
    return new_books
       

def pay_fine(present_book):
  """Calculate fine based on borrow duration.
    First 14 days are free. Thereafter, 500 units per day.
    """
  borrowing_limit = 14
  amount = 500
  now = datetime.now()

  borrowed_date = present_book["borrow_date"]   
  difference = now-borrowed_date
  day_difference =  abs(difference.days)

  if day_difference > borrowing_limit:
    fine = (day_difference - borrowing_limit) * amount

  else:
    fine = 0

  return fine 



app = FastAPI()


@app.get("/")
def read_root():
    return {"Python is the best programming language!"}


@app.get("/all-books")
def all_books():
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
  new_books = []
  for book in books:
      if author.lower() == book["author"].lower():
          new_books.append(book)
  if len(new_books) == 0:
      return "Book not Found"
  return new_books

@app.post("/add-book")
def add_book(request:BookFullRequest):
  """Add a new book if it doesn't already exist."""
  book_id = request["book_id"]
  title = request["book_name"]
  author = request["author_name"]

  for book in books:
    if (title.lower() == book["title"].lower()) and (author.lower() == book["author"].lower()):
      return "Book already exists"
        
  books.append({"id": book_id, "title": title, "author": author, "in_shelf": True, "times_borrowed": 0})
  return {"reply":"New book added", "books": books}


@app.get("/get-prime-suffix")
def get_books_with_prime_suffix():
  """Return books whose title ends with a prime number."""
  new_books = []
  for book in books:
    title = book["title"]
    match = re.search(r"\d+", title)
    if match:
      number = int(match.group())
      
      if is_prime(number):
        new_books.append(book)

  return new_books

@app.post("/delete-by-name")
def delete_book_by_name(request:BookNameRequest):
  """Delete a book using its title."""
  index = 0
  status = "Not found"
  title = request["book_name"]
  
  for book in books:
    if title.lower() == book["title"].lower():
      status = "Book Deleted"
      del books[index]
      
    index += 1
  return {"status": status, "books":books}

@app.post("/borrow-book-by-author")
def borrow_book_by_author(request:BookAuthorRequest):
  """Borrow a book using author's name."""
  author = request["author_name"]
  status = "Book Not Found"
  for book in books:
      if author.lower() == book["author"].lower():
        if book["in_shelf"] == True:
          book["in_shelf"] = False
          book["borrow_date"] = datetime.now()
          book["times_borrowed"] += 1
          status = "Book has been borrowed"
        else:
          status = "Book not in shelf"
        break

      else:
        status = "Book Not Found"

  return status

@app.post("/borrow-book-by-title")
def borrow_book_by_title(request:BookNameRequest):
  """Borrow a book using title."""
  title = request["book_name"]
  status = "Book Not Found"
  for book in books:
      if title.lower() == book["title"].lower():
        if book["in_shelf"] == True:
          book["in_shelf"] = False
          book["borrow_date"] = datetime.now()
          book["times_borrowed"] += 1
          status = "Book has been borrowed"
        else:
          status = "Book not in shelf"
        break

      else:
        status = "Book Not Found"

  return status


@app.post("/return-book-by-author")
def return_book_by_author(request:BookAuthorRequest):
  """Return a borrowed book by author."""
  author = request["author_name"]
  status = "Book Not Found"
  fine = 0
  for book in books:
      if author.lower() == book["author"].lower():
        if book["in_shelf"] == False:
          book["in_shelf"] = True
          fine = pay_fine(book)
          status = "Book has been Returned"
        else:
          status = "Book already in shelf"
        break

      else:
        status = "Book Not Found"

  return {"fine":fine, "status":status}

@app.post("/return-book-by-title")
def return_book_by_title(request:BookNameRequest):
  """Return a borrowed book by title."""
  title = request["book_name"]
  status = "Book Not Found"
  fine = 0
  for book in books:
      if title.lower() == book["title"].lower():
        if book["in_shelf"] == False:
          book["in_shelf"] = True
          fine = pay_fine(book)
          status = "Book has been Returned"
        else:
          status = "Book already in shelf"
        break

      else:
        status = "Book Not Found"
  
  return {"fine":fine, "status":status}


@app.get("/get-borrowed-books")
def get_borrowed_books():
  """Return books that are currently borrowed."""
  new_books = []
  for book in books:
    if book["in_shelf"] == False:
      new_books.append(book)

  return new_books

@app.get("/get-available-books")
def get_available_books():
  """Return books that are currently in shelf."""
  new_books = []
  for book in books:
    if book["in_shelf"] == True:
      new_books.append(book)
      
  return new_books

@app.get("/most-borrowed-book")
def most_borrowed_book():
  """Return book(s) that have been borrowed the most."""
  most_borrowed_book = books[0]
  for book in books[1:]:
    if book["times_borrowed"] > most_borrowed_book["times_borrowed"]:
      most_borrowed_book = book
  
  new_books = list(filter(lambda x: x["times_borrowed"] == most_borrowed_book["times_borrowed"], books))       
  return new_books


# print(borrow_book_by_author({"author_name":"Joel Grus"}))
# print(all_books())
# print("hello")