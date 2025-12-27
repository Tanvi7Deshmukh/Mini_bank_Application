Mini Bank Web Application

A full-stack online banking web application built using Flask (Python) and MySQL, implementing essential banking features such as account creation, secure login, fund transfer, transaction history, and an admin panel.

Features

# User Features

* User Registration & Login (Password Hashing)
* View Account Balance
* Transfer Funds Securely
* View Transaction History
* Session-based Authentication

# Admin Features

* Admin Login
* View All Users
* View All Bank Accounts
* View All Transactions
* Monitor Banking Activities


# Technologies Used


 Backend         Python (Flask)            
 Frontend        HTML, CSS, Bootstrap      
 Database        MySQL                     
 Authentication  Werkzeug Password Hashing 
 ORM/Connector   mysql-connector-python    


# Project Structure


Mini_Bank_App/
|
├── OnlineBankingApp/
|    |
|    |
|    |  
|    ├── backend/
|    │   ├── app.py
|    │   ├── database.py
|    │   ├── hash_passwords.py
|    │   ├── requirements.txt
|    |   |
|    |   ├── templates/
|    |   |    |
|    │   |    ├── login.html
|    |   │    ├── register.html
|    |   │    ├── dashboard.html
|    |   │    ├── transfer.html
|    |   │    ├── balance.html
|    |   │    ├── transactions.html
|    |   │    ├── admin_dashboard.html
|    |   │    ├── admin_users.html
|    |   │    ├── admin_accounts.html
|    |   │    └── admin_transactions.html
|    |   │
|    |   ├── static/
|    |   ├── css/
|    |   └── images/
|
├──minibankapp.sql
│── procedure.sql  
│── online_banking_erd.mwb   
│── triggers.sql
│── indexes.sql
│
│
├── requirements.txt
├── README.md



# Installation & Setup

1. Clone or Extract Project

   * extract the ZIP file.



# 2. Create Virtual Environment 

python -m venv venv
venv\Scripts\activate   # for Windows


# 3. Install Dependencies

pip install -r requirements.txt

(requirements.txt inside Mini_Bank_App/OnlineBankingApp/backend)

# 4. Setup MySQL Database

  1. Open MySQL Workbench
  2. Create a database:

     CREATE DATABASE online_banking_db;


  3. Import SQL files in this order:

    * database/minibankapp.sql`
    * database/procedure.sql`
    * database/triggers.sql`
    * database/indexes.sql`

---

# 5. Configure Database Connection

Update database credentials inside `database.py`:


host="localhost"
user="root"
password="your_mysql_password"
database="online_banking_db"


# 6. Run the Application

python app.py


Open browser:

http://127.0.0.1:5000/


# Sample Credentials

* Role: Admin
* Email: amitsharmaadmin@gmail.com
* Password: as@123

* Role: User
* Email: test@gmail.com
* Password: hashed_password


# Author

  Tanvi Deshmukh
