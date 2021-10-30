# Django Employee Portal
This is a Simple Employee Portal System Developed using Python (Django).
Feel free to make changes based on your requirements.

Inspired by [Project Demo on YouTube](https://www.youtube.com/watch?v=kArCR96m7uo "Django Student Management System Demo")

I've created this project after learning Django by following tutorial series from **SuperCoders**

## Features of this Project

### A. Admin Users
1. See Overall Summary Charts of Employees
2. Add Employees
3. Add Supervisors
4. Add Department (Teams)
5. Request and approve vacation by supervisors
6. Review and respond to comments from Employees

### B. Supervisors
1. See summary of attendance for the day
2. Approve or reject vacation requests
3. Respond to employee feedback

### C. Employees
1. See the Overall Summary Charts
2. Request vacation
3. Send feedback

## How to Install and Run this project?

### Pre-Requisites:
1. Install Git Version Control
[ https://git-scm.com/ ]

2. Install Python Latest Version
[ https://www.python.org/downloads/ ]

3. Install Pip (Package Manager)
[ https://pip.pypa.io/en/stable/installing/ ]

*Alternative to Pip is Homebrew*

### Installation
**1. Create a Folder where you want to save the project**

**2. Create a Virtual Environment and Activate**

Install Virtual Environment First
```
$  pip install virtualenv
```

Create Virtual Environment

For Windows
```
$  python -m venv venv
```
For Mac
```
$  python3 -m venv venv
```

Activate Virtual Environment

For Windows
```
$  source venv/scripts/activate
```

For Mac
```
$  source venv/bin/activate
```

**3. Clone this project**
```
$  git clone https://github.com/kseoul/employee_portal.git
```

Then, Enter the project
```
$  cd employee
```

**4. Install Requirements from 'requirements.txt'**
```python
$  pip install -r requirements.txt
```
**5. Now Run Server

Command for PC:
```python
$ python manage.py runserver
```
Make Migrations

$ python manage.py makemigrations
$ python manage.py migrate

Create Super User (HOD)
```
$  python manage.py createsuperuser
```
Then Add Email, Username and Password

