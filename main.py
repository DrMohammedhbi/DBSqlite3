from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Student(BaseModel):
  id: int
  name: str
  grade: int

def setup_database():
  try:
      conn = sqlite3.connect('students.db')  # Create a connection to the database
      cursor = conn.cursor()  # Create a cursor
      cursor.execute(''' 
          CREATE TABLE IF NOT EXISTS students (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              grade INTEGER
          )
      ''')
      conn.commit()  # Save changes
  except sqlite3.Error as e:  # Handle potential errors
      print(e)  # Print the error
      return {"error": "Failed to fetch students"}  # Return an error message if data fetching fails

setup_database()

@app.get("/students/")
async def read_students():
  try:
      conn = sqlite3.connect('students.db')  # Create a connection to the database
      cursor = conn.cursor()  # Create a cursor to interact with the database
      cursor.execute("SELECT * FROM students")  # Execute an SQL query to fetch all rows from the students table
      rows = cursor.fetchall()  # Fetch all results from the database
      conn.close()  # Close the database connection
      return rows  # Return the data fetched from the database
  except sqlite3.Error as e:  # Handle potential errors
      print(e)  # Print the error
      return {"error": "Failed to fetch students"}  # Return an error message if data fetching fails

@app.post("/students/")
async def create_student(student: Student):
  try:
      conn = sqlite3.connect('students.db')
      cursor = conn.cursor()
      cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (student.name, student.grade))
      conn.commit()
      conn.close()
      return {"message": "Student added successfully"}
  except sqlite3.Error as e:
      print(e)
      return {"error": "Failed to create student"}

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
  try:
      conn = sqlite3.connect('students.db')  # Create a connection to the database
      cursor = conn.cursor()  # Create a cursor
      cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?",
                    (student.name, student.grade, student_id))  # SQL to update student data
      conn.commit()  # Save changes to the database
      conn.close()  # Close the connection
      return {"id": student_id, **student.dict()}  # Return the updated student data
  except sqlite3.Error as e:  # In case of an error
      print(e)  # Print the error
      return {"error": "Failed to update student"}  # Return an error message

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
  try:
      conn = sqlite3.connect('students.db')  # Create a connection to the database
      cursor = conn.cursor()  # Create a cursor
      cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))  # Execute an SQL query to delete a student
      conn.commit()  # Save changes to the database
      conn.close()  # Close the connection
      return {"message": "Student deleted"}  # Return a confirmation message of deletion
  except sqlite3.Error as e:  # In case of an error
      print(e)  # Print the error
      return {"error": "Failed to delete student"}  # Return an error message