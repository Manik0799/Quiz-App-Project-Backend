from fastapi import APIRouter, File, Request, HTTPException, UploadFile, status
import pandas as pd
from database import courses_collection, create_quiz, insert_quiz_data_to_student, quizzes_collection, students_collection
from helperFunctions.checkQuizAnswers import check_answers
from helperFunctions.createQuiz import create_additional_fields_for_quiz
from helperFunctions.prepareDataFromDf import prepare_questions_from_dataframe
router = APIRouter(
    prefix = '/quiz',
    tags = ["Quiz"]
)


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
        return {'message': 'Quiz successfully created'}
    
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to create the quiz")


# Submit quiz
@router.post("/submit-quiz")
async def submit_quiz(req : Request):
    req = await req.json()

    if not "quiz_id" in req or not "student_id" in req or not "answers" in req:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Missing fields")
    
    # Checking the validity of the quiz_id
    quiz = await quizzes_collection.find_one({'_id' : req['quiz_id']})
    if not quiz:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No quiz found with given quizId")

    # Checking the validity of the student_id
    student = await students_collection.find_one({'_id' : req['student_id']})
    if not student:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Invalid studentId")
    
    # Deleting the studentId field from the req
    student_id = req['student_id']
    del req['student_id']

    # Checking the answers
    result = await check_answers(req)

    # return result

    # Insert the result to the specific studentId
    response = await insert_quiz_data_to_student(studentId= student_id, quiz_data= result)

    if response:
            return {'message' : 'Successfully submitted the Quiz'}
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Error in quiz submission")

# Route for reading the csv file of the quiz questions
@router.post('/read-csv-file')
async def read_questions_from_csv_file(csv_file : UploadFile = File(...)):
    dataframe = pd.read_csv(csv_file.file)

    response = prepare_questions_from_dataframe(dataframe)
    return response
