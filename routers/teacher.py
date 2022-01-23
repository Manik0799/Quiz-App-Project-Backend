from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder

from database import(
    create_teacher,
    fetch_all_teachers,
    fetch_teacher,
    update_teacher
)
from schemas import TeacherSchema, ShowTeacherSchema, UpdateTeacherSchema
from hashing import Hash

router = APIRouter(
    prefix = '/teacher',
    tags = ["Teachers"]
)

@router.get('/')
async def show_all():
    teachers = await fetch_all_teachers()
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Empty collection - No teacher found")
    return teachers

@router.get('/{id}', response_model= ShowTeacherSchema)
async def get_teacher(id):
    teacher = await fetch_teacher(id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Teacher with id - {id}, Not found")
    return teacher

@router.post('/')
async def add(request : TeacherSchema = Body(...)):
    teacher = jsonable_encoder(request)
    hashedPassword = Hash.bcrypt(teacher['password'])
    teacher['password'] = hashedPassword
    new_teacher = await create_teacher(teacher)
    return new_teacher

@router.put('/{id}')
async def update(id : str, request : UpdateTeacherSchema):
    req = {k: v for k, v in request.dict().items() if v is not None}
    # Hashing the received password
    hashedPassword = Hash.bcrypt(req['password'])
    req['password'] = hashedPassword
    # Updating the record
    updated_teacher = await update_teacher(id, req)
    if not updated_teacher:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Update could not be completed")
    return f"Record with id - {id}, Updated successfully"
        
