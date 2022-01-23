from passlib.context import CryptContext

# Hashing the password before storing it to the db
pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class Hash():
    def bcrypt(password: str):
        hashedPassword = pwd_context.hash(password)
        return hashedPassword
    
    def verify_password(hashedPassword, plainPassword):
        return pwd_context.verify(plainPassword, hashedPassword)