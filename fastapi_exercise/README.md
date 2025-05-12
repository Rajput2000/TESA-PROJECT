# 📚 Library Management API

A powerful and lightweight Library Management System built using **FastAPI**. This API allows users to manage a collection of books by performing operations such as borrowing, returning, searching, and tracking borrow history — all with clean and well-documented routes.

---

## 🚀 Features

✅ Add New Books  
✅ Search by Title or Author  
✅ Borrow and Return Books  
✅ Fine Calculation for Late Returns  
✅ Filter Books by Availability  
✅ Highlight Books with Prime Suffix in Title  
✅ Track Most Borrowed Books

---

## 🧑‍💻 Tech Stack

- **Language:** Python 3.8+
- **Framework:** FastAPI
- **Schema Validation:** Pydantic
- **Data Storage:** In-Memory (List of Dictionaries)
- **Date Handling:** datetime module

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Rajput2000/TESA-PROJECT.git
cd TESA-PROJECT/fastapi_exercise/

# Install dependencies
pip install fastapi uvicorn
```

---

## 🚦 Run the API Server

```bash
uvicorn main:app --reload
```

API will be available at:  
🔗 `http://127.0.0.1:8000`

Swagger UI for testing:  
🔗 `http://127.0.0.1:8000/docs`

---

## 📚 API Endpoints

| Method | Endpoint                 | Description                             |
| ------ | ------------------------ | --------------------------------------- |
| GET    | `/`                      | Welcome message                         |
| GET    | `/all-books`             | List all books                          |
| GET    | `/get-prime-suffix`      | Books with prime-number suffix in title |
| GET    | `/get-borrowed-books`    | List borrowed books                     |
| GET    | `/get-available-books`   | List available books                    |
| GET    | `/most-borrowed-book`    | Show most borrowed book(s)              |
| POST   | `/get-book-by-name`      | Search book by name                     |
| POST   | `/get-books-by-author`   | Search books by author                  |
| POST   | `/add-book`              | Add a new book                          |
| POST   | `/delete-by-name`        | Delete a book by name                   |
| POST   | `/borrow-book-by-author` | Borrow book using author name           |
| POST   | `/borrow-book-by-title`  | Borrow book using title                 |
| POST   | `/return-book-by-author` | Return book using author name           |
| POST   | `/return-book-by-title`  | Return book using title                 |

---

## 📋 Data Format

**Add Book:**

```json
{
  "book_name": "Fluent Python",
  "author_name": "Luciano Ramalho",
  "book_id": 937
}
```

**Borrow / Return:**

```json
{
  "book_name": "Fluent Python"
}
```

---

## 🎨 Sample JSON Response

```json
{
  "fine": 1500,
  "status": "Book has been Returned"
}
```

---

## 🤝 Collaborators

Built with ❤️ by:

- 🧑‍💼 Amarachi
- 🧑‍💼 Gbenga
- 🧑‍💼 Tomi
- 🧑‍💼 Emmanuel
- 🧑‍💼 Olusola
- 🧑‍💼 Tolu
- 🧑‍💼 Albert
- 🧑‍💼 Lola
- 🧑‍💼 Damilare
- 🧑‍💼 Doyin
- 🧑‍💼 Tunchi
- 🧑‍💼 Olawale

---

## 🌟 Show Your Support

If you find this project helpful, please ⭐ the repo and share it with others!
