# Function definition for Gemini API
search_book_function = {
    "name": "search_book",
    "description": "Search for books by title, author, section, or any combination of these parameters. Supports partial matching.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Book title to search for (partial matching supported, case-insensitive)"
            },
            "author": {
                "type": "string",
                "description": "Author name to search for (partial matching supported, case-insensitive)"
            },
            "section": {
                "type": "string",
                "description": "Section name to search for (partial matching supported, case-insensitive)"
            },
            "subsection": {
                "type": "string",
                "description": "Subsection name to search for (partial matching supported, case-insensitive)"
            }
            
        },
        "required": []
    }
}

is_book_in_shelf_function = {
    "name": "is_book_in_shelf",
    "description": "Check if a specific book (by title and author) is currently available in the shelf.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The exact title of the book to check"
            },
            "author": {
                "type": "string",
                "description": "The exact author name of the book to check"
            }
        },
        "required": ["title", "author"]
    }
}

borrow_book_function = {
    "name": "borrow_book",
    "description": "Borrow a book from the library by providing the exact title and author. Requires the user's name.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The exact title of the book to borrow"
            },
            "author": {
                "type": "string",
                "description": "The exact author of the book to borrow"
            },
            "user": {
                "type": "string",
                "description": "The name of the person borrowing the book"
            }
        },
        "required": ["title", "author", "user"]
    }
}
return_book_function = {
    "name": "return_book",
    "description": "Allows a user to return a borrowed book, only if they were the one who borrowed it.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The exact title of the book to return"
            },
            "author": {
                "type": "string",
                "description": "The exact author name of the book to return"
            },
            "user": {
                "type": "string",
                "description": "The name of the user attempting to return the book"
            }
        },
        "required": ["title", "author", "user"]
    }
}


library_functions = [
    search_book_function,
    is_book_in_shelf_function,
    borrow_book_function,
    return_book_function
]