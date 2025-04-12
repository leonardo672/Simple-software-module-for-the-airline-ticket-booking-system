![image](https://github.com/user-attachments/assets/00ad64b8-c4fa-40a5-b6f7-4c34ffec5ee5)# ✈️ Airline Database Management System (DBMS)

The **Airline Database Management System (DBMS)** is a desktop-based application developed in **Python 3.11**, utilizing **Tkinter** and **PyQt5** to deliver an intuitive and feature-rich graphical interface. This system is designed to manage all aspects of airline operations — from **user registration** and **flight scheduling** to **seat allocation**, **ticket booking**, **payment processing**, and **passenger records** — powered by a robust **Microsoft Access database** backend.

## 📌 Features

- **User Authentication**
  - Login and registration interfaces with error handling
  - Welcome messages on successful login
- **Main Interface**
  - Central hub to access all modules:
    Access to key system modules: Users, Flights, Bookings, Seats, Payments, Passengers, Airports.   
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
- **Airport-Flight Relationship Management**
  - Manage associations between flights and airports
  - Link departure and arrival airport codes to flights

## 🖥️ Interface Overview

### 🔐 Authentication Screens
- **Login Screen** – Enter credentials to access the system  
<img src="https://github.com/user-attachments/assets/f9deabe7-53f6-4a7b-91ca-f6021b5b8dce" alt="Interface Main Window" width="300"/>

- **Login Error** – Displays when incorrect data is entered  
<img src="https://github.com/user-attachments/assets/b49dcdc1-e8e0-44ad-a912-ef1292a4f755" alt="Interface Main Window" width="300"/>

- **Registration Screen** – Sign up as a new user  
<img src="https://github.com/user-attachments/assets/97c502fa-2588-4bc3-9234-0b83ac967465" alt="Interface Main Window" width="300"/>

- **Registration Success** – Confirmation message  
<img src="https://github.com/user-attachments/assets/dd737052-7b9f-4925-8c74-d347281229a0" alt="Interface Main Window" width="300"/>

- **Successful Login** – Welcome message for the user  
<img src="https://github.com/user-attachments/assets/490a47fc-d76e-4641-97ad-6b198afc2933" alt="Interface Main Window" width="300"/>

### 🧭 Main Interface
<img src="https://github.com/user-attachments/assets/30690524-84ee-493b-bf9d-d14e200bf164" alt="Interface Main Window" width="600"/>

---

## ✈️ Flight Management

- Flight listing with:
  - Flight code
  - Airline
  - Departure and arrival info
  - Scheduled times
  - Seat availability
    
 ### Interface "Manage Flights"
  <img src="https://github.com/user-attachments/assets/30690524-84ee-493b-bf9d-d14e200bf164" alt="Interface Main Window" width="600"/>

 ### Interface "Add/Edit Flights"
  <img src="https://github.com/user-attachments/assets/6d57173c-2d27-4422-936c-4d34450ce43f" alt="Interface Main Window" width="600"/>

  <img src="https://github.com/user-attachments/assets/91555ee4-34e1-4e00-a1f6-1b15167d7fb9" alt="Interface Main Window" width="600"/>

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

---

## 🛫 Airport-Flight Relationship Management

This module allows system administrators to manage the connections between flights and the airports they operate from.

- View existing airport-flight links
- Set or update:
  - Departure Airport
  - Arrival Airport
  - Associated Flight

📷 *Figure 27: Interface "Manage Airport-Flight Relationships"*  
📷 *Figure 28: Interface "Add/Edit Airport-Flight Relationship"*

---

## ⚙️ Technical Specifications

| Component            | Description                        |
|----------------------|------------------------------------|
| 🐍 Language           | Python 3.11                        |
| 🖼 GUI Frameworks     | Tkinter, PyQt5                     |
| 🗃 Database           | Microsoft Access (.accdb via pyodbc) |
| 📦 Key Libraries      | `tkinter`, `PyQt5`, `pyodbc`, `datetime`, `os` |
| 🖥️ System Type        | Desktop-based Database Management System |
