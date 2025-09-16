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
                            session['role_id'] = user['role_id']                            
                            role = user['role_id']
                            if role == 3:
                                sql = "SELECT * FROM owner WHERE user_id = %s"
                                cursor.execute(sql, (user['id'],))
                                user = cursor.fetchone()
                                session['first_name'] = user['first_name']
                                session['last_name'] = user['last_name']
                                session['admin_id'] = user['id']
                                session['dashboard']="adminDashboard"
                                
                                flash(f'Welcome {session["first_name"]}', 'success')
                                return redirect(url_for("adminDashboard"))
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
                                sql = "SELECT * FROM unverified_agent WHERE user_id = %s"
                                cursor.execute(sql, (user['id'],))
                                unver_agent = cursor.fetchone()
                                if unver_user:
                                    if unver_user['status'] == 1:
                                        session['first_name'] = unver_user['first_name']
                                        session['last_name'] = unver_user['last_name']
                                        session['dashboard'] = "userDashboard"
                                        flash(f'Welcome {session["first_name"]}', 'success')
                                        return redirect(url_for("userDashboard"))
                                    else:
                                        session['first_name'] = unver_user['first_name']
                                        session['last_name'] = unver_user['last_name']
                                        session['dashboard'] = "rejectedDashboard"
                                        flash(f'{session["first_name"]} your application has been rejected', 'info')
                                        return redirect(url_for("rejectedDashboard"))
                                elif unver_agent:
                                    if unver_agent['status'] == 1:
                                        session['first_name'] = unver_agent['first_name']
                                        session['last_name'] = unver_agent['last_name']
                                        session['dashboard'] = "userDashboard"
                                        flash(f'Welcome {session["first_name"]}', 'success')
                                        return redirect(url_for("userDashboard"))
                                    else:
                                        session['first_name'] = unver_agent['first_name']
                                        session['last_name'] = unver_agent['last_name']
                                        session['dashboard'] = "rejectedAgentDashboard"
                                        flash(f'{session["first_name"]} your application has been rejected', 'info')
                                        return redirect(url_for("rejectedAgentDashboard"))    
                                else:
                                    flash("Unverified user not found.", "danger")
                                    return redirect(url_for("index"))                            
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