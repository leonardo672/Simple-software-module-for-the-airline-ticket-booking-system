import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from aviary import show_aviary
from bookings import show_bookings
from seats import show_seats
from payments import show_payments
from passengers import show_passengers
from airport_links import show_airport_links
from users import UsersApp
from PyQt5.QtWidgets import QApplication
from UserAuth import UserForm

def open_table_window(root, table_function):
    new_window = tk.Toplevel(root)
    new_window.title("Таблица")
    new_window.geometry("800x600")
    new_window.config(bg="#ffffff")
    table_function(new_window)

def main():
    root = tk.Tk()
    root.title("Система бронирования авиабилетов")
    root.geometry("1200x800")
    root.config(bg="#ffffff")

    try:
        background_image = Image.open("assets/Main_Interface.png")
        background_image = background_image.resize((1200, 800))
        background_photo = ImageTk.PhotoImage(background_image)
    except Exception as e:
        print(f"Error loading background image: {e}")
        background_photo = None

    if background_photo:
        background_label = tk.Label(root, image=background_photo, bg="#ffffff")
        background_label.place(x=0, y=70, relwidth=1, relheight=1)
        background_label.image = background_photo

    title_label = tk.Label(
        root,
        text="Система бронирования авиабилетов",
        font=("Helvetica", 24, "bold"),
        fg="#000000",
        bg="#ffffff",
        pady=20,
    )
    title_label.pack(fill="x")

    buttons_frame = ttk.Frame(root, padding="15")
    buttons_frame.pack(padx=10, pady=10, fill="x")

    tables = {
        "Авиарейсы": lambda: open_table_window(root, show_aviary),
        "Бронирование": lambda: open_table_window(root, show_bookings),
        "Места в самолете": lambda: open_table_window(root, show_seats),
        "Оплаты": lambda: open_table_window(root, show_payments),
        "Пассажиры": lambda: open_table_window(root, show_passengers),
        "Связь аэропортов и рейсов": lambda: open_table_window(root, show_airport_links),
        "Пользователи": lambda: open_table_window(root, lambda win: UsersApp(win)),
    }

    max_columns = 4
    row, col = 0, 0

    for name, func in tables.items():
        btn = ttk.Button(buttons_frame, text=name, command=func, style="TButton")
        btn.grid(row=row, column=col, padx=8, pady=10, sticky="nsew")
        col += 1
        if col >= max_columns:
            col = 0
            row += 1

    for i in range(max_columns):
        buttons_frame.grid_columnconfigure(i, weight=1)
    for r in range(row + 1):
        buttons_frame.grid_rowconfigure(r, weight=1)

    root.mainloop()

class GUIApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(self.get_stylesheet())
        self.user_form = UserForm()
        self.user_form.login_successful.connect(self.on_login_successful)
        self.user_form.show()

    def on_login_successful(self):
        self.user_form.close()
        main()

    @staticmethod
    def get_stylesheet():
        return """
        QWidget { font-size: 14px; font-family: 'Segoe UI', Arial, sans-serif; background-color: #ffffff; color: #000000; }
        QPushButton { background-color: #0078D7; color: #ffffff; border-radius: 8px; padding: 10px; font-size: 14px; font-weight: bold; border: 1px solid #005bb5; }
        QPushButton:hover { background-color: #005bb5; }
        QPushButton:pressed { background-color: #004a9c; border: 2px solid #ffffff; }
        QLineEdit { background-color: #ffffff; color: #000000; border-radius: 5px; padding: 5px; border: 1px solid #cccccc; }
        QLineEdit:focus { border: 2px solid #0078D7; }
        QLabel { font-size: 16px; font-weight: bold; color: #000000; }
        QComboBox { background-color: #ffffff; color: #000000; border-radius: 5px; padding: 5px; border: 1px solid #cccccc; }
        QComboBox:hover { background-color: #f0f0f0; }
        QTableWidget { background-color: #ffffff; border-radius: 5px; gridline-color: #cccccc; color: #000000; }
        QTableWidget::item:selected { background-color: #0078D7; color: #ffffff; }
        QScrollBar:vertical { background: #f0f0f0; width: 10px; }
        QScrollBar::handle:vertical { background: #cccccc; min-height: 20px; border-radius: 4px; }
        QScrollBar::handle:vertical:hover { background: #999999; }
        """

if __name__ == "__main__":
    gui_app = GUIApp()
    gui_app.app.exec_()