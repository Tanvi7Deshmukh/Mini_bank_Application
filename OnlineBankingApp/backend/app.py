from flask import Flask, render_template, request, redirect, session
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "mysecretkey123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT user_id, email, password_hash, role FROM users WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["user_id"]
            session["email"] = user["email"]
            session["role"] = user["role"]

            return redirect("/admin/dashboard" if user["role"] == "ADMIN" else "/dashboard")

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "ADMIN":
        return redirect("/")

    return render_template("admin_dashboard.html")

@app.route("/admin/users")
def admin_users():
    if session.get("role") != "ADMIN":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_id, full_name, email, role, created_at
        FROM users
    """)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin_users.html", users=users)

@app.route("/admin/accounts")
def admin_accounts():
    if "role" not in session or session["role"] != "ADMIN":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT account_number, full_name, phone, balance, status
        FROM accounts
        ORDER BY created_at DESC
    """)
    accounts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin_accounts.html", accounts=accounts)

@app.route("/admin/transactions")
def admin_transactions():
     
    if "role" not in session or session["role"] != "ADMIN":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT from_account, to_account, amount, txn_type, txn_time
        FROM transactions
        ORDER BY txn_time DESC
    """)
    transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin_transactions.html", transactions=transactions)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        account_number = request.form["account_number"]
        full_name = request.form["full_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ Validate account details
        cursor.execute("""
            SELECT account_id
            FROM accounts
            WHERE account_number = %s
              AND full_name = %s
              AND phone = %s
              AND status = 'ACTIVE'
              AND user_id IS NULL
        """, (account_number, full_name, phone))

        account = cursor.fetchone()

        if not account:
            cursor.close()
            conn.close()
            return render_template(
                "register.html",
                error="Invalid account details or account already registered"
            )

        # 2️⃣ Check if email already exists
        cursor.execute(
            "SELECT 1 FROM users WHERE email = %s",
            (email,)
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return render_template("register.html", error="Email already registered")

        # 3️⃣ Create user
        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (full_name, email, password_hash, role, created_at)
            VALUES (%s, %s, %s, 'USER', NOW())
        """, (full_name, email, hashed_password))

        user_id = cursor.lastrowid

        # 4️⃣ Link user to account
        cursor.execute("""
            UPDATE accounts
            SET user_id = %s
            WHERE account_number = %s
        """, (user_id, account_number))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    user_id = session["user_id"]
    user_email = session["email"]

    cursor.execute("""
        SELECT account_number, balance, status
        FROM accounts
        WHERE user_id = %s
    """, (user_id,))
    account = cursor.fetchone()

    cursor.execute("""
        SELECT from_account, to_account, amount, txn_type, txn_time
        FROM transactions
        WHERE from_account = %s OR to_account = %s
        ORDER BY txn_time DESC
    """, (account["account_number"], account["account_number"]))
    transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        user_email=user_email,
        account=account,
        transactions=transactions
    )


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "user_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT account_number FROM accounts WHERE user_id = %s",
        (session["user_id"],)
    )
    account = cursor.fetchone()

    if not account:
        cursor.close()
        conn.close()
        return "Account not found"

    from_acc = account["account_number"]

    if request.method == "POST":
        to_acc = request.form["to_account"]
        amount = float(request.form["amount"])
        password = request.form["password"]

        cursor.execute(
            "SELECT password_hash FROM users WHERE user_id = %s",
            (session["user_id"],)
        )
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            cursor.close()
            conn.close()
            return render_template(
                "transfer.html",
                from_account=from_acc,
                error="❌ Invalid password"
            )

        cursor = conn.cursor()
        cursor.callproc("transfer_funds", [from_acc, to_acc, amount])

        result = None
        for r in cursor.stored_results():
            row = r.fetchone()
            if row:
                result = row[0]

        conn.commit()
        cursor.close()
        conn.close()

        if result == "INSUFFICIENT_BALANCE":
            return render_template(
                "transfer.html",
                from_account=from_acc,
                error="Insufficient balance, Transfer Failed"
            )

        return redirect("/dashboard")

    cursor.close()
    conn.close()
    return render_template("transfer.html", from_account=from_acc)


@app.route("/transactions")
def transactions():
    if "user_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get user's account number
    cursor.execute(
        "SELECT account_number FROM accounts WHERE user_id = %s",
        (session["user_id"],)
    )
    account = cursor.fetchone()

    if not account:
        cursor.close()
        conn.close()
        return "Account not found"

    # Fetch transactions
    cursor.execute("""
        SELECT from_account, to_account, amount, txn_type, txn_time
        FROM transactions
        WHERE from_account = %s OR to_account = %s
        ORDER BY txn_time DESC
    """, (account["account_number"], account["account_number"]))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("transactions.html", transactions=data)

@app.route("/verify-balance", methods=["GET", "POST"])
def verify_balance():
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ Fetch password hash
        cursor.execute(
            "SELECT password_hash FROM users WHERE user_id = %s",
            (session["user_id"],)
        )
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            cursor.close()
            conn.close()
            return "Invalid password"

        # 2️⃣ Fetch balance
        cursor.execute(
            "SELECT balance FROM accounts WHERE user_id = %s",
            (session["user_id"],)
        )
        data = cursor.fetchone()

        cursor.close()
        conn.close()

        return render_template("balance.html", balance=data["balance"])

    return render_template("verify_balance.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
