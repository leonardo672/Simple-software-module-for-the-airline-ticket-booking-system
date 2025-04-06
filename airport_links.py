import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyodbc
from database import get_connection
from datetime import datetime

class show_airport_links:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление связь между аэропортами и рейсами")
        self.root.geometry("900x500")
        self.root.configure(bg="#FFFFFF")

        self.load_icons()
        self.create_widgets()
        self.load_data()

    def load_icons(self):
        try:
            self.code_icon = ImageTk.PhotoImage(Image.open("assets/Связь_между_аэропортами_и_рейсами/Код.png").resize((40, 40)))
            self.flight_id_icon = ImageTk.PhotoImage(Image.open("assets/Связь_между_аэропортами_и_рейсами/рейс_id.png").resize((40, 40)))
            self.airport_id_icon = ImageTk.PhotoImage(Image.open("assets/Связь_между_аэропортами_и_рейсами/аэропорт_id.png").resize((40, 40)))
            self.airport_type_icon = ImageTk.PhotoImage(Image.open("assets/Связь_между_аэропортами_и_рейсами/тип_аэропорта.png").resize((40, 40)))
            self.booking_icon = ImageTk.PhotoImage(Image.open("assets/Связь_между_аэропортами_и_рейсами/icons8_hub_100px_2.png").resize((100, 100)))
            self.user_icon = ImageTk.PhotoImage(Image.open("assets/OIP.jpeg").resize((100, 100)))
            print("Иконки успешно загружены.")
        except Exception as e:
            print(f"Ошибка загрузки иконок: {e}")
            self.code_icon = self.flight_id_icon = self.airport_id_icon = self.airport_type_icon = self.booking_icon = self.user_icon = None

    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", pady=(10, 0))

        title_label = ttk.Label(header_frame, text="Список Связь между аэропортами и рейсами")
        title_label.pack(side="left", padx=20, pady=10)

        refresh_btn = ttk.Button(header_frame, text="🔄 Обновить", command=self.load_data)
        refresh_btn.pack(side="right", padx=20, pady=10)

        manage_users_btn = ttk.Button(header_frame, text="Управление данными приложений", command=self.open_flight_airport_management)
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
            query = 'SELECT Код, рейс_id, аэропорт_id, тип_аэропорта FROM Связь_между_аэропортами_и_рейсами'
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            for row in data:
                self.add_flight_airport_row(row)

            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные.\n{e}")

    def add_flight_airport_row(self, row):
        relationship_frame = ttk.Frame(self.canvas_frame, padding=10)
        relationship_frame.pack(fill="x", pady=5, padx=10)

        icon_label = ttk.Label(relationship_frame, image=self.booking_icon)
        icon_label.image = self.booking_icon
        icon_label.grid(row=0, column=0, padx=10, rowspan=4)

        self.add_field(relationship_frame, f"Код: {row[0]}", self.code_icon, 1)
        self.add_field(relationship_frame, f"Рейс ID: {row[1]}", self.flight_id_icon, 2)
        self.add_field(relationship_frame, f"Аэропорт ID: {row[2]}", self.airport_id_icon, 3)
        self.add_field(relationship_frame, f"Тип аэропорта: {row[3]}", self.airport_type_icon, 4)

        edit_btn = ttk.Button(relationship_frame, text="Редактировать", command=lambda r=row: self.open_edit_window(r))
        edit_btn.grid(row=0, column=2, padx=10, pady=5)

    def open_edit_window(self, row):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать Связь Аэропорт-Рейс")
        edit_window.geometry("400x350")
        edit_window.configure(bg="#FFFFFF")

        labels = ["Код", "Рейс ID", "Аэропорт ID", "Тип аэропорта"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(edit_window, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, row[i])

            self.entries[label_text] = entry

        update_btn = ttk.Button(edit_window, text="Обновить", command=lambda: self.update_AirportFlightLink(row[0], edit_window))
        update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_AirportFlightLink(self, link_code, edit_window):
        new_code = self.entries["Код"].get()
        new_flight_id = self.entries["Рейс ID"].get()
        new_airport_id = self.entries["Аэропорт ID"].get()
        new_airport_type = self.entries["Тип аэропорта"].get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Связь_между_аэропортами_и_рейсами SET Код=?, рейс_id=?, аэропорт_id=?, тип_аэропорта=? WHERE Код=?",
                (new_code, new_flight_id, new_airport_id, new_airport_type, link_code)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Данные связи обновлены.")
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
            cursor.execute("SELECT Код, рейс_id, аэропорт_id, тип_аэропорта FROM Связь_между_аэропортами_и_рейсами")
            bookings = cursor.fetchall()

            self.seat_table.delete(*self.seat_table.get_children())
            for booking in bookings:
                self.seat_table.insert("", "end", values=booking)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def add_flight_airport_relationship(self):
        try:
            code = self.entries["Код"].get().strip()
            flight_id = int(self.entries["Рейс ID"].get())
            airport_id = int(self.entries["Аэропорт ID"].get())
            airport_type = self.entries["Тип аэропорта"].get().strip()

            if not code or not airport_type:
                messagebox.showwarning("Ошибка", "Поля 'Код' и 'Тип аэропорта' не могут быть пустыми.")
                return

        except ValueError as e:
            messagebox.showwarning("Ошибка", f"Неверный формат данных: {e}")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Связь_между_аэропортами_и_рейсами (Код, рейс_id, аэропорт_id, тип_аэропорта) VALUES (?, ?, ?, ?)",
                (code, flight_id, airport_id, airport_type)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Связь между рейсом и аэропортом добавлена.")
            self.load_table_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить связь: {e}")

    def open_flight_airport_management(self):
        management_window = tk.Toplevel(self.root)
        management_window.title("Управление связями рейсов и аэропортов")
        management_window.geometry("800x600")
        management_window.configure(bg="#FFFFFF")

        title_label = ttk.Label(management_window, text="Управление связями рейсов и аэропортов")
        title_label.pack(pady=10)

        fields_frame = ttk.Frame(management_window)
        fields_frame.pack(pady=10)

        labels = ["Код", "Рейс ID", "Аэропорт ID", "Тип аэропорта"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(fields_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(fields_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.entries[label_text] = entry

        btn_frame = ttk.Frame(management_window)
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Добавить", command=self.add_flight_airport_relationship)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        columns = ("Код", "Рейс ID", "Аэропорт ID", "Тип аэропорта")
        self.seat_table = ttk.Treeview(management_window, columns=columns, show="headings", height=10)

        for col in columns:
            self.seat_table.heading(col, text=col)
            self.seat_table.column(col, width=140, anchor="center")

        self.seat_table.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_table_data()