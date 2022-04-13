import datetime, time, bson
from bson.objectid import ObjectId

def create_additional_fields_for_quiz(req):
    # Calculating end_time of the quiz
    end_time = req["start_time"] + req["duration"] * 60 * 1000
    req["end_time"] = end_time

    # Calculating the total marks
    # And creating 'question_id' for each question
    total_marks = 0
    if "questions" in req:
        for question in req["questions"]:
            question_max_marks = question["max_marks"]
            total_marks += question_max_marks

            # create 'question_id' field
            id  = ObjectId()
            question['question_id'] = str(id)
    
    req["total_marks"] = total_marks

     # generating timestamp for the created_at field
    dtime = datetime.datetime.now()
    createdAt = time.mktime(dtime.timetuple())*1000
    req["created_at"] = bson.int64.Int64(createdAt)


    return req
