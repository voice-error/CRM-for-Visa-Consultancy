from flask import Flask, session,render_template,flash, request,redirect,url_for
import secrets
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/client", methods =["GET", "POST"])
def clientDashboard():
        if 'user_id' in session:
            return render_template("client/client.html")
        else:
            flash('Session Expired', 'info')
            return redirect(url_for("index"))


@app.route("/clientChat", methods =["GET", "POST"])
def clientChat():
        if 'user_id' in session:
            return render_template("client/chatwithagent.html")
        else:
            flash(f'Session for {session["first_name"]} has expired', 'info')
            return redirect(url_for("index"))
        
@app.route("/clientviewprogress", methods =["GET", "POST"])
def clientViewProgress():        
    if 'user_id' not in session:
        flash('Session Expired', 'info')
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
            return render_template("client/user.html")
        else:
            flash('Session Expired', 'info')
            return redirect(url_for("index"))
        

if __name__=="__main__":
    app.run(debug=True)