from flask import Flask,session, render_template,flash, request,redirect,url_for
import secrets
from datetime import timedelta
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)



@app.route("/")
@app.route("/login", methods =["GET", "POST"])
def index():
    if "user_id" in session:
        return redirect(url_for(session['dashboard']))
    
    
    elif request.method =="POST":
        #getting the form data
        username_input = request.form.get("username").lower()
        password_input = request.form.get("password")          
              
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM user WHERE username = %s"
                    cursor.execute(sql, (username_input,))
                    user = cursor.fetchone()
                    if user == None:
                        flash('Invalid username or password', 'danger')                        
                        return render_template("login.html")
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
                                session['last_name'] = user['last_name']
                                session['agent_id'] = user['id']
                                session['dashboard']="agentDashboard"
                                
                                flash(f'Welcome {session["first_name"]}', 'success')
                                return redirect(url_for("agentDashboard"))
                            elif role == 4:
                                sql = "SELECT * FROM unverified WHERE user_id = %s"
                                cursor.execute(sql, (user['id'],))
                                unver_user = cursor.fetchone()

                                if unver_user:
                                    session['first_name'] = unver_user['first_name']
                                    session['last_name'] = unver_user['last_name']
                                    session['dashboard'] = "userDashboard"
                                    flash(f'Welcome {session["first_name"]}', 'success')
                                    return redirect(url_for("userDashboard"))
                                else:
                                    flash("Unverified user not found.", "danger")
                                    return render_template("login.html")                            
                            elif role == 1:
                                sql = "SELECT * FROM client WHERE user_id = %s"
                                cursor.execute(sql, (user['id'],))
                                user = cursor.fetchone()
                                session['first_name'] = user['first_name']
                                session['last_name'] = user['last_name']
                                session['client_id'] = user['id']
                                session['dashboard']="clientDashboard"
                                flash(f'Welcome {session["first_name"]}', 'success')
                                return redirect(url_for("clientDashboard"))
                            else:
                                flash('Unknown role.', 'danger')
                                return render_template("login.html")
                        else:
                            flash('Invalid username or password', 'danger')
                            return render_template("login.html")
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
    return render_template("login.html")
    

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug=True)