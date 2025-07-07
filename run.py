from flask import Flask
from app.routes import login,userreg,client  # this will register your routes
import os

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(16)

print("TEMPLATE DIR:", os.path.abspath("app/templates"))
print("Files in template dir:", os.listdir("app/templates"))

# Register routes defined in login.py
app.add_url_rule("/", view_func=login.index, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=login.index, methods=["GET", "POST"])
app.add_url_rule("/userreg", view_func=userreg.register, methods=["GET", "POST"])
app.add_url_rule("/client", view_func=client.clientDashbord, methods=["GET", "POST"])
app.add_url_rule("/clientChat", view_func=client.clientChat, methods=["GET", "POST"])
app.add_url_rule("/clientViewProgress", view_func=client.clientViewProgress, methods=["GET", "POST"])

if (__name__) == "__main__":
    app.run(debug=True)