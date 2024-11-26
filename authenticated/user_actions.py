import os
from sqlalchemy.orm import sessionmaker
from database.models import User, Password, engine
from sqlalchemy.exc import IntegrityError
from session_manager import generate_token
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave AES desde la variable de entorno
AES_KEY = os.getenv('AES_KEY')
fernet = Fernet(AES_KEY)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

def create_user(email, password):
    encrypted_password = fernet.encrypt(password.encode()).decode()
    new_user = User(email=email, password=encrypted_password, pin='', recovery_codes='')
    try:
        session.add(new_user)
        session.commit()
        return "User created successfully."
    except IntegrityError:
        session.rollback()
        return "Error: The email is already registered."

def login(email, password):
    user = session.query(User).filter_by(email=email).first()
    if user:
        try:
            decrypted_password = fernet.decrypt(user.password.encode()).decode()
            if decrypted_password == password:
                token = generate_token(user.id)
                return "Login successful.", user, token
            else:
                return "Incorrect email or password.", None, None
        except InvalidToken:
            return "Incorrect email or password.", None, None
    else:
        return "Incorrect email or password.", None, None

def list_passwords(user_id):
    passwords = session.query(Password).filter_by(user_id=user_id).all()
    return passwords

def create_password(service_name, user_email, password, user_id):
    encrypted_password = fernet.encrypt(password.encode()).decode()
    new_password = Password(
        service_name=service_name,
        user_email=user_email,
        password=encrypted_password,
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
        encrypted_password = fernet.encrypt(password.encode()).decode()
        password_record.service_name = service_name
        password_record.user_email = user_email
        password_record.password = encrypted_password
        session.commit()
        return "Password updated successfully."
    return "Password not found."

def get_password(password_id):
    password_record = session.query(Password).filter_by(id=password_id).first()
    if password_record:
        try:
            decrypted_password = fernet.decrypt(password_record.password.encode()).decode()
            password_record.password = decrypted_password
        except InvalidToken:
            password_record.password = "Invalid token"
        return password_record
    return None