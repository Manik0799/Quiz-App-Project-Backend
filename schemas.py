from tkinter.tix import INTEGER
from turtle import st
from typing import Optional
from pydantic import BaseModel, Field

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