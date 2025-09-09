from flask import Flask, render_template,flash, request,redirect,url_for
import secrets
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/userreg", methods =["GET", "POST"])
def register():
    if request.method =="POST" :      
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone = request.form.get("phone")
        username_input = request.form.get("email")
        password_input = request.form.get("password")
        message = request.form.get("notes")
        program_id = request.form.get("program")
        visa_type = request.form.get("visa_type")
        country_id = request.form.get("country")
        university_id = request.form.get("university")

        
        try:
            with get_connection() as conn:
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
                            sql = "INSERT INTO unverified (user_id, first_name, last_name,email,phone,visa_type,country_id,university_id,program_id,notes) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(sql, (user['id'],first_name, last_name,username_input, phone,visa_type,country_id,university_id,program_id,message,))
                            conn.commit()
                            flash("Registration successful","success")
                            return redirect(url_for("index"))
                    else:
                        flash('User already exists','danger')                   
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
    else:
        return render_template("userregistration.html")
    
@app.route("/agentreg", methods =["GET", "POST"])
def registerAgent():
    if request.method =="POST" :      
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone = request.form.get("phone")
        username_input = request.form.get("email")
        password_input = request.form.get("password")
        message = request.form.get("notes")

        
        try:
            with get_connection() as conn:
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
                            sql = "INSERT INTO unverified_agent (user_id, first_name, last_name,email,phone,notes) VALUES ( %s, %s, %s, %s, %s, %s)"
                            cursor.execute(sql, (user['id'],first_name, last_name,username_input, phone,message,))
                            conn.commit()
                            flash("Registration successful","success")
                            return redirect(url_for("index"))
                    else:
                        flash('User already exists','danger')                   
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
    else:
        return render_template("agentregistration.html")    
    

@app.route("/usertype", methods =["GET", "POST"])
def usertype():
    if request.method == "POST":
        usertype = request.form.get("user_type")
        if usertype == "agent":
            return render_template("agentregistration.html")
        if usertype == "client":
            return render_template("userregistration.html")
        else:
            flash('Invalid user type', 'danger')
            return redirect(url_for("index"))
    return render_template("userreg.html")

if __name__=="__main__":
    app.run(debug=True)