from fastapi import APIRouter, HTTPException, status
from hashing import Hash
from jwt_token import create_access_token
from schemas import Login
from database import (students_collection, teachers_collection)
router = APIRouter(
    tags = ["Login"],
    prefix = '/login'
)

# Function to perform DB check, password matching & returning of JWT token
def helper_function(user, request):
    # Checking user's presence in the db
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Invalid Credentials' )
    # Password checking
    if not Hash.verify_password(user.get('password'), request.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Invalid Credentials')
    # Generate a JWT Token
    access_token = create_access_token(data = {'sub' : user.get('email')})
    return access_token

@router.post('/student')
async def login_student(request : Login):
    user = await students_collection.find_one({'email' : request.email})
    access_token = helper_function(user, request)
    return {'access_token' : access_token, 'token_type' : 'bearer'}

@router.post('/teacher')
async def login_teacher(request : Login):
    user = await teachers_collection.find_one({'email' : request.email})
    access_token = helper_function(user, request)
    return {'access_token' : access_token, 'token_type' : 'bearer'}