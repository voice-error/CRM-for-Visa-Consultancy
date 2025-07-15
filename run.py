from flask import Flask
from app.routes import login,userreg,client,agent
import os

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
import secrets
app.config['SECRET_KEY'] = "prabin@1234"
# app.config['SECRET_KEY'] = secrets.token_hex(16)

print("TEMPLATE DIR:", os.path.abspath("app/templates"))
print("Files in template dir:", os.listdir("app/templates"))

# Register routes defined in other files
app.add_url_rule("/", view_func=login.index, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=login.index, methods=["GET", "POST"])
app.add_url_rule("/userreg", view_func=userreg.register, methods=["GET", "POST"])
app.add_url_rule("/client", view_func=client.clientDashbord, methods=["GET", "POST"])
app.add_url_rule("/clientChat", view_func=client.clientChat, methods=["GET", "POST"])
app.add_url_rule("/clientViewProgress", view_func=client.clientViewProgress, methods=["GET", "POST"])
app.add_url_rule("/agent", view_func=agent.agentDashbord, methods=["GET", "POST"])
app.add_url_rule("/viewclients", view_func=agent.viewClients, methods=["GET", "POST"])
app.add_url_rule("/updateprogress/<int:client_id>", view_func=agent.updateProgress, methods=["GET", "POST"])
app.add_url_rule("/report", view_func=agent.submitReport, methods=["GET", "POST"])
app.add_url_rule("/updatesales", view_func=agent.updateSales, methods=["GET", "POST"])
app.add_url_rule("/updatesales1", view_func=agent.updateSales1, methods=["GET", "POST"])

if (__name__) == "__main__":
    app.run(debug=True)