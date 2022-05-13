from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
import time, bson, io, uuid, datetime, base64

from database import(
    create_student,
    fetch_all_students,
    fetch_student,
    update_student,
    join_course_with_id,
    quizzes_collection,
    courses_collection,
    students_collection,
    teachers_collection
)
from helperFunctions.uploadImagesToS3 import upload_images_to_s3, bucket_name

from helperFunctions.createPresignedUrl import create_presigned_url
from helperFunctions.sendEmail import send_email
from oauth2 import get_current_user
from schemas import JoinCourseSchema, StudentSchema, ShowStudentSchema, UpdateStudentSchema
from hashing import Hash

router = APIRouter(
    tags = ["Students"]
)


class Student(BaseModel):
    email : str
    id : str

# @router.get('/')
# async def show_all():
#     students = await fetch_all_students()
#     if not students:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Empty collection - No Student found")
#     return students

@router.get('/student', response_model= ShowStudentSchema)
async def get_student(current_user : Student = Depends(get_current_user)):
    student = await fetch_student(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Student with id - {id}, Not found")
    return student

@router.post('/student')
async def add(request : StudentSchema = Body(...)):

    student = jsonable_encoder(request)
    hashedPassword = Hash.bcrypt(student['password'])
    student['password'] = hashedPassword
    new_student = await create_student(student)
    return {'message' : 'Successfully created new user'}

@router.put('/student')
async def update(request : UpdateStudentSchema, current_user : Student = Depends(get_current_user)):

    id = current_user.id

    req = {k: v for k, v in request.dict().items() if v is not None}

    if req.get('password'):
        # Hashing the received password
        hashedPassword = Hash.bcrypt(req.get('password'))
        req['password'] = hashedPassword

    # Updating the record
    updated_student = await update_student(id, req)
    if not updated_student:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Update could not be completed")
    return f"Record with id - {id}, Updated successfully"
        


# Other functional API endpoints
@router.post('/student-join-course')
async def join_course(info : JoinCourseSchema = Body(...), current_user : Student = Depends(get_current_user)):
    
    studentId = current_user.id
    info = jsonable_encoder(info)
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
    

# Get all the courses that a student has joined


@router.get('/student-joined-courses')
async def get_joined_courses(current_user : Student = Depends(get_current_user)):

    # Fetching the id of the current logged in student
    studentId = current_user.id
    
    # For this studentId fetch all the courses that he/she has enrolled in
    info = await students_collection.find_one({'_id': studentId}, {'courses' : 1, '_id' : 0})

    if (len(info.get('courses'))) == 0:
        return {'message' : "Student has not joined any course yet"}
    else:
        return info.get('courses')



def quizListHelper(quiz) -> dict :
    return{
        'id' : str(quiz['_id']),
        }

# Get all the quizzes a student has given of a particular course
@router.get('/student-given-quizzes/{courseId}')
async def get_given_quizzes_of_student_by_courseId(courseId : str, current_user : Student = Depends(get_current_user)):
    # Fetching the id of the current logged in student
    studentId = current_user.id
    
    # Fetch all quiz data from student's collection
    quizData = await students_collection.find_one({'_id' : studentId}, {'quizzes' : 1, '_id': 0})
    quizListofStudent =  quizData.get('quizzes')

    if(len(quizListofStudent) == 0):
        return []

    quizGivenData = []
    
    for quiz in quizListofStudent:
        course_id = quiz.get('course_id')
        if(course_id == courseId):
            quizGivenData.append(quiz)

    return quizGivenData



# Send marked responses as a mail
# One element from the above route array will be the request payload to this endpoint
@router.post('/student-send-responses-mail')
async def send_response_mail(req : Request, current_user : Student = Depends(get_current_user)):
    req = await req.json()
    studentId = current_user.id
    studentEmail = current_user.email
    quizId = req.get('quiz_id')
    courseId = req.get('course_id')
    marked_answers = req.get('answers')

    # Send email to user
    response = send_email(req, studentEmail) 
    
    return response


@router.post('/student-quiz-images')
async def upload_student_images(req : Request):

    req = await req.json()

    base64_str = req.get("base64_string")
    course_id = req.get('course_id')

    # Encoding and decoding the base64 string
    base64_encoded = base64_str.encode('utf-8')
    base64bytes = base64.b64decode(base64_encoded, validate= True)
    bytesObj = io.BytesIO(base64bytes)
    bytesObj.seek(0)

    # Generating filename
    # Random UUID generated
    fileName = str(uuid.uuid1())
    complete_filename = fileName + ".jpeg" 


    response = upload_images_to_s3(bytesObj, complete_filename, bucket_name)
    if response == "error":
        return {"error" : "Could not upload User Images."}
    
    message = ""

    responseURL = create_presigned_url(complete_filename)
    if responseURL:
        message = responseURL

    creatorResponse = await courses_collection.find_one({'_id' : course_id}, {'creator_id' : 1, '_id' : 0})
    
    emailResponse = await teachers_collection.find_one({'_id' : creatorResponse.get('creator_id') }, {'email' : 1, '_id' : 0}) 

    if emailResponse.get('email'):
        email_teacher = emailResponse.get('email')

        response = send_email(message = message, recepientMail= email_teacher)

        return {'message' : 'Email sent to recepient'}