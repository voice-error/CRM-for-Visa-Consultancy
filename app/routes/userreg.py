from flask import Flask, render_template,flash, request,redirect,url_for
import secrets
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/userreg", methods =["GET", "POST"])
def register():
    if request.method =="POST":
        #getting the form data
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone = request.form.get("phone")
        username_input = request.form.get("username")
        password_input = request.form.get("password")

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM user WHERE username = %s"
                cursor.execute(sql, (username_input,))
                user = cursor.fetchone()
                if user == None:
                    with conn.cursor() as cursor:
                        sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
                        cursor.execute(sql, (username_input, password_input,))
                        conn.commit()
                        sql = "SELECT * FROM user WHERE username = %s"
                        cursor.execute(sql, (username_input,))
                        user = cursor.fetchone()
                        sql = "INSERT INTO client (user_id, first_name, last_name,phone) VALUES ( %s, %s, %s, %s)"
                        cursor.execute(sql, (user['id'],first_name, last_name, phone,))
                        conn.commit()
                        flash("Registration successful","success")
                        return redirect(url_for("index"))
                else:
                    flash('User already exists','danger')                   
        finally:
            conn.close()      
    return render_template("userreg.html")

if __name__=="__main__":
    app.run(debug=True)