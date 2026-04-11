# Holberton School - HBNB AirBnB Clone

This repository contains my implementation of the **HBnB (AirBnB) clone project** from the Holberton School curriculum.  
The goal of this project is to build a Python web application inspired by the core features of the AirBnB platform, focusing on backend logic, data modeling, API handling, and project structure following best practices.

---

## 🚀 Project Overview

HBnB is designed to mimic some of the basic functionalities of AirBnB, such as:

- Creating and managing users  
- Listing and storing places for rent  
- Reviews and amenities concept  
- Searching and showing stored data  

This project is part of the Holberton curriculum and demonstrates understanding of:

- Object-oriented programming (OOP) in Python  
- REST/API design principles  
- Data storage and manipulation  
- Coding best practices and modular architecture

---

## 📁 Repository Structure

The project is organized into logical parts:

- `part1/` — foundational setup and initial tasks  
- `part2/hbnb/` — main application logic  
- `part3/` — additional features and enhancements  
- `.venv/` — Python virtual environment directory  
- `requirements.txt` — project dependencies

---

## 🛠️ Requirements

- Python 3.x  
- Virtual environment (`venv`)  
- Flask (or framework versions listed in `requirements.txt`)  
- Other dependencies from `requirements.txt`

---

## 📦 Installation & Usage

1. **Clone the repository**
```bash
git clone https://github.com/mnarzaid247-stack/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
_(depending on the app structure — this is an example)_
```bash
python app.py
```

Check routes in the code or README instructions inside parts for specific commands.

---

## 🧠 Skills Demonstrated

- Python OOP and modular design  
- REST API routing and request handling  
- Data persistence structure  
- Testing and debugging smaller modules  
- Understanding web app fundamentals


---

## 🌐 Part 4 - Web Client

### Description
This part implements a simple web client that interacts with the backend API to:
- Log in users and store authentication tokens
- Display a list of places
- View detailed information about a selected place
- Add reviews for places (only when logged in)

### How to Run

#### Run Backend (Part 3)
```bash
cd part3
python run.py
```


#### Run Frontend (Part 4)
```
cd part4
python -m http.server 8000
``` 

### Open in Browser
- http://127.0.0.1:8000/login.html
- http://127.0.0.1:8000/index.html

### How to Test
1. Open `login.html` and log in with valid credentials  
2. Go to `index.html` to view all places  
3. Click on "View Details" for any place  
4. Add a review (only works if logged in)


## 🧑‍💻 Author

**Manar Al-Zhrani**  
**Aljawharah saad**

**Reem**

