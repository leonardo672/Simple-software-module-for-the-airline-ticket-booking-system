import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyodbc
from database import get_connection
from datetime import datetime

class show_payments:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление Оплаты")
        self.root.geometry("900x500")
        self.root.configure(bg="#FFFFFF")

        self.load_icons()
        self.create_widgets()
        self.load_data()

    def load_icons(self):
        try:
            self.code_icon = ImageTk.PhotoImage(Image.open("assets/Оплаты/Код.png").resize((30, 30)))
            self.booking_id_icon = ImageTk.PhotoImage(Image.open("assets/Оплаты/бронирование_id.png").resize((30, 30)))
            self.amount_icon = ImageTk.PhotoImage(Image.open("assets/Оплаты/сумма.png").resize((30, 30)))
            self.payment_date_icon = ImageTk.PhotoImage(Image.open("assets/Оплаты/дата_оплаты.png").resize((30, 30)))
            self.payment_method_icon = ImageTk.PhotoImage(Image.open("assets/Оплаты/способ_оплаты.png").resize((30, 30)))
            self.payment_status_icon = ImageTk.PhotoImage(Image.open("assets/Оплаты/статус_оплаты.png").resize((30, 30)))
            self.booking_icon = ImageTk.PhotoImage(Image.open("assets/Оплаты/vector-payment-icon.jpg").resize((100, 100)))
            self.user_icon = ImageTk.PhotoImage(Image.open("assets/OIP.jpeg").resize((40, 40)))
            print("Иконки успешно загружены.")
        except Exception as e:
            print(f"Ошибка загрузки иконок: {e}")
            self.code_icon = self.booking_id_icon = self.amount_icon = self.payment_date_icon = self.payment_method_icon = self.payment_status_icon = self.booking_icon = self.user_icon = None

    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", pady=(10, 0))

        title_label = ttk.Label(header_frame, text="Список Оплаты")
        title_label.pack(side="left", padx=20, pady=10)

        refresh_btn = ttk.Button(header_frame, text="🔄 Обновить", command=self.load_data)
        refresh_btn.pack(side="right", padx=20, pady=10)

        manage_payments_btn = ttk.Button(header_frame, text="Управление оплатами", command=self.open_payment_management)
        manage_payments_btn.pack(side="right", padx=20, pady=10)

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

        footer_label = ttk.Label(footer_frame, text="© 2025 Управление Оплаты")
        footer_label.pack(side="bottom", pady=5)

    def load_data(self):
        try:
            conn = get_connection()
            query = 'SELECT Код, бронирование_id, сумма, дата_оплаты, способ_оплаты, статус_оплаты FROM Оплаты'
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            for row in data:
                self.add_payment_row(row)

            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные.\n{e}")

    def add_payment_row(self, row):
        payment_frame = ttk.Frame(self.canvas_frame, padding=10)
        payment_frame.pack(fill="x", pady=5, padx=10)

        icon_label = ttk.Label(payment_frame, image=self.booking_icon)
        icon_label.image = self.booking_icon
        icon_label.grid(row=0, column=0, padx=10, rowspan=6)

        self.add_field(payment_frame, f"Код: {row[0]}", self.code_icon, 1)
        self.add_field(payment_frame, f"Бронирование ID: {row[1]}", self.booking_id_icon, 2)
        self.add_field(payment_frame, f"Сумма: {row[2]}", self.amount_icon, 3)
        self.add_field(payment_frame, f"Дата оплаты: {row[3]}", self.payment_date_icon, 4)
        self.add_field(payment_frame, f"Способ оплаты: {row[4]}", self.payment_method_icon, 5)
        self.add_field(payment_frame, f"Статус оплаты: {row[5]}", self.payment_status_icon, 6)

        edit_btn = ttk.Button(payment_frame, text="Редактировать", command=lambda r=row: self.open_edit_window(r))
        edit_btn.grid(row=0, column=2, padx=10, pady=5)

    def open_edit_window(self, row):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать Оплату")
        edit_window.geometry("400x300")
        edit_window.configure(bg="#FFFFFF")

        labels = ["Код", "Бронирование ID", "Сумма", "Дата оплаты", "Способ оплаты", "Статус оплаты"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(edit_window, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, row[i])

            self.entries[label_text] = entry

        update_btn = ttk.Button(edit_window, text="Обновить", command=lambda: self.update_Payments(row[0], edit_window))
        update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_Payments(self, payment_code, edit_window):
        new_payment_code = self.entries["Код"].get()
        new_booking_id = self.entries["Бронирование ID"].get()
        new_amount = self.entries["Сумма"].get()
        new_payment_date = self.entries["Дата оплаты"].get()
        new_payment_method = self.entries["Способ оплаты"].get()
        new_payment_status = self.entries["Статус оплаты"].get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Оплаты SET Код=?, бронирование_id=?, сумма=?, дата_оплаты=?, способ_оплаты=?, статус_оплаты=? WHERE Код=?",
                (new_payment_code, new_booking_id, new_amount, new_payment_date, new_payment_method, new_payment_status, payment_code)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Данные оплаты обновлены.")
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
            cursor.execute("SELECT Код, бронирование_id, сумма, дата_оплаты, способ_оплаты, статус_оплаты FROM Оплаты")
            payments = cursor.fetchall()

            self.seat_table.delete(*self.seat_table.get_children())
            for payment in payments:
                self.seat_table.insert("", "end", values=payment)

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def add_payment(self):
        try:
            code = int(self.entries["Код"].get())
            booking_id = int(self.entries["Бронирование ID"].get())
            amount = float(self.entries["Сумма"].get())
            payment_date = self.entries["Дата оплаты"].get().strip()
            payment_method = self.entries["Способ оплаты"].get().strip()
            payment_status = self.entries["Статус оплаты"].get().strip()

            if not payment_date or not payment_method or not payment_status:
                messagebox.showwarning("Ошибка", "Все поля должны быть заполнены.")
                return

        except ValueError as e:
            messagebox.showwarning("Ошибка", f"Неверный формат данных: {e}")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Оплаты (код, бронирование_id, сумма, дата_оплаты, способ_оплаты, статус_оплаты) VALUES (?, ?, ?, ?, ?, ?)",
                (code, booking_id, amount, payment_date, payment_method, payment_status)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Успех", "Запись об оплате добавлена.")
            self.load_table_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить запись об оплате: {e}")

    def open_payment_management(self):
        management_window = tk.Toplevel(self.root)
        management_window.title("Управление оплатами")
        management_window.geometry("1000x600")
        management_window.configure(bg="#FFFFFF")

        title_label = ttk.Label(management_window, text="Управление оплатами")
        title_label.pack(pady=10)

        fields_frame = ttk.Frame(management_window)
        fields_frame.pack(pady=10)

        labels = ["Код", "Бронирование ID", "Сумма", "Дата оплаты", "Способ оплаты", "Статус оплаты"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(fields_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(fields_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.entries[label_text] = entry

        btn_frame = ttk.Frame(management_window)
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Добавить", command=self.add_payment)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        columns = ("Код", "Бронирование ID", "Сумма", "Дата оплаты", "Способ оплаты", "Статус оплаты")
        self.seat_table = ttk.Treeview(management_window, columns=columns, show="headings", height=10)

        for col in columns:
            self.seat_table.heading(col, text=col)
            self.seat_table.column(col, width=140, anchor="center")

        self.seat_table.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_table_data()