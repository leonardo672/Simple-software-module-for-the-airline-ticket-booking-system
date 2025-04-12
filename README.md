

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

## 👤 Users Management

- Store passenger details:
  - Name, surname
  - Email
  - Birthdate

### Interface "Manage/Edit Passengers"
  <img src="https://github.com/user-attachments/assets/77fa196c-938d-4c84-9420-b2c3318ec9b2" alt="Interface Main Window" width="600"/>
  
  <img src="https://github.com/user-attachments/assets/ecdc2fca-9bcc-4fa4-a39f-4cb9dabc49cc" alt="Interface Main Window" width="600"/>

## ✈️ Flight Management

- Flight listing with:
  - Flight code
  - Airline
  - Departure and arrival info
  - Scheduled times
  - Seat availability
    
 ### Interface "Manage Flights"
  <img src="https://github.com/user-attachments/assets/50a5e0fd-0dc8-4c8b-ab30-87c00b0e70a9" alt="Interface Main Window" width="600"/>

 ### Interface "Add/Edit Flights"
  <img src="https://github.com/user-attachments/assets/abf96565-8299-4cfe-a9a3-91f2d29d4a82" alt="Interface Main Window" width="600"/>

  <img src="https://github.com/user-attachments/assets/d1375473-3fce-44b6-a362-9782f94d7f01" alt="Interface Main Window" width="600"/>

---

## 📑 Booking Management

- View and manage:
  - Booking code
  - Passenger and flight IDs
  - Booking date and status
  - Price  
📷 *Figure 16: Interface "Manage Bookings"*
 ### Interface "Manage Flights"
  <img src="https://github.com/user-attachments/assets/e35da353-59c7-4116-b174-4e503ff2b776" alt="Interface Main Window" width="600"/>

 ### Interface "Edit/Add Booking"
  <img src="https://github.com/user-attachments/assets/ced9fe7a-8754-4d6d-ac70-a78182c3ad4d" alt="Interface Main Window" width="600"/>

  <img src="https://github.com/user-attachments/assets/c653ace4-2d0f-4ba9-a17c-f93deec84510" alt="Interface Main Window" width="600"/>
  
---

## 💺 Seat Management

- Control seat assignments per flight:
  - Seat ID
  - Seat number
  - Class (Economy, Business, First)
    
### Interface "Manage/Edit/Add Seats"
  <img src="https://github.com/user-attachments/assets/39fb0d52-80bf-4af5-bf5b-9b80701befc0" alt="Interface Main Window" width="600"/>
  
  <img src="https://github.com/user-attachments/assets/0a86915c-e600-4147-933d-0351e8707e0b" alt="Interface Main Window" width="600"/>

  <img src="https://github.com/user-attachments/assets/0e2996b2-02fe-4ccf-94b3-2d5f33ca3777" alt="Interface Main Window" width="600"/>

---

## 💳 Payment Management

- Record and manage payments:
  - Linked booking
  - Amount
  - Payment method and status  

### Interface "Manage/Edit/Add Payments"
  <img src="https://github.com/user-attachments/assets/d2dd6b85-43c8-4252-8f58-5d378013f5ec" alt="Interface Main Window" width="600"/>
  
  <img src="https://github.com/user-attachments/assets/28e1082e-af00-464b-a969-9385d058fc74" alt="Interface Main Window" width="600"/>

  <img src="https://github.com/user-attachments/assets/f2840866-d533-4904-9745-5fd230d3170a" alt="Interface Main Window" width="600"/>

---

## 👤 Passenger Management

- Store passenger details:
  - Name, surname
  - Birthdate
  - Passport number
  - Email and phone  

### Interface "Manage/Edit Passengers"
  <img src="https://github.com/user-attachments/assets/17ff4320-8cee-420a-8977-5c7a532abb66" alt="Interface Main Window" width="600"/>
  
  <img src="https://github.com/user-attachments/assets/8e082a3e-82b0-47c7-acbf-0c81997c8122" alt="Interface Main Window" width="600"/>

  <img src="https://github.com/user-attachments/assets/cd7a5ae9-9887-4e7f-87cf-fe334312643c" alt="Interface Main Window" width="600"/>

---

## 🛫 Airport-Flight Relationship Management

This module allows system administrators to manage the connections between flights and the airports they operate from.

- View existing airport-flight links
- Set or update:
  - Departure Airport
  - Arrival Airport
  - Associated Flight

### Interface "Manage/Edit Airport-Flight Relationship"
  <img src="https://github.com/user-attachments/assets/8cace9ce-e6ae-4716-94c6-be43c31ae02b" alt="Interface Main Window" width="600"/>
  
  <img src="https://github.com/user-attachments/assets/b6dbf150-8df0-408f-aeaf-04de4a6fedac" alt="Interface Main Window" width="600"/>

  <img src="https://github.com/user-attachments/assets/e84610bf-83b0-4eca-9ae7-3dde24bdce35" alt="Interface Main Window" width="600"/>

---

## ⚙️ Technical Specifications

| Component            | Description                        |
|----------------------|------------------------------------|
| 🐍 Language           | Python 3.11                        |
| 🖼 GUI Frameworks     | Tkinter, PyQt5                     |
| 🗃 Database           | Microsoft Access (.accdb via pyodbc) |
| 📦 Key Libraries      | `tkinter`, `PyQt5`, `pyodbc`, `datetime`, `os` |
| 🖥️ System Type        | Desktop-based Database Management System |
