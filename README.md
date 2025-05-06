# 💸 Flask Bank App

A simple bank management system built with Flask and file-based data storage.  
The goal of this project is to learn and implement core backend concepts like authentication, CRUD operations, and data persistence — without using a database.

---

## 🚀 Features

- User Registration & Login
- JWT-based Authentication
- Deposit & Withdraw Funds
- Transfer Between Users
- View Transaction History
- File-based Data Storage (JSON or similar)
- Modular Code Structure with Blueprints
- Futur react app for front-end

---

## 📁 Project Structure

```
|-- flask-bank-app
    |-- .env
    |-- .gitignore
    |-- app.py
    |-- config.py
    |-- directoryList.md
    |-- LICENSE
    |-- logs.log
    |-- README.md
    |-- requirements.txt
    |-- test.py
    |-- data
    |   |-- admin.json
    |   |-- brahim.json
    |-- utils
    |   |-- authmanager.py
    |   |-- logger.py
    |   |-- storage.py
    |   |-- __init__.py
    |  
    |-- views
    |   |-- admin.py
    |   |-- auth.py
    |   |-- banking.py
    |   |-- __init__.py


```

---

## 🧠 Goals of This Project

- Practice authentication and session handling.
- Understand file-based data persistence.
- Organize a Flask project using blueprints.
- Build a real-world-like application step by step.
- Develop problem-solving and debugging skills.

---

## 📌 Requirements

- Python 3.x
- Flask
- Any other standard libraries (like `uuid`, `hashlib`, `json`)

---

## 🏃‍♂️ Running the App

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/BrahimChatri/flask-bank-app.git
cd flask-bank-app
```

### 2️⃣ Install Dependencies  
Ensure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Flask Server  
```bash
python app.py
```
Then, open **http://127.0.0.1:5000** in your browser.
---

## 💡 Notes

This is a learning-focused project. It doesn't use a database — everything is stored in simple JSON files.  
You’re encouraged to improve upon it later by adding database support, proper validation, better UI, and more advanced security.

---

## 📚 License

This project is for educational purposes. Use it to learn, break it, fix it, and improve it!
```

