import sys
import hashlib
import pyodbc
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox,
    QDesktopWidget, QDateEdit, QStackedWidget
)
from PyQt5.QtCore import pyqtSignal, QDate

DATABASE_CONNECTION_STRING = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=D:\laravel\Projects\Tamam\pythonProject\База_данных.accdb;'
)

def create_database_connection():
    try:
        return pyodbc.connect(DATABASE_CONNECTION_STRING)
    except pyodbc.Error as e:
        QMessageBox.critical(None, "Database Error", f"Failed to connect to the database: {e}")
        raise

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(name, email):
    try:
        conn = create_database_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Пользователи WHERE Имя = ? OR Электронная_почта = ?", (name, email))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    except pyodbc.Error as e:
        QMessageBox.critical(None, "Database Error", f"Failed to check user existence: {e}")
        return False

def register_user(name, surname, email, password, dob):
    try:
        conn = create_database_connection()
        cursor = conn.cursor()
        password_hash = hash_password(password)
        dob_str = dob.toString("yyyy-MM-dd")

        cursor.execute(
            "INSERT INTO Пользователи (Имя, Фамилия, Электронная_почта, Пароль, Дата_рождения) VALUES (?, ?, ?, ?, ?)",
            (name, surname, email, password_hash, dob_str)
        )
        conn.commit()
        conn.close()
        return True
    except pyodbc.Error as e:
        QMessageBox.critical(None, "Database Error", f"Failed to register user: {e}")
        return False

def authenticate_user(name, email, password):
    try:
        conn = create_database_connection()
        cursor = conn.cursor()
        password_hash = hash_password(password)

        cursor.execute(
            "SELECT * FROM Пользователи WHERE (Имя = ? OR Электронная_почта = ?) AND Пароль = ?",
            (name, email, password_hash))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    except pyodbc.Error as e:
        QMessageBox.critical(None, "Database Error", f"Failed to authenticate user: {e}")
        return False

