from fastapi import APIRouter, Depends, File, Request, HTTPException, UploadFile, status
import pandas as pd
from pydantic import BaseModel
from database import add_quiz_to_course_collection, courses_collection, create_quiz, fetch_quiz, insert_quiz_data_to_student, quizzes_collection, students_collection
from helperFunctions.checkQuizAnswers import check_answers
from helperFunctions.createQuiz import create_additional_fields_for_quiz
from helperFunctions.prepareDataFromDf import prepare_questions_from_dataframe
from oauth2 import get_current_user
router = APIRouter(
    prefix = '/quiz',
    tags = ["Quiz"]
)


class Student(BaseModel):
    email : str
    id : str

# Get Quiz by Id
@router.get('/{id}')
async def get_quiz_by_id(id : str):
    quiz = await fetch_quiz(id)
    
    if quiz:
        courseId = quiz.get('course_id')
        data = await courses_collection.find_one({'_id': courseId}, {'course_name' : 1, 'course_code' : 1, '_id' : 0})
        
        if data :
            quiz['course_code'] = data.get('course_code')
            quiz['course_name'] = data.get('course_name')

        return quiz

    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Quiz with id - {id}, Not found")
    

# Get all quizzzes in a course
@router.get('/course-quizzes/{course_id}')
async def get_quizzes(course_id: str):
    responseData = await courses_collection.find_one({'_id' : course_id}, {'quizzes' : 1, '_id' : 0})

    if responseData:
        return responseData.get('quizzes')

# Create a quiz
@router.post("/create-quiz")
async def create_new_quiz(req : Request):
    req = await req.json()

    if not "course_id" in req or not "start_time" in req or not "duration" in req:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Please send all fields in request")
    
    # Checking the validity of the 'course_id' field
    course = await courses_collection.find_one({'_id' : req['course_id']})
    if not course:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No course found with given courseId")


    req = create_additional_fields_for_quiz(req)

    # Request to the database for adding quiz to the collection
    response = await create_quiz(req)

    if response:
        # Fetching the course_id to which the new quiz belongs
        course_id = req['course_id']
        quiz_data = {
            '_id' : req['_id'],
            'no_of_questions' : req['no_of_questions'],
            'end_time' : req['end_time']
        }

        res = await add_quiz_to_course_collection(course_id = course_id, quiz_info= quiz_data)
        if res:
            return {'message': 'Quiz successfully created'}
    
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to create the quiz")


# Submit quiz
@router.post("/submit-quiz")
async def submit_quiz(req : Request, current_user : Student = Depends(get_current_user)):
    
    studentId = current_user.id
    req = await req.json()

    if not "quiz_id" in req or not "answers" in req:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Missing fields")
    
    # Checking the validity of the quiz_id
    quiz = await quizzes_collection.find_one({'_id' : req['quiz_id']})
    if not quiz:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No quiz found with given quizId")

    # Checking the validity of the student_id
    student = await students_collection.find_one({'_id' : studentId})
    if not student:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Invalid studentId")
    
    # Deleting the studentId field from the req
    student_id = studentId

    # Checking the answers
    result = await check_answers(req)

    # return result

    # Insert the result to the specific studentId
    response = await insert_quiz_data_to_student(studentId= student_id, quiz_data= result)

    if response:
            return {'message' : 'Successfully submitted the Quiz', 'total_marks' : result.get('total_marks_obtained')}
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Error in quiz submission")

# Route for reading the csv file of the quiz questions
@router.post('/read-csv-file')
async def read_questions_from_csv_file(csv_file : UploadFile = File(...)):
    dataframe = pd.read_csv(csv_file.file)

    response = prepare_questions_from_dataframe(dataframe)
    return response
