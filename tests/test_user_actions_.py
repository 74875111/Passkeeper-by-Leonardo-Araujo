import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database.models import Base, User, Password
from authenticated.user_actions import create_user, login, list_passwords, create_password, delete_password, update_password

class TestUserActions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Crear una base de datos SQLite en memoria para pruebas
        cls.engine = create_engine('sqlite:///:memory:')
        cls.Session = scoped_session(sessionmaker(bind=cls.engine))
    
    def setUp(self):
        # Reiniciar la base de datos antes de cada prueba
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.session = self.Session()
        # Crear un usuario de prueba
        self.user = User(email='test@example.com', password='password123')
        self.session.add(self.user)
        self.session.commit()
    
    def tearDown(self):
        self.session.rollback()
        self.session.close()
        self.Session.remove()

    def test_create_user_success(self):
        # Asegurarse de que el usuario 'newuser@example.com' no existe antes de la prueba
        existing_user = self.session.query(User).filter_by(email='newuser@example.com').first()
        if existing_user:
            self.session.delete(existing_user)
            self.session.commit()
        
        result = create_user('newuser@example.com', 'password123')
        self.assertEqual(result, "User created successfully.")
    
    def test_create_user_duplicate_email(self):
        result = create_user('test@example.com', 'password123')
        self.assertEqual(result, "Error: The email is already registered.")
    
    def test_login_success(self):
        result, user, token = login('test@example.com', 'password123')
        self.assertEqual(result, "Login successful.")
    
    def test_login_failure(self):
        result, user, token = login('test@example.com', 'wrongpassword')
        self.assertEqual(result, "Incorrect email or password.")
    
    def test_create_password(self):
        user_id = self.user.id
        result = create_password('Service1', 'user1@example.com', 'pass1', user_id)
        self.assertEqual(result, "Password created successfully.")
    
    def test_delete_password_not_found(self):
        result = delete_password(999)
        self.assertEqual(result, "Password not found.")
    
    def test_update_password_not_found(self):
        result = update_password(999, 'Service1Updated', 'user1updated@example.com', 'pass1updated')
        self.assertEqual(result, "Password not found.")

if __name__ == '__main__':
    unittest.main()