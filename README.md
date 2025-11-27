# 📊 Small Business Bookkeeping App

A lightweight **double-entry bookkeeping application** built with **Python** and **Streamlit**.  
This app allows small business owners to record daily transactions, track account balances, and view **real-time financial statements** (Income Statement and Balance Sheet).

---

## ✨ Features

### 🔹 Double-Entry Accounting  
Enforces the fundamental accounting equation:  
**Assets = Liabilities + Equity**  
Every transaction must have balanced **debits and credits**.

### 🔹 Real-Time Dashboard  
Automatically generates:  
- **Income Statement** (Revenue vs. Expenses)  
- **Balance Sheet** (Assets, Liabilities, Equity)

### 🔹 Data Persistence  
All transactions and balances are stored in **`ledger.pkl`**, ensuring no data loss when the app closes.

### 🔹 Journal Entry Form  
A user-friendly interface to input transactions with **multiple line items (splits)**.

### 🔹 Chart of Accounts  
Shows all accounts and their current balances.

### 🔹 Transaction Log  
Displays a full history of all previously posted journal entries.

---

## 📂 Project Structure

The project contains two main Python files:

### **1. `app.py`**
- Main Streamlit UI  
- Form handling  
- Dashboard  
- Income Statement & Balance Sheet generation  

### **2. `ledger_classes.py`**
- Core data models:
  - `Account`
  - `Ledger`
  - `JournalEntry`
  - `Posting`
- Separated to avoid Streamlit serialization errors

---

## 🚀 Getting Started

### **Prerequisites**

Ensure you have **Python 3.8 or higher** installed.  
You will need the following libraries:

- `streamlit`
- `pandas`

---

### **Installation**

1. **Clone or download** this repository (or place the files in a folder).  
2. Install dependencies:

```bash
pip install streamlit pandas

## ▶️ Running the App

Navigate to the project directory in your terminal and run:

```bash
streamlit run app.py
```

The application will launch in your default web browser (usually at http://localhost:8501).


## 📖 Usage Guide

### **1. Dashboard Tab**

This is your landing page. It displays:

- **Net Income:** Calculated as *Total Revenue − Total Expenses*
- **Income Statement:** Shows where money is coming in and going out
- **Balance Sheet:** Snapshot of Assets, Liabilities, and Equity

---

### **2. New Journal Entry Tab**

Use this tab to record transactions.

- **Date:** Select the transaction date  
- **Description:** Enter a memo (e.g., "Paid Office Rent")  
- **Postings:** Add line items for the transaction  

#### Example — Paying Rent:
Line 1: Rent Expense | Debit | 1000.00
Line 2: Cash | Credit | 1000.00


Click **Post Journal Entry**.  
The app validates that **Debits = Credits** before saving.

---

### **3. Chart of Accounts Tab**

Displays a table of all accounts in the system  
(e.g., Cash, Accounts Payable, Sales) along with their **current balances**.

---

### **4. All Entries Tab**

A complete, read-only log of all validated journal entries ever entered.

---

## 💾 Data Storage

- The app creates **`ledger.pkl`** in the same directory.
- **Do NOT delete** this file unless you want to erase all saved data.
- To back up your data:  
  Simply copy the **`ledger.pkl`** file to another location.

---

## 🛠️ Extending the App

To modify or extend functionality:

- **Add new accounts:** Edit the `initialize_ledger()` function in `app.py`.  
- **Change business logic:** Modify the classes inside `ledger_classes.py`.


