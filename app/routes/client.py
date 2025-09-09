from flask import Flask, session,render_template,flash, request,redirect,url_for
import secrets
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/client", methods =["GET", "POST"])
def clientDashboard():
        if 'client_id' in session:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT status FROM unverified WHERE user_id = %s"
                    cursor.execute(sql, (session['user_id'],))
                    unver_user = cursor.fetchone()
                    if unver_user:
                        if unver_user['status'] == 0:
                            session['dashboard'] = "rejectedDashboard"
                            flash(f'{session["first_name"]} your application has been rejected', 'info')
                            return redirect(url_for("rejectedDashboard"))
            return render_template("client/client.html")
        else:
            flash('Valid user not found', 'info')
            return redirect(url_for("index"))


@app.route("/clientChat", methods =["GET", "POST"])
def clientChat():
        if 'client_id' in session:
            return render_template("client/chatwithagent.html")
        else:
            flash(f'Session for {session["first_name"]} has expired', 'info')
            return redirect(url_for("index"))
        
@app.route("/clientviewprogress", methods =["GET", "POST"])
def clientViewProgress():        
    if 'client_id' not in session:
        flash('Valid user not found', 'info')
        return render_template("login.html")

    client_id = session['client_id']
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql ="""SELECT * FROM visa_application WHERE client_id = %s"""
            cursor.execute(sql,(client_id,))
            records = cursor.fetchone()
            return render_template('client/checkprogress.html', records=records)

@app.route("/user", methods =["GET", "POST"])
def userDashboard():
        if 'user_id' in session:
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql = 'SELECT status FROM unverified where user_id = %s'                             
                        cursor.execute(sql, (session['user_id'],))
                        unregistered_client = cursor.fetchone()
                        sql = 'SELECT status  FROM unverified_agent where user_id = %s'                                
                        cursor.execute(sql, (session['user_id'],))
                        unregistered_agent = cursor.fetchone()
            except Exception as e:
                flash('Error: {}'.format(e), 'danger')
                return redirect(url_for("index"))
            status_client = unregistered_client['status'] if unregistered_client else None
            status_agent = unregistered_agent['status'] if unregistered_agent else None

            if status_client == 1 or status_agent == 1:
                return render_template("client/user.html")
            else:
                session.clear()
                flash('Critical change detected', 'info')
                return redirect(url_for("index"))
        else:
            flash('Valid user not found', 'info')
            return redirect(url_for("index"))

@app.route("/rejectedDashboard", methods =["GET", "POST"])
def rejectedDashboard():
    if 'user_id' in session:
        if session['dashboard'] != "rejectedDashboard":
            flash('Unauthorized access', 'info')
            return redirect(url_for("index"))
        if request.method != "POST":
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql = "select first_name, last_name,email,phone from unverified where user_id =  %s"
                        cursor.execute(sql, (session['user_id'],))
                        data = cursor.fetchone()
            except Exception as e:
                flash('Error: {}'.format(e), 'danger')
                return redirect(url_for("index"))
            
            return render_template("client/rejectedDashboard.html",data=data)
        elif request.method == "POST":
            if 'user_id' in session:
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                phone = request.form.get("phone")
                username_input = request.form.get("email")
                try:
                    with get_connection() as conn:
                        with conn.cursor() as cursor: 
                            sql = "Update unverified set first_name = %s, last_name = %s ,email = %s,phone =%s,status = %s  where user_id = %s"
                            cursor.execute(sql, (first_name, last_name,username_input, phone,1,session['user_id']))
                            conn.commit()
                            sql = "Update user set username = %s where id = %s"
                            cursor.execute(sql, (username_input,session['user_id']))
                            conn.commit()
                            session['dashboard'] = "userDashboard"
                except Exception as e:
                    flash('Error: {}'.format(e), 'danger')
                    return redirect(url_for("index"))
                return redirect(url_for(session["dashboard"]))
        return redirect(url_for("index"))
    else:
        flash('Unauthorized access', 'info')
        return redirect(url_for("index"))
    
@app.route("/rejectedAgentDashboard", methods =["GET", "POST"])
def rejectedAgentDashboard():
    if 'user_id' in session:
        if session['dashboard'] != "rejectedAgentDashboard":
            flash('Unauthorized access', 'info')
            return redirect(url_for("index"))
        if request.method != "POST":
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql = "select first_name, last_name,email,phone from unverified_agent where user_id =  %s"
                        cursor.execute(sql, (session['user_id'],))
                        data = cursor.fetchone()
            except Exception as e:
                flash('Error: {}'.format(e), 'danger')
                return redirect(url_for("index"))
            
            return render_template("agent/rejectedAgentDashboard.html",data=data)
        elif request.method == "POST":
            if 'user_id' in session:
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                phone = request.form.get("phone")
                username_input = request.form.get("email")
                try:
                    with get_connection() as conn:
                        with conn.cursor() as cursor: 
                            sql = "Update unverified_agent set first_name = %s, last_name = %s ,email = %s,phone =%s,status = %s  where user_id = %s"
                            cursor.execute(sql, (first_name, last_name,username_input, phone,1,session['user_id']))
                            conn.commit()
                            sql = "Update user set username = %s where id = %s"
                            cursor.execute(sql, (username_input,session['user_id']))
                            conn.commit()
                            session['dashboard'] = "userDashboard"
                except Exception as e:
                    flash('Error: {}'.format(e), 'danger')
                    return redirect(url_for("index"))
                return redirect(url_for(session["dashboard"]))
        return redirect(url_for("index"))
    else:
        flash('Unauthorized access', 'info')
        return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug=True)