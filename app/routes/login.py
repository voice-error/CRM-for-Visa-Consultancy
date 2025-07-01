from flask import Flask, render_template,flash, request
import secrets
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)




@app.route("/")
@app.route("/login", methods =["GET", "POST"])
def index():
    if request.method =="POST":
        #getting the form data
        username_input = request.form.get("username")
        password_input = request.form.get("password")
            
        
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM user WHERE username = %s"
                    cursor.execute(sql, (username_input,))
                    user = cursor.fetchone()
                    if user == None:
                        flash('Invalid username or password', 'danger')
                    else:
                        if username_input==(user['username']) and password_input==(user['password']):
                            role = user['role_id']
                            if role == 3:
                                flash('Welcome  Admin', 'success')
                                return render_template("admin.html")
                            elif role == 2:
                                flash('Welcome  Agent ', 'success')
                                return render_template("agent.html")
                            elif role == 4:
                                flash('Welcome  User', 'success')
                                return render_template("user.html")
                            elif role == 1:
                                flash('Welcome Client', 'success')
                                return render_template("client.html")
                            else:
                                flash('Unknown role.', 'danger')
                                return render_template("login.html")
                        else:
                            flash('Invalid username or password', 'danger')
                            return render_template("login.html")
        except Exception as e:
            flash("503 Service Unavailable", 'info')
    return render_template("login.html")


if __name__=="__main__":
    app.run(debug=True)