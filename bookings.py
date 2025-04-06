import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyodbc
from database import get_connection
from datetime import datetime

class show_bookings:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление бронированием")
        self.root.geometry("900x500")
        self.root.configure(bg="#FFFFFF")

        self.load_icons()
        self.create_widgets()
        self.load_data()

    def load_icons(self):
        try:
            self.code_icon = ImageTk.PhotoImage(Image.open("assets/Бронирования/Код.png").resize((30, 30)))
            self.passenger_id_icon = ImageTk.PhotoImage(Image.open("assets/Бронирования/пассажир_id.png").resize((30, 30)))
            self.flight_id_icon = ImageTk.PhotoImage(Image.open("assets/Бронирования/рейс_id.png").resize((30, 30)))
            self.booking_date_icon = ImageTk.PhotoImage(Image.open("assets/Бронирования/дата_бронирования.png").resize((30, 30)))
            self.booking_status_icon = ImageTk.PhotoImage(Image.open("assets/Бронирования/статус_бронирования.png").resize((30, 30)))
            self.price_icon = ImageTk.PhotoImage(Image.open("assets/Бронирования/price.png").resize((30, 30)))
            self.booking_icon = ImageTk.PhotoImage(Image.open("assets/Бронирования/Flight-reservation02-min.jpg").resize((120, 120)))
            print("Иконки успешно загружены.")
        except Exception as e:
            print(f"Ошибка загрузки иконок: {e}")
            self.code_icon = self.passenger_id_icon = self.flight_id_icon = self.booking_date_icon = self.booking_status_icon = self.price_icon = self.booking_icon = None

    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", pady=(10, 0))

        title_label = ttk.Label(header_frame, text="Список бронирований")
        title_label.pack(side="left", padx=20, pady=10)

        refresh_btn = ttk.Button(header_frame, text="🔄 Обновить", command=self.load_data)
        refresh_btn.pack(side="right", padx=20, pady=10)

        manage_users_btn = ttk.Button(header_frame, text="Управление данными приложений", command=self.open_bookings_management)
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

        footer_label = ttk.Label(footer_frame, text="© 2025 Управление бронированиями")
        footer_label.pack(side="bottom", pady=5)

    def load_data(self):
        try:
            conn = get_connection()
            query = 'SELECT Код, пассажир_id, рейс_id, дата_бронирования, статус_бронирования, цена FROM Бронирования'
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            for row in data:
                self.add_booking_row(row)

            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные.\n{e}")

    def add_booking_row(self, row):
        booking_frame = ttk.Frame(self.canvas_frame, padding=10)
        booking_frame.pack(fill="x", pady=5, padx=10)

        icon_label = ttk.Label(booking_frame, image=self.booking_icon)
        icon_label.image = self.booking_icon
        icon_label.grid(row=0, column=0, padx=10, rowspan=6)

        self.add_field(booking_frame, f"Код: {row[0]}", self.code_icon, 1)
        self.add_field(booking_frame, f"Пассажир ID: {row[1]}", self.passenger_id_icon, 2)
        self.add_field(booking_frame, f"Рейс ID: {row[2]}", self.flight_id_icon, 3)
        self.add_field(booking_frame, f"Дата бронирования: {row[3]}", self.booking_date_icon, 4)
        self.add_field(booking_frame, f"Статус бронирования: {row[4]}", self.booking_status_icon, 5)
        self.add_field(booking_frame, f"Цена: {row[5]}", self.price_icon, 6)

        edit_btn = ttk.Button(booking_frame, text="Редактировать", command=lambda r=row: self.open_edit_window(r))
        edit_btn.grid(row=0, column=2, padx=10, pady=5)

    def add_field(self, frame, text, icon, row):
        field_frame = ttk.Frame(frame)
        field_frame.grid(row=row - 1, column=1, sticky="w")

        if icon:
            icon_label = ttk.Label(field_frame, image=icon)
            icon_label.image = icon
            icon_label.pack(side="left", padx=(0, 5))

        text_label = ttk.Label(field_frame, text=text)
        text_label.pack(side="left")

    def open_edit_window(self, row):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать бронирование")
        edit_window.geometry("400x300")
        edit_window.configure(bg="#FFFFFF")

        labels = ["Код", "Пассажир ID", "Рейс ID", "Дата бронирования", "Статус бронирования", "Цена"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(edit_window, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, row[i])

            self.entries[label_text] = entry

        update_btn = ttk.Button(edit_window, text="Обновить", command=lambda: self.update_Reservations(row[0], edit_window))
        update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_Reservations(self, seat_code, edit_window):
        new_seat_code = self.entries["Код"].get()
        new_passenger_id = self.entries["Пассажир ID"].get()
        new_flight_id = self.entries["Рейс ID"].get()
        new_booking_date = self.entries["Дата бронирования"].get()
        new_booking_status = self.entries["Статус бронирования"].get()
        new_price = self.entries["Цена"].get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Бронирования SET Код=?, пассажир_id=?, рейс_id=?, дата_бронирования=?, статус_бронирования=?, цена=? WHERE Код=?",
                (new_seat_code, new_passenger_id, new_flight_id, new_booking_date, new_booking_status, new_price, seat_code)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Данные места обновлены.")
            self.load_data()
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить данные: {e}")

    def load_table_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Код, пассажир_id, рейс_id, дата_бронирования, статус_бронирования, цена FROM Бронирования")
            bookings = cursor.fetchall()

            self.seat_table.delete(*self.seat_table.get_children())
            for booking in bookings:
                self.seat_table.insert("", "end", values=booking)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def open_bookings_management(self):
        management_window = tk.Toplevel(self.root)
        management_window.title("Управление бронированиями")
        management_window.geometry("800x500")
        management_window.configure(bg="#FFFFFF")

        title_label = ttk.Label(management_window, text="Управление бронированиями")
        title_label.pack(pady=10)

        fields_frame = ttk.Frame(management_window)
        fields_frame.pack(pady=10)

        labels = ["Код", "Пассажир ID", "Рейс ID", "Дата бронирования", "Статус бронирования", "Цена"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(fields_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(fields_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.entries[label_text] = entry

        btn_frame = ttk.Frame(management_window)
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Добавить", command=self.add_booking)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        columns = ("Код", "Пассажир ID", "Рейс ID", "Дата бронирования", "Статус бронирования", "Цена")
        self.seat_table = ttk.Treeview(management_window, columns=columns, show="headings", height=10)

        for col in columns:
            self.seat_table.heading(col, text=col)
            self.seat_table.column(col, width=140, anchor="center")

        self.seat_table.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_table_data()

    def add_booking(self):
        try:
            code = self.entries["Код"].get().strip()
            passenger_id = self.entries["Пассажир ID"].get().strip()
            flight_id = self.entries["Рейс ID"].get().strip()
            booking_date = self.entries["Дата бронирования"].get().strip()
            booking_status = self.entries["Статус бронирования"].get().strip()
            price = self.entries["Цена"].get().strip()

            if not code or not passenger_id or not flight_id or not booking_date or not booking_status or not price:
                messagebox.showwarning("Ошибка", "Все поля должны быть заполнены.")
                return

        except ValueError as e:
            messagebox.showwarning("Ошибка", f"Неверный формат данных: {e}")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Бронирования (Код, пассажир_id, рейс_id, дата_бронирования, статус_бронирования, цена) VALUES (?, ?, ?, ?, ?, ?)",
                (code, passenger_id, flight_id, booking_date, booking_status, price)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Бронирование добавлено.")
            self.load_table_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить бронирование: {e}")