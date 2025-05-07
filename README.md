

# 💸 Flask Bank App

A simple yet functional **bank management system** built using **Flask** and **file-based data storage**. This backend-focused project is designed to help understand and implement key concepts like **authentication**, **CRUD operations**, and **data persistence**—all without using a traditional database.

---

## 🚀 Features

* 🔐 User Registration & Login with Password Hashing
* 🔑 JWT-Based Authentication for Secure Session Management
* 💰 Deposit & Withdraw Functionality
* 🔄 Transfer Funds Between Users
* 📜 View Full Transaction History
* 📁 JSON-Based File Storage (No Database)
* 🧩 Modular Code Architecture Using Flask Blueprints
* ⚛️ Ready for Future Integration with a React Frontend

---

## 🧠 Project Goals

* Practice user **authentication** and **authorization**
* Understand **file-based data persistence** techniques
* Learn how to structure a Flask application using **blueprints**
* Simulate real-world **banking system logic**
* Improve **debugging** and **problem-solving** skills in backend development

---

## 📁 Project Structure

```
flask-bank-app/
│
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── logs.log            # Logging system output
├── README.md           # Project documentation
├── LICENSE             # License information
│
├── data/               # JSON file storage (user data)
│   ├── admin.json
│   └── brahim.json
│
├── utils/              # Utility modules
│   ├── authmanager.py  # Handles JWT and authentication logic
│   ├── logger.py       # Logging setup
│   └── storage.py      # Read/write JSON data
│
├── views/              # Flask blueprints (routes)
│   ├── auth.py         # Authentication routes
│   ├── banking.py      # Deposit, withdraw, transfer
│   └── admin.py        # Admin-related endpoints
│
└── test.py             # Testing script
```

---

## ⚙️ Requirements

* Python 3.x
* Flask
* Standard Python Libraries (`uuid`, `hashlib`, `json`, `os`, etc.)

---

## 🏃‍♂️ How to Run the App

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/BrahimChatri/flask-bank-app.git
cd flask-bank-app
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Launch the Server

```bash
python app.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 💡 Notes

This is a backend-focused learning project. No database is used — all data is stored securely in JSON files. You are encouraged to extend this system with:

* 🧪 Unit tests
* 🔐 Role-based access control
* 🗃️ Database integration (e.g., SQLite or PostgreSQL)
* 📈 Admin dashboard or metrics
* ⚙️ API rate limiting or error handling enhancements

---

## 📚 License

This project is open for educational use. Feel free to fork, modify, and build on it. Contributions are welcome!
