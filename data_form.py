from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from database import update_data, insert_data


class DataFormBase(QDialog):
    def __init__(self, table_name, columns, existing_data=None, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.columns = columns
        self.existing_data = existing_data
        self.setWindowTitle(f'Редактирование: {table_name}')
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("background-color: #1B2B5E; color: #D6E4FF;")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(12)

        # Header
        self.header = QLabel(f'Редактирование: {table_name}')
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont("Arial", 14, QFont.Bold))
        self.header.setStyleSheet("color: #8DA2E2; padding-bottom: 10px;")
        self.layout.addWidget(self.header)

        # Input Fields
        self.inputs = {}
        input_style = """
        QLineEdit {
            background-color: #3A5BA7;
            border: 2px solid #5778C1;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
            color: white;
        }
        QLineEdit:focus {
            border: 2px solid #8DA2E2;
        }
        """
        for idx, column in enumerate(columns):
            label = QLabel(f'{column}:')
            label.setFont(QFont("Arial", 12, QFont.Bold))
            label.setStyleSheet("color: #8DA2E2; padding: 4px;")

            input_field = QLineEdit(self)
            input_field.setFont(QFont("Arial", 12))
            input_field.setStyleSheet(input_style)
            if existing_data:
                input_field.setText(str(existing_data[idx]))  # Set existing data if available

            self.layout.addWidget(label)
            self.layout.addWidget(input_field)
            self.inputs[column] = input_field

        # Save Button
        self.saveButton = QPushButton('💾 Сохранить', self)
        self.saveButton.setFont(QFont("Arial", 12, QFont.Bold))
        self.saveButton.setStyleSheet("""
        QPushButton {
            background-color: #5778C1;
            color: white;
            padding: 12px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #8DA2E2;
        }
        """)
        self.saveButton.clicked.connect(self.save_data)
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)

    def save_data(self):
        values = [self.inputs[col].text() for col in self.columns]
        raise NotImplementedError("This method should be implemented by subclasses.")


class DataForm_Update(DataFormBase):
    def save_data(self):
        values = [self.inputs[col].text() for col in self.columns]
        try:
            update_data(self.table_name, self.columns, values, self.columns[0],
                        self.existing_data[0])  # Use the first column as key
            QMessageBox.information(self, 'Успех', 'Запись успешно обновлена!')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))


class DataForm_Insert(DataFormBase):
    def save_data(self):
        values = [self.inputs[col].text() for col in self.columns]
        try:
            insert_data(self.table_name, self.columns, values)
            QMessageBox.information(self, 'Успех', 'Запись успешно добавлена!')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))

