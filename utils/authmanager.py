from utils.storage import Storage
import bcrypt
import utils.logger as logger
from cryptography.fernet import Fernet, InvalidToken
import base64
import hashlib

min_: int = 6


class AuthenticationManager:
    def __init__(self):
        pass

    @staticmethod
    def hash_pass(password: str) -> str:
        try:
            if (
                not password or len(password) < min_
            ):  # You can set a minimum password length
                return
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            return hashed.decode("utf-8")

        except UnicodeDecodeError:
            logger.Error_logger.error("Error while trying to decode the psw")

    @staticmethod
    def compare_pass(password: str, hashed_password: str) -> bool:
        """This is for comparing a (psw <-> hash)"""
        try:
            if not hashed_password:
                logger.Error_logger.error("Invalid hash provided for comparison")
                return False
            return bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            )

        except ValueError:
            logger.Error_logger.error("Invalid hash")
            return False

    @staticmethod
    def register_user(username: str, password: str, name: str) -> None:
        """Registering function"""
        # data = Storage.load_data()
        # if username in data:
        #     logger.Error_logger.error("Username already exists.")
        #     return
        # password_hash = AuthenticationManager.hash_pass(password=password)
        # data[username] = {
        #     "user_info": {"name": name, "password": password_hash},
        #     "tasks": [],
        # }
        # Storage.save_data(data)

    @staticmethod
    def login_user(username: str, password: str) -> bool:
        """Login handler"""
        data = Storage.load_data(username)

        if username not in data["username"]:
            logger.Error_logger.error(f"Account {username} not found Please register first!")
            return False

        password_hash = data["password_hash"]
        if AuthenticationManager.compare_pass(password, password_hash):
            return True
        return False
    
    @staticmethod
    def _generate_key(key: str) -> bytes:
        """Generate a Fernet key based on the provided key"""
        digest = hashlib.sha256(key.encode()).digest()
        return base64.urlsafe_b64encode(digest)

    @staticmethod
    def encrypt_data(data: str | dict | list, key: str) -> str:
        """Encrypt given data using a key"""
        if isinstance(data, (dict, list)):
            import json
            data = json.dumps(data)

        fernet_key = AuthenticationManager._generate_key(key)
        fernet = Fernet(fernet_key)
        encrypted = fernet.encrypt(data.encode())
        return encrypted.decode()

    @staticmethod
    def decrypt_data(data: str, key: str):
        """Decrypt given data using a key"""
        try :
            fernet_key = AuthenticationManager._generate_key(key)
            fernet = Fernet(fernet_key)
            decrypted = fernet.decrypt(data.encode()).decode()
            return decrypted
        except (InvalidToken, base64.binascii.Error):
            # Decryption failed (data was not encrypted properly)
            print("[Warning] Data is not encrypted or key is invalid.")
            return None