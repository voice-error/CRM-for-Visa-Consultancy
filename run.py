from flask import Flask
from app.routes import login,userreg,client,agent,forgotpass,admin
import os
from flask_mail import Mail
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join("crmEnv", ".env"))
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(16)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("sender_email")
app.config["MAIL_PASSWORD"] = os.getenv("sender_pass")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("sender_email")

mail = Mail(app)



print("TEMPLATE DIR:", os.path.abspath("app/templates"))
print("Files in template dir:", os.listdir("app/templates"))

# # Register routes defined in other files
app.add_url_rule("/", view_func=login.index, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=login.index, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=login.logout, methods=["GET", "POST"])
app.add_url_rule("/userreg", view_func=userreg.register, methods=["GET", "POST"])
app.add_url_rule("/client", view_func=client.clientDashboard, methods=["GET", "POST"])
app.add_url_rule("/clientChat", view_func=client.clientChat, methods=["GET", "POST"])
app.add_url_rule("/clientViewProgress", view_func=client.clientViewProgress, methods=["GET", "POST"])
app.add_url_rule("/agent", view_func=agent.agentDashboard, methods=["GET", "POST"])
app.add_url_rule("/viewclients", view_func=agent.viewClients, methods=["GET", "POST"])
app.add_url_rule("/updateprogress/<int:client_id>", view_func=agent.updateProgress, methods=["GET", "POST"])
app.add_url_rule("/report", view_func=agent.submitReport, methods=["GET", "POST"])
app.add_url_rule("/updatesales", view_func=agent.updateSales, methods=["GET", "POST"])
app.add_url_rule("/updatesales1", view_func=agent.updateSales1, methods=["GET", "POST"])
app.add_url_rule("/user", view_func=client.userDashboard, methods=["GET", "POST"])
app.add_url_rule("/forgotpass", view_func=forgotpass.forgotpassEmail, methods=["GET", "POST"])
app.add_url_rule("/forgotpasscode", view_func=forgotpass.forgotpassCode, methods=["GET", "POST"])
app.add_url_rule("/forgotpassChange", view_func=forgotpass.forgotpassChange, methods=["GET", "POST"])
app.add_url_rule("/admin", view_func=admin.adminDashboard, methods=["GET", "POST"])
app.add_url_rule("/checkRegistrations", view_func=admin.checkRegistrations, methods=["GET", "POST"])
app.add_url_rule("/reviewApplication/<int:user_id>", view_func=admin.reviewApplication, methods=["GET", "POST"])
app.add_url_rule("/approveApplication/<int:user_id>", view_func=admin.aprove, methods=["GET", "POST"])
app.add_url_rule("/rejectApplication/<int:user_id>", view_func=admin.rejectApplication, methods=["GET", "POST"])
app.add_url_rule("/rejectedDashboard", view_func=client.rejectedDashboard, methods=["GET", "POST"])
app.add_url_rule("/usertype", view_func=userreg.usertype, methods=["GET", "POST"])
app.add_url_rule("/agentreg", view_func=userreg.registerAgent, methods=["GET", "POST"])
app.add_url_rule("/rejectedAgentDashboard", view_func=client.rejectedAgentDashboard, methods=["GET", "POST"])
app.add_url_rule("/approveAgentApplication/<int:user_id>", view_func=admin.aproveAgent, methods=["GET", "POST"])
app.add_url_rule("/rejectAgentApplication/<int:user_id>", view_func=admin.rejectAgentApplication, methods=["GET", "POST"])
app.add_url_rule("/lookClients", view_func=admin.lookClients, methods=["GET", "POST"])
app.add_url_rule("/lookAgents", view_func=admin.lookAgents, methods=["GET", "POST"])
app.add_url_rule("/lookAgents/<int:agent_id>", view_func=admin.lookAgents, methods=["GET", "POST"])



# app.add_url_rule("/testmail", view_func=forgotpass.test_mail, methods=["GET", "POST"])

if (__name__) == "__main__":
    app.run(debug=True)