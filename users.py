import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyodbc
from database import get_connection

class UsersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление пользователями")
        self.root.geometry("900x500")

        self.load_icons()
        self.create_widgets()
        self.load_data()

    def load_icons(self):
        try:
            self.code_icon = ImageTk.PhotoImage(Image.open("assets/Пользователи/Код.png").resize((30, 30)))
            self.first_name_icon = ImageTk.PhotoImage(Image.open("assets/Пользователи/Имя.png").resize((30, 30)))
            self.last_name_icon = ImageTk.PhotoImage(Image.open("assets/Пользователи/Фамилия.png").resize((30, 30)))
            self.email_icon = ImageTk.PhotoImage(Image.open("assets/Пользователи/Электронная_почта.png").resize((30, 30)))
            self.birthdate_icon = ImageTk.PhotoImage(Image.open("assets/Пользователи/Дата_рождения.png").resize((30, 30)))
            self.user_icon = ImageTk.PhotoImage(Image.open("assets/User_Icon.jpeg").resize((100, 100)))
            print("Иконки успешно загружены.")
        except Exception as e:
            print(f"Ошибка загрузки иконок: {e}")
            self.code_icon = self.first_name_icon = self.last_name_icon = self.email_icon = self.birthdate_icon = self.user_icon = None

    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", pady=(10, 0))

        title_label = ttk.Label(header_frame, text="Список пользователей")
        title_label.pack(side="left", padx=20, pady=10)

        refresh_btn = ttk.Button(header_frame, text="🔄 Обновить", command=self.load_data)
        refresh_btn.pack(side="right", padx=20, pady=10)

        manage_users_btn = ttk.Button(header_frame, text="Управление данными приложений", command=self.open_user_management)
        manage_users_btn.pack(side="right", padx=20, pady=10)

        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.canvas = tk.Canvas(self.container, bg="#FFFFFF", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        footer_frame = ttk.Frame(self.root, height=30)
        footer_frame.pack(side="bottom", fill="x", pady=(0, 0))

        footer_label = ttk.Label(footer_frame, text="© 2025 Управление пользователями")
        footer_label.pack(side="bottom", pady=5)

    def load_data(self):
        try:
            conn = get_connection()
            query = 'SELECT Код, Имя, Фамилия, Электронная_почта, Дата_рождения FROM Пользователи'
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            for row in data:
                self.add_user_row(row)

            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные.\n{e}")

    def add_user_row(self, row):
        user_frame = ttk.Frame(self.canvas_frame, padding=10)
        user_frame.pack(fill="x", pady=5, padx=10)

        icon_label = ttk.Label(user_frame, image=self.user_icon)
        icon_label.image = self.user_icon
        icon_label.grid(row=0, column=0, padx=10, rowspan=6)

        self.add_field(user_frame, f"Код: {row[0]}", self.code_icon, 1)
        self.add_field(user_frame, f"Имя: {row[1]}", self.first_name_icon, 2)
        self.add_field(user_frame, f"Фамилия: {row[2]}", self.last_name_icon, 3)
        self.add_field(user_frame, f"Электронная почта: {row[3]}", self.email_icon, 4)
        self.add_field(user_frame, f"Дата рождения: {row[4]}", self.birthdate_icon, 5)

    def add_field(self, frame, text, icon, row):
        field_frame = ttk.Frame(frame)
        field_frame.grid(row=row - 1, column=1, sticky="w")

        if icon:
            icon_label = ttk.Label(field_frame, image=icon)
            icon_label.image = icon
            icon_label.pack(side="left", padx=(0, 5))

        text_label = ttk.Label(field_frame, text=text)
        text_label.pack(side="left")

    def load_table_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Код, Имя, Фамилия, Электронная_почта, Пароль, Дата_рождения FROM Пользователи")
            users = cursor.fetchall()

            self.user_table.delete(*self.user_table.get_children())
            for user in users:
                self.user_table.insert("", "end", values=user)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def add_user(self):
        code = self.entries["Код"].get()
        name = self.entries["Имя"].get()
        surname = self.entries["Фамилия"].get()
        email = self.entries["Электронная почта"].get()
        password = self.entries["Пароль"].get()
        birthdate = self.entries["Дата рождения"].get()

        if not (code and name and surname and email and password and birthdate):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            from datetime import datetime
            birthdate = datetime.strptime(birthdate, "%Y-%m-%d %H:%M:%S").date()

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Пользователи (Код, Имя, Фамилия, Электронная_почта, Пароль, Дата_рождения) VALUES (?, ?, ?, ?, ?, ?)",
                (code, name, surname, email, password, birthdate)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Пользователь добавлен.")
            self.load_table_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить пользователя: {e}")

    def open_user_management(self):
        management_window = tk.Toplevel(self.root)
        management_window.title("Управление пользователями")
        management_window.geometry("700x500")
        management_window.configure(bg="#FFFFFF")

        title_label = ttk.Label(management_window, text="Управление пользователями")
        title_label.pack(pady=10)

        fields_frame = ttk.Frame(management_window)
        fields_frame.pack(pady=10)

        labels = ["Код", "Имя", "Фамилия", "Электронная почта", "Пароль", "Дата рождения"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(fields_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(fields_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.entries[label_text] = entry

        btn_frame = ttk.Frame(management_window)
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Добавить", command=self.add_user)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        columns = ("Код", "Имя", "Фамилия", "Электронная почта", "Пароль", "Дата рождения")
        self.user_table = ttk.Treeview(management_window, columns=columns, show="headings", height=10)

        for col in columns:
            self.user_table.heading(col, text=col)
            self.user_table.column(col, width=140, anchor="center")

        self.user_table.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_table_data()