from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from database import (
    add_course_to_teacher,
    fetch_all_courses,
    fetch_course,
    create_course,
    update_course,
    delete_course
)
from oauth2 import get_current_user
from schemas import CourseSchema, ShowCourse, TeacherSchema, UpdateCourseSchema


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
   
    # The next line currently prints just the user email that has been logged in
    # print(current_user)
    # By getting the current logged in email of the teacher, we need to get the objectID of that
    # teacher, in order to insert it into the database, when a course is being created!!!

    course = jsonable_encoder(course)
    new_course = await create_course(course)

    if new_course:

        # Fetch the id and the course code of the newly added course and add the course to the courses list of the teacher
        teacher_id = new_course['creator_id']
        # Sending the request to teachers collection to add the new course to the teacher
        course_data = {
            'id' : new_course['id'],
            'course_code' : new_course['course_code'],
            'course_name' : new_course['course_name']
        }

        response = await add_course_to_teacher(teacher_id, course_data)

        if response:
            return {'message': 'Course added successfully'}

    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Please Insert a valid creator_id")

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


# , current_user : TeacherSchema = Depends(get_current_user)
