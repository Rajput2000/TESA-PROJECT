import re
from datetime import datetime

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


def get_book_by_author(author):
  """Get all books by a specific author."""
  new_books = []
  for book in books:
      if author.lower() == book["author"].lower():
          new_books.append(book)
  if len(new_books) == 0:
      return "Book not Found"
  return new_books


def add_book(book_id, title, author):
  """Add a new book if it doesn't already exist."""
  for book in books:
    if (title.lower() == book["title"].lower()) and (author.lower() == book["author"].lower()):
      return "Book already exists"
        
  books.append({"id": book_id, "title": title, "author": author, "in_shelf": True, "times_borrowed": 0})
  return {"reply":"New book added", "books": books}


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


def delete_book_by_name(title):
  """Delete a book using its title."""
  index = 0
  status = "Not found"
  
  for book in books:
    if title.lower() == book["title"].lower():
      status = "Book Deleted"
      del books[index]
      
    index += 1
  return {"status": status, "books":books}


def borrow_book_by_author(author):
  """Borrow a book using author's name."""
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


def borrow_book_by_title(title):
  """Borrow a book using title."""
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


def return_book_by_author(author):
  """Return a borrowed book by author."""
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


def return_book_by_title(title):
  """Return a borrowed book by title."""
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


def get_borrowed_books():
  """Return books that are currently borrowed."""
  new_books = []
  for book in books:
    if book["in_shelf"] == False:
      new_books.append(book)

  return new_books


def get_available_books():
  """Return books that are currently in shelf."""
  new_books = []
  for book in books:
    if book["in_shelf"] == True:
      new_books.append(book)
      
  return new_books


def most_borrowed_book():
  """Return book(s) that have been borrowed the most."""
  most_borrowed_book = books[0]
  for book in books[1:]:
    if book["times_borrowed"] > most_borrowed_book["times_borrowed"]:
      most_borrowed_book = book
  
  new_books = list(filter(lambda x: x["times_borrowed"] == most_borrowed_book["times_borrowed"], books))       
  return new_books
