from sqlalchemy.orm import sessionmaker
from database.models import User, Password, engine
from sqlalchemy.exc import IntegrityError
from session_manager import generate_token

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

def create_user(email, password):
    new_user = User(email=email, password=password, pin='', recovery_codes='')
    try:
        session.add(new_user)
        session.commit()
        return "User created successfully."
    except IntegrityError:
        session.rollback()
        return "Error: The email is already registered."

def login(email, password):
    user = session.query(User).filter_by(email=email, password=password).first()
    if user:
        token = generate_token(user.id)
        return "Login successful.", user, token
    else:
        return "Incorrect email or password.", None, None

def list_passwords(user_id):
    return session.query(Password).filter_by(user_id=user_id).all()

def create_password(service_name, user_email, password, user_id):
    new_password = Password(
        service_name=service_name,
        user_email=user_email,
        password=password,
        user_id=user_id
    )
    session.add(new_password)
    session.commit()
    return "Password created successfully."

def delete_password(password_id):
    password = session.query(Password).filter_by(id=password_id).first()
    if password:
        session.delete(password)
        session.commit()
        return "Password deleted successfully."
    return "Password not found."

def update_password(password_id, service_name, user_email, password):
    password_record = session.query(Password).filter_by(id=password_id).first()
    if password_record:
        password_record.service_name = service_name
        password_record.user_email = user_email
        password_record.password = password
        session.commit()
        return "Password updated successfully."
    return "Password not found."