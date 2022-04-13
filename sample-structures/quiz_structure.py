# Quiz structure
{
    "_id" : "6242ee323a5ff04b30f73ad6", #(created in backend)
    "course_id" : "6242d648129d9865faaa471d", # course_id to which the quiz is linked
    "no_of_questions" : 2,
    "start_time" : 1649738400000, # UNIX timestamp in milliseconds
    "duration" : 10, # in minutes
    "end_time" : 1649739000000, # start_time + duration (no need to send this from frontend)
    "total_marks" : 10, # Addition of max_marks of all questions (no need to send this from frontend)
    "created_at" : 1649594097000, # UNIX timestamp in milliseconds

    "questions" : [ 
        # Question 1
        {
            "question_id" : "6242d671129d9865faaa471e", #(created in backend)
            "question" : "What is the capital of India?",
            "type" : "default", # default or numerical,
            "time_duration" : 60, # in seconds
            "max_marks" : 5,
            "correct_option_id" : "2",
            "options" : [
                {
                    "option_id" : "1",
                    "description" : "Mumbai" 
                },
                {
                    "option_id" : "2",
                    "description" : "New Delhi" 
                },
                {
                    "option_id" : "3",
                    "description" : "Kolkata" 
                },
                {
                    "option_id" : "4",
                    "description" : "Chandigarh" 
                },
            ]
        },
        # Question 2
        {
            "question_id" : "6242d671129d9865faaa471f", #(created in backend)
            "question" : "What is the full form of USA?",
            "type" : "default", # default or numerical
            "time_duration" : 60, # in seconds
            "max_marks" : 5,
            "correct_option_id" : "3",
            "options" : [
                {
                    "option_id" : "1",
                    "description" : "United Spirit Alliance" 
                },
                {
                    "option_id" : "2",
                    "description" : "United Sovereign Alliance" 
                },
                {
                    "option_id" : "3",
                    "description" : "United States of America" 
                },
                {
                    "option_id" : "4",
                    "description" : "United Structure of America" 
                },
            ]
        },  
    ],
}