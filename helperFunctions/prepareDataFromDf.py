import json
def prepare_questions_from_dataframe(df):
    quiz_data =  json.loads(df.to_json(orient="index"))
    
    questions_list = []

    for question in quiz_data.values():
        data = {
            "question" : question['Question'],
            "type" : question['Type'],
            "time_duration" : question['Duration'],
            "max_marks" : question['Max Marks'],
            "correct_option_id" : question['Correct Option'],
            "options" : [
               { 
                   "option_id" : "1",
                   "description" : question["Option 1"]
               },
               { 
                   "option_id" : "2",
                   "description" : question["Option 2"]
               },
               { 
                   "option_id" : "3",
                   "description" : question["Option 3"]
               },
               { 
                   "option_id" : "4",
                   "description" : question["Option 4"]
               }

            ]
        }

        questions_list.append(data)
        
    return questions_list
