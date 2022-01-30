from bson.objectid import ObjectId
# MongoDB Driver
import motor.motor_asyncio

MONGO_DETAILS = 'mongodb://localhost:27017'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.quizapp
courses_collection = database.courses
teachers_collection = database.teachers
students_collection = database.students

# helpers
def course_helper(course) -> dict :
    return{
        'id' : str(course['_id']),
        'course_name' : course['course_name'],
        'course_code' : course['course_code'],
        'creator_id' : course['creator_id']
        }

def teacher_helper(teacher) -> dict :
    return{
        'id' : str(teacher['_id']),
        'name' : teacher['name'],
        'email' : teacher['email'],
        'password' : teacher['password']
        }

def student_helper(student) -> dict :
    return{
        'id' : str(student['_id']),
        'name' : student['name'],
        'roll_no' : student['roll_no'],
        'email' : student['email'],
        'password' : student['password']
        }


# CRUD operations
async def fetch_all_courses():
    courses = []
    async for document in courses_collection.find():
        courses.append(course_helper(document))
    return courses

async def fetch_course(id : str):
    course = await courses_collection.find_one({'_id' : ObjectId(id)})
    if course:
        return course

async def create_course(course_data : dict) -> dict:
    course = await courses_collection.insert_one(course_data)
    new_course = await courses_collection.find_one({'_id' : course.inserted_id})
    return course_helper(new_course)

async def update_course(id : str, data : dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    course = await courses_collection.find_one({"_id": ObjectId(id)})
    if course:
        updated_course = await courses_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_course:
            return True
        return False
    
async def delete_course(id :str):
    course = await courses_collection.find_one({'_id' : ObjectId(id)})
    if course:
        await courses_collection.delete_one({'_id' : ObjectId(id)})
        return True

# CRUD Operations - Teacher User
async def fetch_all_teachers():
    teachers = []
    async for document in teachers_collection.find():
        teachers.append(teacher_helper(document))
    return teachers

async def fetch_teacher(id : str):
    teacher = await teachers_collection.find_one({'_id' : ObjectId(id)})
    if teacher:
        return teacher

async def create_teacher(teacher_data : dict) -> dict:
    teacher = await teachers_collection.insert_one(teacher_data)
    new_teacher = await teachers_collection.find_one({'_id' : teacher.inserted_id})
    return teacher_helper(new_teacher)

async def update_teacher(id : str, data : dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    teacher = await teachers_collection.find_one({"_id": ObjectId(id)})
    if teacher:
        updated_teacher = await teachers_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_teacher:
            return True
        return False

# CRUD Operations - Student User
async def fetch_all_students():
    students = []
    async for document in students_collection.find():
        students.append(student_helper(document))
    return students

async def fetch_student(id : str):
    student = await students_collection.find_one({'_id' : ObjectId(id)})
    if student:
        return student

async def create_student(student_data : dict) -> dict:
    student = await students_collection.insert_one(student_data)
    new_student = await students_collection.find_one({'_id' : student.inserted_id})
    return student_helper(new_student)

async def update_student(id : str, data : dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await students_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await students_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False
