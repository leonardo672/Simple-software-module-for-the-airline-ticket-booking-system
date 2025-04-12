import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyodbc
from database import get_connection
from datetime import datetime

class show_aviary:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление Авиарейсы")
        self.root.geometry("900x500")
        self.root.configure(bg="#1c2b38")

        self.load_icons()
        self.create_widgets()
        self.load_data()

    def load_icons(self):
        try:
            self.code_icon = ImageTk.PhotoImage(Image.open("assets/Авиарейсы/Код.png").resize((20, 20)))
            self.airline_icon = ImageTk.PhotoImage(Image.open("assets/Авиарейсы/авиакомпания.png").resize((20, 20)))
            self.departure_icon = ImageTk.PhotoImage(Image.open("assets/Авиарейсы/отправление_из.png").resize((20, 20)))
            self.arrival_icon = ImageTk.PhotoImage(Image.open("assets/Авиарейсы/прибытие_в.png").resize((20, 20)))
            self.departure_time_icon = ImageTk.PhotoImage(Image.open("assets/Авиарейсы/время_отправления.png").resize((20, 20)))
            self.arrival_time_icon = ImageTk.PhotoImage(Image.open("assets/Авиарейсы/время_прибытия.png").resize((20, 20)))
            self.number_of_seats_icon = ImageTk.PhotoImage(Image.open("assets/Авиарейсы/количество_мест.png").resize((20, 20)))
            self.booking_icon = ImageTk.PhotoImage(Image.open("assets/User_Icon.jpeg").resize((100, 100)))
            print("Иконки успешно загружены.")
        except Exception as e:
            print(f"Ошибка загрузки иконок: {e}")
            self.code_icon = self.airline_icon = self.departure_icon = self.arrival_icon = self.departure_time_icon = self.arrival_time_icon = self.number_of_seats_icon = None

    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", pady=(10, 0))

        title_label = ttk.Label(header_frame, text="Список Авиарейсы")
        title_label.pack(side="left", padx=20, pady=10)

        refresh_btn = ttk.Button(header_frame, text="🔄 Обновить", command=self.load_data)
        refresh_btn.pack(side="right", padx=20, pady=10)

        manage_users_btn = ttk.Button(header_frame, text="Управление данными приложений", command=self.open_flights_management)
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

        footer_label = ttk.Label(footer_frame, text="© 2025 Управление данными приложений")
        footer_label.pack(side="bottom", pady=5)

    def load_data(self):
        try:
            conn = get_connection()
            query = 'SELECT Код, авиакомпания, отправление_из, прибытие_в, время_отправления, время_прибытия, количество_мест FROM Авиарейсы'
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

        if self.booking_icon:
            icon_label = ttk.Label(booking_frame, image=self.booking_icon)
            icon_label.image = self.booking_icon
            icon_label.grid(row=0, column=0, padx=10, rowspan=6)

        self.add_field(booking_frame, f"Код: {row[0]}", self.code_icon, 1)
        self.add_field(booking_frame, f"Авиакомпания: {row[1]}", self.airline_icon, 2)
        self.add_field(booking_frame, f"Отправление из: {row[2]}", self.departure_icon, 3)
        self.add_field(booking_frame, f"Прибытие в: {row[3]}", self.arrival_icon, 4)
        self.add_field(booking_frame, f"Время отправления: {row[4]}", self.departure_time_icon, 5)
        self.add_field(booking_frame, f"Время прибытия: {row[5]}", self.arrival_time_icon, 6)
        self.add_field(booking_frame, f"Количество мест: {row[6]}", self.number_of_seats_icon, 7)

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
        edit_window.title("Редактировать Авиарейс")
        edit_window.geometry("400x300")
        edit_window.configure(bg="#FFFFFF")

        labels = ["Код", "Авиакомпания", "Отправление из", "Прибытие в", "Время отправления", "Время прибытия", "Количество мест"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(edit_window, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, row[i])

            self.entries[label_text] = entry

        update_btn = ttk.Button(edit_window, text="Обновить", command=lambda: self.update_Flights(row[0], edit_window))
        update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_Flights(self, flight_code, edit_window):
        new_flight_code = self.entries["Код"].get()
        new_airline = self.entries["Авиакомпания"].get()
        new_departure_from = self.entries["Отправление из"].get()
        new_arrival_to = self.entries["Прибытие в"].get()
        new_departure_time = self.entries["Время отправления"].get()
        new_arrival_time = self.entries["Время прибытия"].get()
        new_seat_count = self.entries["Количество мест"].get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Авиарейсы SET Код=?, авиакомпания=?, отправление_из=?, прибытие_в=?, время_отправления=?, время_прибытия=?, количество_мест=? WHERE Код=?",
                (new_flight_code, new_airline, new_departure_from, new_arrival_to, new_departure_time, new_arrival_time, new_seat_count, flight_code)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Данные авиарейса обновлены.")
            self.load_data()
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить данные: {e}")

    def load_table_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Код, авиакомпания, отправление_из, прибытие_в, время_отправления, время_прибытия, количество_мест FROM Авиарейсы")
            bookings = cursor.fetchall()

            self.seat_table.delete(*self.seat_table.get_children())
            for booking in bookings:
                self.seat_table.insert("", "end", values=booking)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def add_flight(self):
        try:
            code = int(self.entries["Код"].get())
            airline = self.entries["Авиакомпания"].get().strip()
            departure_from = self.entries["Отправление из"].get().strip()
            arrival_to = self.entries["Прибытие в"].get().strip()
            seats_available = int(self.entries["Количество мест"].get())
            departure_time = self.entries["Время отправления"].get().strip()
            arrival_time = self.entries["Время прибытия"].get().strip()

            try:
                departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
                arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат даты! Используйте формат: YYYY-MM-DD HH:MM:SS")
                return

        except ValueError as e:
            messagebox.showwarning("Ошибка", f"Неверный формат данных: {e}")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Авиарейсы (Код, авиакомпания, отправление_из, прибытие_в, время_отправления, время_прибытия, количество_мест) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (code, airline, departure_from, arrival_to, departure_time, arrival_time, seats_available)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Авиарейс добавлен.")
            self.load_table_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить авиарейс: {e}")

    def open_flights_management(self):
        management_window = tk.Toplevel(self.root)
        management_window.title("Управление авиарейсами")
        management_window.geometry("1000x600")
        management_window.configure(bg="#FFFFFF")

        title_label = ttk.Label(management_window, text="Управление авиарейсами")
        title_label.pack(pady=10)

        fields_frame = ttk.Frame(management_window)
        fields_frame.pack(pady=10)

        labels = ["Код", "Авиакомпания", "Отправление из", "Прибытие в", "Время отправления", "Время прибытия", "Количество мест"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(fields_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(fields_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.entries[label_text] = entry

        btn_frame = ttk.Frame(management_window)
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Добавить", command=self.add_flight)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        columns = ("Код", "Авиакомпания", "Отправление из", "Прибытие в", "Время отправления", "Время прибытия", "Количество мест")
        self.seat_table = ttk.Treeview(management_window, columns=columns, show="headings", height=10)

        for col in columns:
            self.seat_table.heading(col, text=col)
            self.seat_table.column(col, width=140, anchor="center")

        self.seat_table.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_table_data()