# ✈️ Airline Database Management System (DBMS)

The **Airline Database Management System (DBMS)** is a desktop-based application developed in **Python 3.11**, utilizing **Tkinter** and **PyQt5** to deliver an intuitive and feature-rich graphical interface. This system is designed to manage all aspects of airline operations — from **user registration** and **flight scheduling** to **seat allocation**, **ticket booking**, **payment processing**, and **passenger records** — powered by a robust **Microsoft Access database** backend.

## 📌 Features

- **User Authentication**
  - Login and registration interfaces with error handling
  - Welcome messages on successful login
- **Flight Management**
  - View, add, and edit flight details
  - Manage departure/arrival times, airport codes, seat capacity
- **Booking Management**
  - Create and manage bookings
  - View booking statuses, prices, and passenger-flight relationships
- **Seat Management**
  - Assign and manage airplane seats
  - Support for multiple seat classes (Economy, Business, First)
- **Payment Management**
  - Track payments for each booking
  - Payment methods, amounts, and status handling
- **Passenger Management**
  - Store detailed passenger data (name, passport, birthdate, contact info)
- **Admin Dashboard**
  - Centralized control panel for managing all system modules

## 🖥️ Interface Overview

### 🔐 Authentication Screens
- **Login Screen** – Enter credentials to access the system  
  📷 *Figure 8: Interface "Login"*

- **Login Error** – Displays when incorrect data is entered  
  📷 *Figure 9: Interface "Invalid Credentials"*

- **Registration Screen** – Sign up as a new user  
  📷 *Figure 10: Interface "Register"*

- **Registration Success** – Confirmation message  
  📷 *Figure 11: Interface "User Registered"*

- **Successful Login** – Welcome message for the user  
  📷 *Figure 12: Interface "Welcome User"*

### 🧭 Main Dashboard

- Access to key system modules: Flights, Bookings, Seats, Payments, Passengers, and Users  
  📷 *Figure 13: Interface "Main Window"*

---

## ✈️ Flight Management

- Flight listing with:
  - Flight code
  - Airline
  - Departure and arrival info
  - Scheduled times
  - Seat availability  
📷 *Figure 14: Interface "Manage Flights"*  
📷 *Figure 15: Interface "Add/Edit Flights"*

---

## 📑 Booking Management

- View and manage:
  - Booking code
  - Passenger and flight IDs
  - Booking date and status
  - Price  
📷 *Figure 16: Interface "Manage Bookings"*  
📷 *Figure 17–18: Edit/Add Booking*

---

## 💺 Seat Management

- Control seat assignments per flight:
  - Seat ID
  - Seat number
  - Class (Economy, Business, First)  
📷 *Figure 19–21: Manage/Edit/Add Seats*

---

## 💳 Payment Management

- Record and manage payments:
  - Linked booking
  - Amount
  - Payment method and status  
📷 *Figure 22–24: Manage/Edit/Add Payments*

---

## 👤 Passenger Management

- Store passenger details:
  - Name, surname
  - Birthdate
  - Passport number
  - Email and phone  
📷 *Figure 25–26: Manage/Edit Passengers*


## ⚙️ Technical Specifications

| Component            | Description                        |
|----------------------|------------------------------------|
| 🐍 Language           | Python 3.11                        |
| 🖼 GUI Frameworks     | Tkinter, PyQt5                     |
| 🗃 Database           | Microsoft Access (.accdb via pyodbc) |
| 📦 Key Libraries      | `tkinter`, `PyQt5`, `pyodbc`, `datetime`, `os` |
| 🖥️ System Type        | Desktop-based Database Management System |


