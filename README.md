
## 💰 Personal Finance Manager

A Python-based **console application** that helps users manage their income, expenses, savings goals, and budgets — all from the terminal.
It includes detailed reports, financial health analysis, and persistent data storage using JSON and CSV files.

---

### 🧭 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Advanced Features](#advanced-features)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Sample Output](#sample-output)
* [Technical Details](#technical-details)
* [Future Improvements](#future-improvements)
* [License](#license)

---

### 📋 Overview

The **Personal Finance Manager** is a modular console app built in Python to help users:

* Track income and expenses
* Analyze spending habits
* Set and monitor monthly budgets
* View reports and a financial health score

It demonstrates key Python concepts:

* File handling (JSON, CSV)
* Data validation & error handling
* OOP & modular programming
* Console-based menu systems

---

### ⚙️ Features

#### 👤 User Management

* Register & login with password hashing (bcrypt)
* Strong password validation (uppercase, lowercase, digit, special character, 8+ chars)
* Multi-user support with profiles and balances

#### 💳 Transactions

* Add, edit, and delete transactions
* Track both **income** and **expenses**
* Automatically save transactions to `transactions.csv`

#### 📊 Reports

* Dashboard summary (income, expenses, balance)
* Monthly and category-based reports
* Financial Health Score calculation
* Budget tracking with warnings

#### 💾 Data Persistence

* JSON for users
* CSV for transactions
* Auto-load and auto-save on each operation

---

### 🌟 Advanced Features

* **Savings Goals with Progress Tracking**
* **Monthly Budget Management**
* **Recurring Transactions**
* **Financial Health Score**
* **ASCII Data Visualization**
* **Bill Reminder System**
* **Predictive Analytics (optional)**
* **CSV Import/Export**

---

### 🧩 Project Structure

```
├── main.py                 # Main program and menu system
├── user_manager.py         # Handles registration, login, user profiles
├── transactions.py         # Manages transaction CRUD operations
├── reports.py              # Generates reports & financial health score
├── utils.py                # Common functions: hashing, validation, data I/O
├── users.json              # Stored user data
├── transactions.csv        # Stored transaction data
└── budgets.json            # Stored budget data
```

---

### 🛠️ Installation

#### Requirements

* Python 3.8+
* Modules:

  ```bash
  pip install bcrypt
  ```

#### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
2. Run the program:

   ```bash
   python main.py
   ```

---

### 🖥️ Usage

* Follow the on-screen menu to:

  * Register or login
  * Add income or expenses
  * Set a monthly budget
  * View dashboards or health scores
  * Exit safely (data auto-saves)

---

### 💡 Sample Output

```
============================================================
                  Financial Health Score
============================================================
score                    : 82
message                  : 💚 Excellent financial health! Keep it up.
============================================================

