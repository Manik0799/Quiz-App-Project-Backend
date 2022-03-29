from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.encoders import jsonable_encoder
from database import(
    create_student,
    fetch_all_students,
    fetch_student,
    update_student,
    join_course_with_id,
    courses_collection
)
from schemas import JoinCourseSchema, StudentSchema, ShowStudentSchema, UpdateStudentSchema
from hashing import Hash

router = APIRouter(
    prefix = '/student',
    tags = ["Students"]
)

@router.get('/')
async def show_all():
    students = await fetch_all_students()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Empty collection - No Student found")
    return students

@router.get('/{id}', response_model= ShowStudentSchema)
async def get_student(id):
    student = await fetch_student(id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Student with id - {id}, Not found")
    return student

@router.post('/')
async def add(request : StudentSchema = Body(...)):
    student = jsonable_encoder(request)
    hashedPassword = Hash.bcrypt(student['password'])
    student['password'] = hashedPassword
    new_student = await create_student(student)
    return new_student

@router.put('/{id}')
async def update(id : str, request : UpdateStudentSchema):
    req = {k: v for k, v in request.dict().items() if v is not None}
    # Hashing the received password
    hashedPassword = Hash.bcrypt(req['password'])
    req['password'] = hashedPassword
    # Updating the record
    updated_student = await update_student(id, req)
    if not updated_student:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Update could not be completed")
    return f"Record with id - {id}, Updated successfully"
        



# Other functional API endpoints
@router.post('/join-course')
async def join_course(info : JoinCourseSchema = Body(...) ):

    info = jsonable_encoder(info)
    studentId = info['studentId']
    courseId = info['courseId']
   
    # 1. Search if the course exists in the database
    fetched_course = await courses_collection.find_one({'_id' : courseId})

    if fetched_course:
        # 2. Course exists, append the course details to the student document.

        course_data = {
            'id' : fetched_course['_id'],
            'course_code' : fetched_course['course_code'],
            'course_name' : fetched_course['course_name']
        }

        response = await join_course_with_id(studentId, course_data)
        if response:
            return {'message' : 'Successfully joined the Class'}
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Error in joining the class")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Invalid Course Code! Please try again")
    

