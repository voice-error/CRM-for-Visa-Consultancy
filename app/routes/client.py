from flask import Flask, session,render_template,flash, request,redirect,url_for
import secrets
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)

app.route("/client", methods =["GET", "POST"])
def clientDashbord():
        if 'user_id' in session:
            return render_template("client/client.html")
        else:
            flash('Session Expired', 'info')
            return redirect(url_for("index"))


app.route("/clientChat", methods =["GET", "POST"])
def clientChat():
        if 'user_id' in session:
            return render_template("client/chatwithagent.html")
        else:
            flash(f'Session for {session["first_name"]} has expired', 'info')
            return redirect(url_for("index"))
        
app.route("/clientviewprogress", methods =["GET", "POST"])
def clientViewProgress():
        if 'user_id' in session:
            return render_template("client/checkprogress.html")
        else:
            flash(f'Session for {session["first_name"]} has expired', 'info')
            return redirect(url_for("index"))
        

if __name__=="__main__":
    app.run(debug=True)