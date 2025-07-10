import re
import numpy as np
import pandas as pd


class Library():
  def __init__(self) -> None:
    self.book_path = "Chat_Bot/library/Futminna_Library.xlsx"
    self.books =  pd.read_excel(self.book_path, sheet_name="Books")


  def search_book(self, title=None, author=None, section=None, subsection=None):
    """
    Search for books by title, author, section, or any combination of these parameters.
    
    Args:
        title (str, optional): Book title to search for (case-insensitive)
        author (str, optional): Author name to search for (case-insensitive)
        section (str, optional): Section name to search for (case-insensitive)
        subsection (str, optional): Subsection name to search for (case-insensitive)

    Returns:
        list: List of dictionaries containing book information, or empty list if no matches
        If no parameters provided, returns all unique sections
    """
    # If no parameters provided, return all unique sections
    if not any([title, author, section, subsection]):
        return {"Sections": self.books['Section'].unique().tolist()}

    # Start with all books
    filtered_books = self.books.copy()

    # Apply filters based on provided parameters
    if title:
        filtered_books = filtered_books[
            filtered_books['Title'].str.lower().str.contains(title.lower(), na=False)
        ]
    
    if author:
        filtered_books = filtered_books[
            filtered_books['Author'].str.lower().str.contains(author.lower(), na=False)
        ]
    
    if section:
        filtered_books = filtered_books[
            filtered_books['Section'].str.lower().str.contains(section.lower(), na=False)
        ]

    if subsection:
        filtered_books = filtered_books[
            filtered_books['Subsection'].str.lower().str.contains(subsection.lower(), na=False)
        ]

    # Return results as list of dictionaries
    if not filtered_books.empty:
        return filtered_books[['Title', 'Author', 'Section', 'Subsection']].to_dict(orient='records')
    else:
        return []
  
  
  def is_book_in_shelf(self, title: str, author: str):
    """
    Check if a book with the given title and author is currently in shelf.
    
    Args:
        title (str): Title of the book.
        author (str): Author of the book.
        
    Returns:
        bool: True if the book is in shelf, False otherwise.
    """
    result = self.books[
        (self.books['Title'].str.lower() == title.lower()) &
        (self.books['Author'].str.lower() == author.lower())
    ]
    if not result.empty:
        return {"response": bool(result.iloc[0]['Inshelf'])}
    return {"response": False}
  

  def borrow_book(self, title: str, author: str, user: str):
    """
    Checks if the book is available and performs a borrow operation.
    
    - title: Title of the book
    - author: Author of the book
    - user: Username of the person borrowing
    """
    
    # Step 1: Check availability
    availability = self.is_book_in_shelf(title, author)

    if not isinstance(availability, dict) or not availability.get("response", False):
        return {"success": False, "message": "Book is not available in the shelf."}

    # Step 2: Find matching book in the DataFrame (case-insensitive)
    mask = (
        self.books["Title"].str.lower() == title.lower()
    ) & (
        self.books["Author"].str.lower() == author.lower()
    ) & (
        self.books["Inshelf"] == True
    )

    if not mask.any():
        return {"success": False, "message": "No available copy of the book found."}

    # Step 3: Update the first matching row
    index = self.books[mask].index[0]
    self.books.at[index, "Inshelf"] = False
    self.books.at[index, "Borrower"] = user

    borrowed_book = self.books.loc[index].to_dict()
    self.books.to_excel(self.book_path, index=False, sheet_name="Books")

    return {
        "success": True,
        "message": "Book borrowed successfully.",
        "book": borrowed_book
    }


  def return_book(self, title: str, author: str, user: str):
    """
    Allows a user to return a book if they were the one who borrowed it.

    - title: Title of the book
    - author: Author of the book
    - user: Username of the person returning
    """
    # Step 1: Find matching borrowed book by same user (case-insensitive)
    mask = (
        (self.books["Title"].str.lower() == title.lower()) &
        (self.books["Author"].str.lower() == author.lower()) &
        (self.books["Inshelf"] == False) &
        (self.books["Borrower"].str.lower() == user.lower())
    )

    if not mask.any():
        return {
            "success": False,
            "message": "Either the book wasn't borrowed, or you are not the borrower."
        }

    # Step 2: Mark the book as returned
    index = self.books[mask].index[0]
    self.books.at[index, "Inshelf"] = True
    self.books.at[index, "Borrower"] = ""

    returned_book = self.books.loc[index].to_dict()
    self.books.to_excel(self.book_path, index=False, sheet_name="Books")

    return {
        "success": True,
        "message": "Book returned successfully.",
        "book": returned_book
    }

