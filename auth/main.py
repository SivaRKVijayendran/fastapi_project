from fastapi import FastAPI , Depends , HTTPException , status
from sqlalchemy.orm import Session
from auth_model import User
from schema import User_create , change_username , ForgotPasswordRequest , ResetPasswordRequest
from auth_database import get_db
from jose import jwt
from utils import hash_password, ALGORITHM, SECRET_KEY, verify_password, create_access_token, create_reset_token
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import JWTError

app = FastAPI()

@app.post("/signup")
def register_user(user : User_create , db : Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="User already exist")

    hashed_password_from_inmethod = hash_password(user.password)

    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password_from_inmethod,
        role = user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'id' : new_user.id , 'username' : new_user.username , 'email' : new_user.email , 'role' : new_user.role}

@app.post("/login")
def login(form_data : OAuth2PasswordRequestForm  =Depends(), db : Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == form_data.username).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,  detail="Invalid Username")

    if not verify_password(form_data.password , existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid Password")

    token_data = {'sub' : existing_user.username , 'role' : existing_user.role}
    token = create_access_token(token_data)

    return {'access_token' : token , 'token_type' : 'bearer'}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token : str = Depends(oauth2_scheme)):
    headers_in = {"www-Authenticate": "Bearer"}
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Could not validate data" , headers=headers_in)


    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        role : str = payload.get("role")
        if username is None or role is None:
            raise credential_exception
    except JWTError :
        raise credential_exception

    return {"username" : username , "role" : role}

@app.get("/protected")
def protected_route(current_user : dict = Depends(get_current_user)):
    return {"Message" : f"Hello welcome {current_user['username'] } and your role is {current_user['role']} | You accessed a protected route "}


def require_roles(allowed_roles : list[str]):
    def role_check(current_user : dict = Depends(get_current_user)):
        user_role = current_user.get('role')
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not enough permission")

        return current_user
    return role_check

@app.get("/profile")
def get_profile(current_user : dict = Depends(require_roles(["admin" , "user"]))):
    return {"Message" : f"user name {current_user['username']} and your role is {current_user['role']}"}

@app.put("/changeusername")
def change_username(update_username : change_username, currect_user : dict = Depends(require_roles(["admin"])), db : Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.id == update_username.id).first()


    if existing_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not found")

    existing_user.username = update_username.username

    db.commit()
    db.refresh(existing_user)

    return {
        'id': existing_user.id,
        'username': existing_user.username,
        'email': existing_user.email,
        'role': existing_user.role
    }


@app.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    reset_token = create_reset_token({"sub": user.username})

    return {"reset_token": reset_token}

@app.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.hashed_password = hash_password(data.new_password)

    db.commit()
    db.refresh(user)

    return {"message": "Password reset successful"}