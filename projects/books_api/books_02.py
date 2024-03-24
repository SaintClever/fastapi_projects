from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

# The three biggest are:
# .dict() function is now renamed to .model_dump()
# schema_extra function within a Config class is now renamed to json_schema_extra
# Optional variables need a =None example: id: Optional[int] = None


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, description="id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5),
    Book(4, "HP1", "Author 1", "Book Description", 2),
    Book(5, "HP2", "Author 2", "Book Description", 3),
    Book(6, "HP3", "Author 3", "Book Description", 1),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    books_to_return = []

    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
# Assign an BookRequest to book_request
async def create_book(book_request: BookRequest):
    # dump the information of book_request into Book, which key/values of BookRequest: id=0 title='string' author='string' description='string' rating=0
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
