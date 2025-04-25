from utils.storage import Storage
import bcrypt
import utils.logger as logger

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
    def register_user(
        username: str,
        password: str,
        name: str,
    ) -> None:
        """Registering function"""
        data = Storage.load_data()
        if username in data:
            logger.Error_logger.error("Username already exists.")
            return
        password_hash = AuthenticationManager.hash_pass(password=password)
        data[username] = {
            "user_info": {"name": name, "password": password_hash},
            "tasks": [],
        }
        Storage.save_data(data)

    @staticmethod
    def login_user(username: str, password: str) -> bool:
        """Login handler"""
        data = Storage.load_data()

        if username not in data:
            logger.Error_logger.error("Account not found Please register first!")
            return False

        password_hash = data[username]["user_info"]["password"]
        if AuthenticationManager.compare_pass(password, password_hash):
            return True
        return False