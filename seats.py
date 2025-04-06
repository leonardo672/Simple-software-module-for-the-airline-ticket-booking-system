import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyodbc
from database import get_connection
from database import insert_data

class show_seats:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление Места в самолете")
        self.root.geometry("900x500")
        self.root.configure(bg="#FFFFFF")

        self.load_icons()
        self.create_widgets()
        self.load_data()

    def load_icons(self):
        try:
            self.code_icon = ImageTk.PhotoImage(Image.open("assets/Места_в_самолете/Код.png").resize((40, 40)))
            self.flight_id_icon = ImageTk.PhotoImage(Image.open("assets/Места_в_самолете/рейс_id.png").resize((40, 40)))
            self.seat_number_icon = ImageTk.PhotoImage(Image.open("assets/Места_в_самолете/место_номер.png").resize((40, 40)))
            self.class_icon = ImageTk.PhotoImage(Image.open("assets/Места_в_самолете/класс.png").resize((40, 40)))
            self.user_icon = ImageTk.PhotoImage(Image.open("assets/Места_в_самолете/SAF2020_0341266.jpg").resize((120, 120)))
            print("Иконки успешно загружены.")
        except Exception as e:
            print(f"Ошибка загрузки иконок: {e}")
            self.name_icon = self.surname_icon = self.email_icon = self.birthdate_icon = self.user_icon = None

    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", pady=(10, 0))

        title_label = ttk.Label(header_frame, text="Список Места в самолете")
        title_label.pack(side="left", padx=20, pady=10)

        refresh_btn = ttk.Button(header_frame, text="🔄 Обновить", command=self.load_data)
        refresh_btn.pack(side="right", padx=20, pady=10)

        manage_users_btn = ttk.Button(header_frame, text="Управление данными приложений", command=self.open_seat_management)
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

        footer_label = ttk.Label(footer_frame, text="© 2025 Управление Места в самолете")
        footer_label.pack(side="bottom", pady=5)

    def load_data(self):
        try:
            conn = get_connection()
            query = 'SELECT Код, рейс_id, место_номер, класс FROM Места_в_самолете'
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
        self.add_field(user_frame, f"рейс_id: {row[1]}", self.flight_id_icon, 2)
        self.add_field(user_frame, f"место_номер: {row[2]}", self.seat_number_icon, 3)
        self.add_field(user_frame, f"класс: {row[3]}", self.class_icon, 4)

        edit_btn = ttk.Button(user_frame, text="Редактировать", command=lambda r=row: self.open_edit_window(r))
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
        edit_window.title("Редактировать место")
        edit_window.geometry("400x300")
        edit_window.configure(bg="#FFFFFF")

        labels = ["Код", "Рейс ID", "Номер места", "Класс"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(edit_window, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, row[i])

            self.entries[label_text] = entry

        update_btn = ttk.Button(edit_window, text="Обновить", command=lambda: self.update_seat(row[0], edit_window))
        update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_seat(self, seat_code, edit_window):
        new_seat_code = self.entries["Код"].get()
        new_flight_id = self.entries["Рейс ID"].get()
        new_seat_number = self.entries["Номер места"].get()
        new_seat_class = self.entries["Класс"].get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Места_в_самолете SET Код=?, рейс_id=?, место_номер=?, класс=? WHERE Код=?",
                (new_seat_code, new_flight_id, new_seat_number, new_seat_class, seat_code)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Данные места обновлены.")
            self.load_data()
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить данные: {e}")

    def open_seat_management(self):
        management_window = tk.Toplevel(self.root)
        management_window.title("Управление местами")
        management_window.geometry("700x500")
        management_window.configure(bg="#FFFFFF")

        title_label = ttk.Label(management_window, text="Управление местами")
        title_label.pack(pady=10)

        fields_frame = ttk.Frame(management_window)
        fields_frame.pack(pady=10)

        labels = ["Код", "Рейс ID", "Номер места", "Класс"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(fields_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(fields_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.entries[label_text] = entry

        btn_frame = ttk.Frame(management_window)
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Добавить", command=self.add_seat)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        columns = ("Код", "Рейс ID", "Номер места", "Класс")
        self.seat_table = ttk.Treeview(management_window, columns=columns, show="headings", height=10)

        for col in columns:
            self.seat_table.heading(col, text=col)
            self.seat_table.column(col, width=140, anchor="center")

        self.seat_table.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_table_data()

    def load_table_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Код, рейс_id, место_номер, класс FROM Места_в_самолете")
            users = cursor.fetchall()

            self.seat_table.delete(*self.seat_table.get_children())
            for user in users:
                self.seat_table.insert("", "end", values=user)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def add_seat(self):
        seat_code = self.entries["Код"].get()
        flight_id = self.entries["Рейс ID"].get()
        seat_number = self.entries["Номер места"].get()
        seat_class = self.entries["Класс"].get()

        if not (seat_code and flight_id and seat_number and seat_class):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Места_в_самолете (Код, рейс_id, место_номер, класс) VALUES (?, ?, ?, ?)",
                (seat_code, flight_id, seat_number, seat_class)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Место добавлено.")
            self.load_table_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить место: {e}")