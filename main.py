from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import course, quiz, teacher, student, login

app = FastAPI()

origins = ['https://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course.router)
app.include_router(teacher.router)
app.include_router(student.router)
app.include_router(login.router)
app.include_router(quiz.router)

