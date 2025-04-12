# Airline Ticket Booking System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter%2FPyQt5-green)
![Database](https://img.shields.io/badge/Database-MS_Access-0078D7)

## 🌟 Core Features

## Booking Management System

### Core Modules

#### 1. Flight Management (`aviary.py`)
**Features:**
- Complete flight schedule control
- Real-time status updates
- Capacity monitoring

**Data Attributes:**
| Field | Type | Example |
|-------|------|---------|
| Flight ID | Primary Key | Код 1 |
| Airline | String | Аэроболт |
| Departure | DateTime | 2023-10-25 08:30:00 |
| Arrival | DateTime | 2023-10-25 11:45:00 |
| Seats Available | Integer | 150 |

**Interface:**
![Flight Management Interface](screenshots/flight_management.png)

---

#### 2. Booking System (`bookings.py`)
**Features:**
- End-to-end reservation processing
- Status tracking (Confirmed/Pending)
- Price calculation

**Data Attributes:**
| Field | Type | Example |
|-------|------|---------|
| Booking ID | Primary Key | Код 0 |
| Passenger ID | Foreign Key | 101 |
| Flight ID | Foreign Key | 1 |
| Booking Date | DateTime | 2023-10-20 10:15:00 |
| Status | String | Подтверждено |
| Price | Decimal | 50000 |

**Interface:**
![Booking Management Interface](screenshots/booking_management.png)

---

#### 3. Seat Management (`seats.py`)
**Features:**
- Visual seat mapping
- Class-based allocation
- Real-time availability

**Data Attributes:**
| Field | Type | Example |
|-------|------|---------|
| Seat ID | Primary Key | Код 1 |
| Flight ID | Foreign Key | 1 |
| Seat Number | String | 12А |
| Class | String | Бизнес |

**Interface:**
![Seat Management Interface](screenshots/seat_management.png)

---

#### 4. Payment Processing (`payments.py`)
**Features:**
- Multiple payment methods
- Transaction recording
- Status tracking

**Data Attributes:**
| Field | Type | Example |
|-------|------|---------|
| Payment ID | Primary Key | Код 1 |
| Booking ID | Foreign Key | D1-1 |
| Amount | Decimal | 25000 |
| Payment Date | DateTime | 2023-10-20 10:30:00 |
| Method | String | Карта |
| Status | String | Отдаленно |

**Interface:**
![Payment Interface](screenshots/payment_interface.png)

---

### Administrative Modules

#### 1. Passenger Management (`passengers.py`)
**Features:**
- Complete passenger profiles
- Document verification
- Booking history

**Data Attributes:**
| Field | Type | Example |
|-------|------|---------|
| Passenger ID | Primary Key | Код 1 |
| First Name | String | Иван |
| Last Name | String | Иванов |
| Passport | String | 1234567890 |
| Email | String | hanovo@example.com |

**Interface:**
![Passenger Management](screenshots/passenger_management.png)

---

#### 2. User Administration (`users.py`)
**Features:**
- Role-based access
- Account management
- System permissions

**Data Attributes:**
| Field | Type | Example |
|-------|------|---------|
| User ID | Primary Key | Код 59 |
| First Name | String | Иван |
| Last Name | String | Иванов |
| Email | String | user@example.com |

**Interface:**
![User Management](screenshots/user_management.png)

### Technical Highlights
- Python 3.11's speed optimizations
- Tkinter/PyQt5 hybrid interface
- ACID-compliant Access transactions

## 📸 Screenshots

| Module | Screenshot | Description |
|--------|------------|-------------|
| **Login** | ![Login Window](screenshots/login.png) | Secure PyQt5 authentication |
| **Dashboard** | ![Main Interface](screenshots/dashboard.png) | Central control panel |
| **Flight Booking** | ![Booking Form](screenshots/booking.png) | Ticket reservation screen |
| **Seat Map** | ![Seat Selection](screenshots/seats.png) | Interactive cabin layout |

*Place screenshots in `/screenshots` folder with these exact names for auto-display.*

## 🛠️ Installation

### Prerequisites
1. **Python 3.11** (64-bit recommended)
   ```powershell
   # Windows installation
   winget install Python.Python.3.11
