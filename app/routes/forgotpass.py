from flask import Flask, session,render_template,flash, request,redirect,url_for
from flask_mail import Mail,Message
import secrets,random,string,os
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)
mail=Mail(app)
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # SMTP Server
app.config["MAIL_PORT"] = 587  # Port for TLS
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "prabinlamichhane@nast.edu.np"  # Your email
app.config["MAIL_PASSWORD"] = "your_password"  # App password or actual password
app.config["MAIL_DEFAULT_SENDER"] = "your_email@gmail.com"

app.route("/forgotpass", methods =["POST"])
def generate_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=5))

def forgotpassEmail():
    if request.method == "POST":
        email = request.form.get("email")
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM users WHERE email = %s"
                    cursor.execute(sql, (email,))
                    user = cursor.fetchone()
                    if user:
                        session['user_id'] = user['id']
                        code = generate_code()
                        sql ="Insert into passreset (user_id, reset_code) values (%s, %s)"
                        cursor.execute(sql, (session['user_id'], code))
                        conn.commit()

                        return redirect(url_for("resetpass2"))
                    else:
                        flash('Email not found', 'danger')
                        return redirect(url_for("forgotpass"))          
        except Exception as e:
            flash('504 internal server error', 'danger')
            return redirect(url_for("index"))                        
    else:
        return render_template("forgotpass.html")
    
if __name__ == '__main__':
    app.config['SECRET_KEY'] = secrets.token_hex(16)