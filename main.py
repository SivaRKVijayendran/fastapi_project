from fastapi import FastAPI, Query , status
from fastapi.exceptions import HTTPException
from typing import Optional
from model import Book , Book_update

app = FastAPI()


books = [
    Book( id = 1 , title = "400days" , author = "chetan bhagat" , publish_date = "05-09-2018"),
    Book( id = 2 , title = "Half Girlfriend" , author = "chetan bhagat" , publish_date = "05-09-2010")
]

@app.get("/")
def welcome():
    return {"Messasge " : " Welcome to my app... "}

@app.get("/greet/{name}")  #http://127.0.0.1:8000/greet/Siva url la value pass panrom ithu path parameter
def greet_with_path_parameter(name : str):
    return {"Message " : f" Hello {name}"}

@app.get("/greetage/{name}")  #http://127.0.0.1:8000/greetage/Siva?age=25 or http://127.0.0.1:8000/greet/Siva url la value pass panrom and ? aprm oru pass panrom athu tha query parameter
def greet_with_path_parameter(name : str , age : Optional[int] = None):
    return {"Message " : f" Hello {name} and your age is {age}"}

@app.get("/greetage")  #http://127.0.0.1:8000/greetage?name=Siva&age=25 url la ? aprm values pass panrom athu tha query parameter
def greet_with_path_parameter(name : str , age : Optional[int] = None):
    return {"Message " : f" Hello {name} and your age is {age}"}

@app.get("/greetagewithquery")
def greet_with_path_parameter(
    name: str = Query("Nandhini Siva", description="User Name"),
    age: int = Query(1, description="Age of the user")
):
    return {"Message " : f" Hello {name} and your age is {age}"}

@app.get("/getallbooks")
def get_all_books():
    return books

@app.get("/getbyid")
def get_by_id(
        qid : int = Query(1 , description="Please provide id")
):
    for i in books:
        if i.id == qid:
            return i
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not found")

@app.post("/createbook")
def create_new_book(bk : Book):
    books.append(bk)
    for i in books:
        if i.id == bk.id:
            return i
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not found")

@app.put("/updatebookbyid/{bid}")
def update_book_by_id(bid : int , b_update : Book_update):
    for i in books:
        if i.id == bid:
            i.title = b_update.title
            i.author = b_update.author
            i.publish_date = b_update.publish_date

            return i
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUN , detail="Book is not found or invalid")


@app.delete("/deletebyid/{bid}")
def delete_by_id(bid : int):
    for i in books:
        if i.id == bid:
            books.remove(i)
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book id is not found or invalid" )