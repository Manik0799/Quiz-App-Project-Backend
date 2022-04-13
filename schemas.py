from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

# Course Schema
class CourseSchema(BaseModel):
    course_name : str = Field(...)
    course_code : str 
    creator_id : str = Field(...)

class ShowCourse(CourseSchema):
    class Config():
        orm_mode = True

class UpdateCourseSchema(BaseModel):
    course_name : Optional[str]
    course_code : Optional[str]
    class Config():
        orm_mode = True

# /////////////////////////////////////////////////////
# Teacher Schema
class TeacherSchema(BaseModel):
    name : str = Field(...)
    email : EmailStr = Field(...)
    password : str = Field(...)
    courses  : List = []

class ShowTeacherSchema(BaseModel):
    name : str = Field(...)
    email : EmailStr = Field(...)

    class Config():
        orm_mode = True

class UpdateTeacherSchema(BaseModel):
    name : Optional[str]
    email : Optional[EmailStr]
    password : Optional[str]
    class Config():
        orm_mode = True

# ///////////////////////////////////////
# Student Schema
class StudentSchema(BaseModel):
    name : str = Field(...)
    roll_no : str
    email : EmailStr = Field(...)
    password : str = Field(...)
    courses  : List = []
    quizzes : List = []

class ShowStudentSchema(BaseModel):
    name : str = Field(...)
    roll_no : str = Field(...)
    email : EmailStr = Field(...)

    class Config():
        orm_mode = True

class UpdateStudentSchema(BaseModel):
    name : Optional[str]
    roll_no : Optional[str]
    email : Optional[EmailStr]
    password : Optional[str]
    class Config():
        orm_mode = True

class JoinCourseSchema(BaseModel):
    studentId : str = Field(...)
    courseId : str  = Field(...)

# Login Schema
class Login(BaseModel):
    email : EmailStr = Field(...)
    password : str = Field(...)

# For JWT Token
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    email : Optional[str] = None