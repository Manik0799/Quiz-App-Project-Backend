import json


def prepare_options_for_each_question(questionData, questionType):
    if questionType == 'default':
        options = [
               { 
                   "option_id" : "1",
                   "description" : questionData["Option 1"]
               },
               { 
                   "option_id" : "2",
                   "description" : questionData["Option 2"]
               },
               { 
                   "option_id" : "3",
                   "description" : questionData["Option 3"]
               },
               { 
                   "option_id" : "4",
                   "description" : questionData["Option 4"]
               }
        ]

        return options
    else:
        options = [
               { 
                   "option_id" : "1",
                   "description" : questionData["Option 1"]
               },
               { 
                   "option_id" : "2",
                   "description" : questionData["Option 2"]
               }
        ]

        return options


def prepare_questions_from_dataframe(df):
    quiz_data =  json.loads(df.to_json(orient="index"))
    
    questions_list = []


    for question in quiz_data.values():
        options = prepare_options_for_each_question(question, question['Type'])

        data = {
            "question" : question['Question'],
            "type" : question['Type'],
            "time_duration" : question['Duration'],
            "max_marks" : question['Max Marks'],
            "correct_option_id" : question['Correct Option'],
            "options" : options
        }

        questions_list.append(data)
        
    return questions_list
