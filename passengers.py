import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyodbc
from database import get_connection
from datetime import datetime

class show_passengers:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление Пассажиры")
        self.root.geometry("900x500")

        self.load_icons()
        self.create_widgets()
        self.load_data()

    def load_icons(self):
        try:
            self.code_icon = ImageTk.PhotoImage(Image.open("assets/Пассажиры/Код.png").resize((30, 30)))
            self.first_name_icon = ImageTk.PhotoImage(Image.open("assets/Пассажиры/имя.png").resize((30, 30)))
            self.last_name_icon = ImageTk.PhotoImage(Image.open("assets/Пассажиры/фамилия.png").resize((30, 30)))
            self.birthdate_icon = ImageTk.PhotoImage(Image.open("assets/Пассажиры/дата_рождения.png").resize((30, 30)))
            self.passport_number_icon = ImageTk.PhotoImage(Image.open("assets/Пассажиры/паспорт_номер.png").resize((30, 30)))
            self.email_icon = ImageTk.PhotoImage(Image.open("assets/Пассажиры/email.png").resize((30, 30)))
            self.phone_icon = ImageTk.PhotoImage(Image.open("assets/Пассажиры/телефон.png").resize((30, 30)))
            self.booking_icon = ImageTk.PhotoImage(Image.open("assets/Пассажиры/passenger-icon-11.png").resize((100, 100)))
            self.user_icon = ImageTk.PhotoImage(Image.open("assets/User_Icon.jpeg").resize((40, 40)))
            print("Иконки успешно загружены.")
        except Exception as e:
            print(f"Ошибка загрузки иконок: {e}")
            self.code_icon = self.first_name_icon = self.last_name_icon = self.birthdate_icon = self.passport_number_icon = self.email_icon = self.phone_icon = self.booking_icon = self.user_icon = None

    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", pady=(10, 0))

        title_label = ttk.Label(header_frame, text="Список Пассажиры")
        title_label.pack(side="left", padx=20, pady=10)

        refresh_btn = ttk.Button(header_frame, text="🔄 Обновить", command=self.load_data)
        refresh_btn.pack(side="right", padx=20, pady=10)

        manage_users_btn = ttk.Button(header_frame, text="Управление данными приложений", command=self.open_passenger_management)
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

        footer_label = ttk.Label(footer_frame, text="© 2025 Управление Пассажиры")
        footer_label.pack(side="bottom", pady=5)

    def load_data(self):
        try:
            conn = get_connection()
            query = 'SELECT Код, имя, фамилия, дата_рождения, паспорт_номер, email, телефон FROM Пассажиры'
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            for row in data:
                self.add_passenger_row(row)

            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные.\n{e}")

    def add_passenger_row(self, row):
        passenger_frame = ttk.Frame(self.canvas_frame, padding=10)
        passenger_frame.pack(fill="x", pady=5, padx=10)

        icon_label = ttk.Label(passenger_frame, image=self.booking_icon)
        icon_label.image = self.booking_icon
        icon_label.grid(row=0, column=0, padx=10, rowspan=7)

        self.add_field(passenger_frame, f"Код: {row[0]}", self.code_icon, 1)
        self.add_field(passenger_frame, f"Имя: {row[1]}", self.first_name_icon, 2)
        self.add_field(passenger_frame, f"Фамилия: {row[2]}", self.last_name_icon, 3)
        self.add_field(passenger_frame, f"Дата рождения: {row[3]}", self.birthdate_icon, 4)
        self.add_field(passenger_frame, f"Паспорт номер: {row[4]}", self.passport_number_icon, 5)
        self.add_field(passenger_frame, f"Email: {row[5]}", self.email_icon, 6)
        self.add_field(passenger_frame, f"Телефон: {row[6]}", self.phone_icon, 7)

        edit_btn = ttk.Button(passenger_frame, text="Редактировать", command=lambda r=row: self.open_edit_window(r))
        edit_btn.grid(row=0, column=2, padx=10, pady=5)

    def open_edit_window(self, row):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать Пассажира")
        edit_window.geometry("400x350")
        edit_window.configure(bg="#FFFFFF")

        labels = ["Код", "Имя", "Фамилия", "Дата рождения", "Паспорт номер", "Email", "Телефон"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(edit_window, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, row[i])

            self.entries[label_text] = entry

        update_btn = ttk.Button(edit_window, text="Обновить", command=lambda: self.update_Passenger(row[0], edit_window))
        update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_Passenger(self, passenger_code, edit_window):
        new_code = self.entries["Код"].get()
        new_first_name = self.entries["Имя"].get()
        new_last_name = self.entries["Фамилия"].get()
        new_birth_date = self.entries["Дата рождения"].get()
        new_passport_number = self.entries["Паспорт номер"].get()
        new_email = self.entries["Email"].get()
        new_phone = self.entries["Телефон"].get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Пассажиры SET Код=?, имя=?, фамилия=?, дата_рождения=?, паспорт_номер=?, email=?, телефон=? WHERE Код=?",
                (new_code, new_first_name, new_last_name, new_birth_date, new_passport_number, new_email, new_phone, passenger_code)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Данные пассажира обновлены.")
            self.load_data()
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить данные: {e}")

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
            cursor.execute("SELECT Код, имя, фамилия, дата_рождения, паспорт_номер, email, телефон FROM Пассажиры")
            bookings = cursor.fetchall()

            self.seat_table.delete(*self.seat_table.get_children())
            for booking in bookings:
                self.seat_table.insert("", "end", values=booking)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def add_passenger(self):
        try:
            new_code = self.entries["Код"].get().strip()
            first_name = self.entries["Имя"].get().strip()
            last_name = self.entries["Фамилия"].get().strip()
            birth_date = self.entries["Дата рождения"].get().strip()
            passport_number = self.entries["Паспорт номер"].get().strip()
            email = self.entries["Email"].get().strip()
            phone = self.entries["Телефон"].get().strip()

            if not new_code or not first_name or not last_name or not birth_date or not passport_number or not email or not phone:
                messagebox.showwarning("Ошибка", "Все поля должны быть заполнены.")
                return

        except ValueError as e:
            messagebox.showwarning("Ошибка", f"Неверный формат данных: {e}")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Пассажиры (Код, имя, фамилия, дата_рождения, паспорт_номер, email, телефон) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (new_code, first_name, last_name, birth_date, passport_number, email, phone)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Пассажир добавлен.")
            self.load_table_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить пассажира: {e}")

    def open_passenger_management(self):
        management_window = tk.Toplevel(self.root)
        management_window.title("Управление пассажирами")
        management_window.geometry("1000x600")
        management_window.configure(bg="#FFFFFF")

        title_label = ttk.Label(management_window, text="Управление пассажирами")
        title_label.pack(pady=10)

        fields_frame = ttk.Frame(management_window)
        fields_frame.pack(pady=10)

        labels = ["Код", "Имя", "Фамилия", "Дата рождения", "Паспорт номер", "Email", "Телефон"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(fields_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(fields_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.entries[label_text] = entry

        btn_frame = ttk.Frame(management_window)
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Добавить", command=self.add_passenger)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        columns = ("Код", "Имя", "Фамилия", "Дата рождения", "Паспорт номер", "Email", "Телефон")
        self.seat_table = ttk.Treeview(management_window, columns=columns, show="headings", height=10)

        for col in columns:
            self.seat_table.heading(col, text=col)
            self.seat_table.column(col, width=140, anchor="center")

        self.seat_table.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_table_data()