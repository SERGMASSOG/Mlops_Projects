from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class BOOKS:
    id: int
    Title: str
    Author: str
    description: str
    category: str
    date: int

    def __init__(self, id, Title, Author, description, category,date):
        self.id = id
        self.Title = Title
        self.Author = Author
        self.description = description
        self.category = category
        self.date = date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="The id of the book", default=None)
    Title: str = Field(min_length=3)
    Author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    category: str = Field(min_length=3, max_length=10)
    date: int = Field(gt=1800, lt=2026)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Name Author",
                "description": "description book",
                "category": "category book",
                "date": "date book"
            }
        }
    }

Book = BOOKS
BOOKS = [
    Book(1, "Rosa", "Pedro", "Libro de ciencia sobre las rosas", "Science",1999),
    Book(2, "Pastel", "Carlos", "Libro nuevo de tecnologia", "Technology",2000),
    Book(3, "Coco", "Santiago", "Libro nuevo de ciencia", "Science",2020),
    Book(4, "Mandarina", "Pedro", "Libro sobre IA", "Technology",1972),
    Book(5, "Nuevo", "Carlos", "Arte y sus cosas", "Arte",1967),
    Book(6, "Rosa 2", "Pedro", "Tecnologia como medio", "Technology",2004),
    Book(7, "Coco 2", "Santiago", "Arte contemporaneo", "Arte",2020),
    Book(8, "Mandarina 2", "Felipé", "Carros y sus tecnologias", "Technology",1999),
    Book(9, "Coco 4", "Felipé", "La ciencia de las cosas", "Science",2000)
]
@app.get("/Books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(Create_book=BookRequest):
    new_book = Book(**Create_book.dict())
    BOOKS.append(new_book)

@app.get("/Books/{id}", status_code=status.HTTP_200_OK)
async def get_book(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/Books/", status_code=status.HTTP_200_OK)
async def get_books_category(book_category):
    book_cat = []
    for book in BOOKS:
        if book.category == book_category:
            book_cat.append(book)
    return book_cat

@app.get("/Books/date/", status_code=status.HTTP_200_OK)
async def get_books_date(date:int = Query(gt=0, lt=2026)):
    books_date = []
    for book in BOOKS:
        if book.date == date:
            books_date.append(book)

    return books_date


# Actualizacion
@app.put("/Books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(Update_book=BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == Update_book.id:
            BOOKS[i] = Update_book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


# Eliminacion
@app.delete("/Books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int = Path(gt=0)):
    book_changed = False
    for book in BOOKS:
        if book.id == id:
            BOOKS.remove(book)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")

