from flask import Flask,session, render_template,flash, request,redirect,url_for
import secrets
from datetime import timedelta
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['PERSISTENT_SESSIONS'] = timedelta(minutes = 1)



@app.route("/")
@app.route("/login", methods =["GET", "POST"])
def index():
    if "user_id" in session:
        return redirect(url_for(session['dashbord']))
    
    elif request.method =="POST":
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
                            session['user_id'] = user['id']                            
                            role = user['role_id']
                            if role == 3:
                                flash('Welcome  Admin', 'success')
                                return render_template("admin/admin.html")
                            elif role == 2:
                                sql = "SELECT * FROM agent WHERE user_id = %s"
                                cursor.execute(sql, (user['id'],))
                                user = cursor.fetchone()
                                session['first_name'] = user['first_name']

                                sql = """SELECT id FROM agent WHERE user_id = %s """
                                cursor.execute(sql, (session['user_id'],))
                                agent = cursor.fetchone()
                                session['agent_id'] = agent['id']

                                session['dashbord']="agentDashbord"
                                
                                flash(f'Welcome {session["first_name"]}', 'success')
                                return redirect(url_for("agentDashbord"))
                            elif role == 4:
                                flash('Welcome  User', 'success')
                                return render_template("client/user.html")
                            elif role == 1:
                                sql = "SELECT * FROM client WHERE user_id = %s"
                                cursor.execute(sql, (user['id'],))
                                user = cursor.fetchone()
                                session['first_name'] = user['first_name']
                                session['dashbord']="clientDashbord"
                                flash(f'Welcome {session["first_name"]}', 'success')
                                return redirect(url_for("clientDashbord"))
                            else:
                                flash('Unknown role.', 'danger')
                                return render_template("login.html")
                        else:
                            flash('Invalid username or password', 'danger')
                            return render_template("login.html")
        except Exception as e:
            flash("503 Service Unavailable", 'danger')
            return render_template("login.html")
    else:
        flash('Session Expired', 'info')    
        return render_template("login.html")


if __name__=="__main__":
    app.run(debug=True)