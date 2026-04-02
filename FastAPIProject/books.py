from fastapi import Body, FastAPI, HTTPException

app = FastAPI()

BOOKS = [
    {"Title": "Rosa", "Author": "Pedro", "category":"Science"},
    {"Title": "Pastel", "Author": "Carlos","category":"Technology"},
    {"Title": "Coco", "Author": "Santiago","category":"Arte"},
    {"Title": "Mandarina", "Author": "Felipé","category":"Psychology"},
    {"Title": "Nuevo", "Author": "Sebastian","category":"Science"}
]
# Metodos Get
@app.get("/api-endpoint")
async def first_api():
    return BOOKS

@app.get("/books/")
async def read_categories(categories: str):
    books = []
    for book in BOOKS:
        if books.get("category") == categories.casefold():
            books.append(book)
    return books

@app.get("/books/{book_autor}/")
async def read_book_author(book_autor: str, categories: str):
    books = []
    for book in BOOKS:
        if (book.get("author").casefold() == book_autor.casefold() and
                book.get("category").casefold() == categories.casefold()):
            books.append(book)
    return books

# Metodos Post CREAR
@app.post("/books/create")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

# Metodos Put actualizar
@app.put("/books/update")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("Title").casefold() == updated_book.get("Title").casefold():
            BOOKS[i].update(updated_book)

# Metodo Delete borrar
@app.delete("/books/delete/{book_Title}")
async def delete_book(book_Title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("Title").casefold() == book_Title.casefold():
            BOOKS[i].pop("Title")
            break
        