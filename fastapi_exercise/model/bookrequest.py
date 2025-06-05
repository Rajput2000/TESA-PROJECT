from pydantic import BaseModel

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