from bson.objectid import ObjectId
# MongoDB Driver
import motor.motor_asyncio

MONGO_DETAILS = 'mongodb://localhost:27017'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.quizapp
courses_collection = database.courses

# helpers
def course_helper(course) -> dict :
    return{
        'id' : str(course['_id']),
        'course_name' : course['course_name'],
        'course_code' : course['course_code'],
        'creator_id' : course['creator_id']
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