class LoginForm(QWidget):
    login_successful = pyqtSignal()

    def __init__(self, switch_to_register_callback):
        super().__init__()
        self.switch_to_register_callback = switch_to_register_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Бронирования Авиабилетов Приложение")
        self.setFixedSize(500, 400)
        self.center_window()
        self.setStyleSheet(self.get_stylesheet())

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        form_layout.addRow("Имя:", self.name_input)

        self.email_input = QLineEdit()
        form_layout.addRow("Электронная почта:", self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Пароль:", self.password_input)

        layout.addLayout(form_layout)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.switch_label = QLabel("Еще не зарегистрированы? Нажмите здесь.")
        self.switch_label.setObjectName("link")
        self.switch_label.mousePressEvent = self.switch_to_register_callback
        layout.addWidget(self.switch_label)

        self.setLayout(layout)

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #ffffff;
                font-family: 'Georgia', serif;
                color: #000000;
                padding: 20px;
            }

            QLabel {
                font-size: 18px;
                font-weight: 500;
                color: #000000;
                margin-bottom: 10px;
                background: none;
            }

            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #cccccc;
                background-color: #ffffff;
                font-size: 16px;
                color: #000000;
                transition: border 0.3s ease, box-shadow 0.3s ease;
            }

            QLineEdit:focus {
                border: 1px solid #0078D7;
                box-shadow: 0 0 8px rgba(0, 120, 215, 0.5);
            }

            QLineEdit::placeholder {
                color: #aab7c1;
            }

            QPushButton {
                background-color: #0078D7;
                color: white;
                font-size: 18px;
                font-weight: 600;
                border-radius: 8px;
                padding: 12px;
                border: none;
                margin-top: 20px;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.2s ease-in-out;
            }

            QPushButton:hover {
                background-color: #005bb5;
                transform: translateY(-2px);
            }

            QPushButton:pressed {
                background-color: #004a9c;
                transform: translateY(2px);
            }

            QLabel#link {
                color: #0078D7;
                font-weight: 600;
                text-decoration: none;
                cursor: pointer;
                transition: color 0.2s ease;
            }

            QLabel#link:hover {
                color: #005bb5;
            }
        """

    def login(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not name and not email:
            QMessageBox.warning(self, "Ошибка", "Введите имя пользователя или email!")
            return

        if authenticate_user(name, email, password):
            QMessageBox.information(self, "Успех", f"Добро пожаловать, {name}!")
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные учетные данные!")

class RegistrationForm(QWidget):
    def __init__(self, switch_to_login_callback):
        super().__init__()
        self.switch_to_login_callback = switch_to_login_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Бронирования Авиабилетов Приложение")
        self.setFixedSize(550, 700)
        self.center_window()
        self.setStyleSheet(self.get_stylesheet())

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        form_layout.addRow("Имя:", self.name_input)

        self.surname_input = QLineEdit()
        form_layout.addRow("Фамилия:", self.surname_input)

        self.email_input = QLineEdit()
        form_layout.addRow("Электронная почта:", self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Пароль:", self.password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Подтверждение пароля:", self.confirm_password_input)

        self.dob_input = QDateEdit()
        self.dob_input.setDate(QDate.currentDate())
        self.dob_input.setCalendarPopup(True)
        form_layout.addRow("Дата рождения:", self.dob_input)

        layout.addLayout(form_layout)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.switch_label = QLabel("Уже зарегистрированы? Нажмите здесь.")
        self.switch_label.setObjectName("link")
        self.switch_label.mousePressEvent = self.switch_to_login_callback
        layout.addWidget(self.switch_label)

        self.setLayout(layout)

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #ffffff;
                font-family: 'Georgia', serif;
                color: #000000;
                padding: 20px;
            }

            QLabel {
                font-size: 18px;
                font-weight: 500;
                color: #000000;
                margin-bottom: 10px;
                background: none;
            }

            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #cccccc;
                background-color: #ffffff;
                font-size: 16px;
                color: #000000;
                transition: border 0.3s ease, box-shadow 0.3s ease;
            }

            QLineEdit:focus {
                border: 1px solid #0078D7;
                box-shadow: 0 0 8px rgba(0, 120, 215, 0.5);
            }

            QLineEdit::placeholder {
                color: #aab7c1;
            }

            QPushButton {
                background-color: #0078D7;
                color: white;
                font-size: 18px;
                font-weight: 600;
                border-radius: 8px;
                padding: 12px;
                border: none;
                margin-top: 20px;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.2s ease-in-out;
            }

            QPushButton:hover {
                background-color: #005bb5;
                transform: translateY(-2px);
            }

            QPushButton:pressed {
                background-color: #004a9c;
                transform: translateY(2px);
            }

            QDateEdit {
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #cccccc;
                background-color: #ffffff;
                font-size: 16px;
                color: #000000;
                transition: border 0.3s ease, box-shadow 0.3s ease;
            }

            QDateEdit:focus {
                border: 1px solid #0078D7;
                box-shadow: 0 0 8px rgba(0, 120, 215, 0.5);
            }

            QLabel#link {
                color: #0078D7;
                font-weight: 600;
                text-decoration: none;
                cursor: pointer;
                transition: color 0.2s ease;
            }

            QLabel#link:hover {
                color: #005bb5;
            }
        """

    def register(self):
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        dob = self.dob_input.date()

        if not all([name, surname, email, password, confirm_password]):
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
            return

        if register_user(name, surname, email, password, dob):
            QMessageBox.information(self, "Успех", f"Пользователь {name} зарегистрирован!")
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Ошибка", "Ошибка регистрации или пользователь уже существует!")

    def clear_fields(self):
        self.name_input.clear()
        self.surname_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.dob_input.setDate(QDate.currentDate())

class UserForm(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Бронирования Авиабилетов Приложение")
        self.center_window()

        self.stacked_widget = QStackedWidget()
        self.login_form = LoginForm(self.switch_to_registration)
        self.registration_form = RegistrationForm(self.switch_to_login)
        self.stacked_widget.addWidget(self.login_form)
        self.stacked_widget.addWidget(self.registration_form)

        self.login_form.login_successful.connect(self.login_successful)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())

    def switch_to_registration(self, event):
        self.stacked_widget.setCurrentIndex(1)

    def switch_to_login(self, event):
        self.stacked_widget.setCurrentIndex(0)