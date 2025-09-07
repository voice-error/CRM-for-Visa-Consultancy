from flask import Flask, session,render_template,flash, request,redirect,url_for,current_app
from flask_mail import Mail,Message
import secrets,random,string,os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join("crmEnv", ".env"))
from app.backend.connection import get_connection



app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("sender_email")
app.config["MAIL_PASSWORD"] = os.getenv("sender_pass")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("sender_email")

mail = Mail(app)
def generate_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=5))

@app.route("/forgotpass", methods =["GET","POST"])
def forgotpassEmail():
    if 'code_status' in session and session['code_status']:
        return redirect(url_for("forgotpassCode"))
    
    elif request.method == "POST":
        email = request.form.get("email")
        if email:
            email=email.lower()
            session[email]  = email
        else:
            flash('Enter your email', 'info')
            return redirect(url_for("forgotpassEmail"))
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM user WHERE username = %s"
                    cursor.execute(sql, (email,))
                    user = cursor.fetchone()
                    if user:
                        user_id = user['id']
                        session['userid'] = user_id
                        code = generate_code()
                        sql ="Insert into passreset (user_id, reset_code) values (%s, %s) ON DUPLICATE KEY UPDATE reset_code = %s"
                        cursor.execute(sql, (user_id, code,code))
                        conn.commit()
                        try:
                            msg = Message(subject="Password Reset Code For Visa application",recipients=[email])
                            msg.body = "you have requested to reset your password, your reset code is "+code
                            mail.send(msg)
                            session['code_status'] = True
                            return render_template("forgotpass2.html")
                        except Exception as e:
                            flash("mail part ko error", 'danger')
                            return redirect(url_for("index"))
                    else:
                        flash('Email not found', 'danger')
                        return redirect(url_for("forgotpassEmail"))          
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for("index"))                        
    else:
        return render_template("forgotpass.html")
@app.route("/forgotpasscode", methods =["GET","POST"])   
def forgotpassCode():
    if request.method != "POST":
        return render_template("forgotpass2.html")
    elif not(session['code_status']):
        return render_template("forgotpass2.html")
    else:
        code = request.form.get("code")
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM passreset WHERE user_id = %s"
                    cursor.execute(sql, (session['userid'],))
                    restuser = cursor.fetchone()
                    if code == restuser['reset_code']:
                        session['status'] = True
                        return redirect(url_for("forgotpassChange"))
                    else:
                        flash('Invalid Code, Check your email '+session['email']+" for code", 'danger')
                        return redirect(url_for("forgotpassCode"))
        except Exception as e:
            flash('Connection ERROR', 'danger')
            return redirect(url_for("index"))
@app.route("/forgotpassChange", methods =["GET","POST"])
def forgotpassChange():
    if request.method != "POST":
        return render_template("reset_password.html")
    elif session['status']:
        password = request.form.get("new_password")
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "UPDATE user SET password = %s WHERE id = %s"
                    cursor.execute(sql, (password, session['userid'],))
                    conn.commit()
                    sql = "DELETE FROM passreset WHERE user_id = %s"
                    cursor.execute(sql, (session['userid'],))
                    conn.commit()
                    session.clear()
                    flash('Password changed successfully', 'success')
                    return redirect(url_for("index"))
        except Exception as e:
            flash('Connection ERROR', 'danger')
            return redirect(url_for("index"))
    else:
        return render_template("reset_password.html")

# @app.route("/testmail")
# def test_mail():
#     print("Current extensions:", current_app.extensions)
#     msg = Message("Test Email", recipients=['prabin700003@gmail.com'])
#     msg.body = "This is a test."
#     print("Server:", app.config["MAIL_SERVER"])
#     print("Port:", app.config["MAIL_PORT"], type(app.config["MAIL_PORT"]))
#     print("Username:", app.config["MAIL_USERNAME"])
#     print("Default sender:", app.config["MAIL_DEFAULT_SENDER"])
#     print("Recipients:", msg.recipients)
#     mail.send(msg)
#     return "Mail sent!"

    
if __name__ == '__main__':
    app.run(debug=True)

