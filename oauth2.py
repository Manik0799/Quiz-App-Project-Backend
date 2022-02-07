from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from jwt_token import verify_token


# 'login/teacher' is the route from where fastAPI will fetch
#  the token and then check its validity in the get_current_user() function
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/teacher")

# this function checks the validity of the JWT token
def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # We try to decode the token we are having
    # This function is being imported from 'jwt_token.py'
    return verify_token(token, credentials_exception)
