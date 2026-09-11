# 🧠 Programming Mistake Museum

A Python-based desktop application for recording, managing, searching, and analyzing programming mistakes.

The **Programming Mistake Museum** helps developers keep a personal collection of coding mistakes so they can understand recurring errors, learn from them, and improve their programming skills over time.

## 🚀 Features

* ➕ Add programming mistakes
* 📋 View all recorded mistakes
* 🔎 Search mistakes
* ✏️ Edit existing mistakes
* 🗑️ Delete mistakes
* 📊 View statistics and mistake patterns
* 💾 SQLite database storage
* 📝 Logging system
* 🖥️ Tkinter graphical user interface
* 📈 Data visualization using Matplotlib
* 🧪 Basic testing with Pytest
* ⚙️ Configuration management

## 🛠️ Technologies Used

* **Python**
* **Tkinter** – Graphical User Interface
* **SQLite** – Database
* **Matplotlib** – Statistics and visualization
* **Pytest** – Testing
* **Git & GitHub** – Version control

## 📂 Project Structure

```text
Programming_Mistake_Museum/
│
├── .gitignore
├── README.md
├── config.py
├── database.py
├── gui.py
├── gui.spec
├── main.py
└── test_museum.py
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/NaveenMR-beep/Programming_Mistake_Museum.git
```

### 2. Open the project

```bash
cd Programming_Mistake_Museum
```

### 3. Install required packages

```bash
pip install matplotlib pytest
```

Tkinter and SQLite are normally included with standard Python installations on Windows.

## ▶️ Running the Application

Run:

```bash
python main.py
```

The application will open the Programming Mistake Museum interface.

## 🧪 Running Tests

Run:

```bash
python -m pytest -v
```

## 💡 How It Works

The application stores programming mistakes in an SQLite database.

A typical workflow is:

```text
Add Mistake
     ↓
Store in SQLite Database
     ↓
View / Search Mistakes
     ↓
Edit or Delete
     ↓
Analyze Mistake Statistics
     ↓
Learn from Recurring Errors
```

## 📊 Statistics

The application can analyze the stored mistakes to identify patterns such as:

* Most common error types
* Mistakes by category
* Number of recorded mistakes
* Frequently occurring programming problems

These statistics help identify areas where additional practice may be useful.

## 🔮 Future Improvements

Possible future enhancements include:

* 🤖 Automatic error detection
* 🧠 AI-based mistake categorization
* 💡 Automatic suggestions for fixing mistakes
* 📈 Advanced analytics dashboard
* 🔐 User accounts
* ☁️ Cloud database support
* 🌐 Web-based version
* 📱 Mobile application
* 📊 More advanced visualizations

## 👨‍💻 Author

**Naveen M R**

GitHub: [NaveenMR-beep](https://github.com/NaveenMR-beep)

## 📄 License

This project is intended for educational and learning purposes.
