from database import quizzes_collection

async def check_answers(data):
    if len(data['answers']) == 0:
        data["total_marks_obtained"] = 0
        return data

    # Fetch the quiz details from the quiz collection in db
    quiz_data = await quizzes_collection.find_one({'_id' : data['quiz_id']}, {'no_of_questions' : 1, "questions" : 1})
    questions = quiz_data['questions']

    total_marks_obtained = 0

    for answer in data['answers']:
        if 'question_id' and 'marked_option_id' in answer:
            question_id = answer['question_id']
            
            # Match this question_id with quiz data questions
            for question in questions:
                if question_id == question['question_id']:
                    # Check if this is a correct answer
                    marked_option = answer['marked_option_id']
                    correct_option = question['correct_option_id']

                    if marked_option == correct_option:
                        answer['correct'] = True
                        answer['marks_obtained'] = question['max_marks']
                        total_marks_obtained += question['max_marks']
                    else:
                        answer['correct'] = False
                        answer['marks_obtained'] = 0

    
    data['total_marks_obtained'] = total_marks_obtained

    return data

    