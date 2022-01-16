from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import (
    fetch_all_courses,
    fetch_course,
    create_course,
    update_course,
    delete_course
)
from schemas import CourseSchema, ShowCourse, UpdateCourseSchema


router = APIRouter(
    prefix = '/course',
    tags = ["Courses"]
)

@router.get('/')
async def get_all():
    courses = await fetch_all_courses()
    if not courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Empty collection - no course found")
    return courses

@router.get('/{id}', response_model= ShowCourse)
async def get_course(id):
    course = await fetch_course(id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Course with id - {id}, Not found")
    return course

@router.post('/')
async def add(course: CourseSchema = Body(...)):
    course = jsonable_encoder(course)
    new_course = await create_course(course)
    return {'data' : new_course}

@router.put('/{id}')
async def update(id : str, request : UpdateCourseSchema):
    req = {k: v for k, v in request.dict().items() if v is not None}
    updated_course = await update_course(id, req)
    if not updated_course:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Update could not be completed")
    return f"Record with id - {id}, Updated successfully"
        


@router.delete('/{id}')
async def drop(id):
    deleted_course = await delete_course(id)
    if deleted_course:
        return {'detail' : f'Course with id {id} successfully deleted'}
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail= "Course not found in the db")

