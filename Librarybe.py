from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client
from datetime import date

URL = "https://setqlbimqqcdyurphtms.supabase.co"
KEY = "sb_publishable_sLz5kgcPPmZvDe2sJXtipA_e3c5nsQl"

db = create_client(URL, KEY)

app = FastAPI(title="Library Management System")



# GET all books
@app.get("/books")
def get_all_books():
    res = db.table("BOOKS").select("*").execute()
    return JSONResponse(res.data)


# ADD a new book
@app.post("/books")
def add_book(book_name: str):
    db.table("BOOKS").insert({
        "Book Name": book_name
    }).execute()
    return JSONResponse({"message": "Book added"})


# GET book by id
@app.get("/books/{book_id}")
def get_book(book_id: int):
    res = db.table("BOOKS").select("*").eq("id", book_id).execute()
    return JSONResponse(res.data)


# DELETE book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    db.table("BOOKS").delete().eq("id", book_id).execute()
    return JSONResponse({"message": "Book deleted"})




# ISSUE BOOK TO STUDENT
@app.post("/issue-book")
def issue_book(book_id: int, student_id: int):
    # get book name from BOOKS table
    book = db.table("BOOKS").select("*").eq("Book id", book_id).execute().data

    if not book:
        return JSONResponse({"message": "Book not found"})

    db.table("Management").insert({
        "Book Name": book[0]["Book Name"],
        "Student id": student_id,
        "Book Collected Date": ""
    }).execute()

    return JSONResponse({"message": "Book issued successfully"})


# GET all transactions
@app.get("/transactions")
def get_all_transactions():
    res = db.table("Management").select("*").execute()
    return JSONResponse(res.data)


# GET transactions of a student
@app.get("/transactions/student/{student_id}")
def get_student_transactions(student_id: int):
    res = db.table("Management").select("*").eq("Student_id", student_id).execute()
    return JSONResponse(res.data)


# COLLECT / RETURN BOOK
@app.put("/collect-book/{transaction_id}")
def collect_book(transaction_id: int):
    db.table("Management").update({
        "Book_Collected_Date": date.today()
    }).eq("id", transaction_id).execute()

    return JSONResponse({"message": "Book collected"})


# DELETE transaction
@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    db.table("Management").delete().eq("id", transaction_id).execute()
    return JSONResponse({"message": "Transaction deleted"})


