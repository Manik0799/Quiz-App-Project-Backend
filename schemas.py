from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# Course Schema
class CourseSchema(BaseModel):
    course_name : str = Field(...)
    course_code : str 
    creator_id : int = Field(...)

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