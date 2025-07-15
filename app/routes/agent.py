from flask import Flask, session,render_template,flash, request,redirect,url_for
import secrets
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)

app.route("/agent", methods =["GET", "POST"])
def agentDashbord():
        if 'user_id' in session:          
            return render_template("agent/agent.html")
        else:
            flash('Session Expired', 'info')
            return redirect(url_for("index"))

app.route("/viewclients", methods =["GET", "POST"])
def viewClients():
    if 'user_id' in session:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = """SELECT
                                    a.client_id,c.first_name,c.last_name,a.progress,a.apply_date
                                    FROM visa_application AS a
                                    INNER JOIN
                                    client AS c ON a.client_id = c.id
                                    where a.agent_id = %s
                            """
                    cursor.execute(sql, (session['agent_id'],))
                    clients = cursor.fetchall()
                    return render_template("agent/viewClients.html", clients = clients)
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for("agentDashbord"))
    else:
        flash('Session Expired', 'info')
        return redirect(url_for("index"))

app.route("/updateprogress/<int:client_id>", methods =["GET", "POST"])
def updateProgress(client_id):
    if 'user_id' in session:
        # getting the client info
        try:                
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql = """SELECT
                                        c.id,c.first_name,a.progress
                                        FROM visa_application AS a
                                        INNER JOIN
                                        client AS c ON a.client_id = c.id
                                        where a.client_id = %s
                                """
                        cursor.execute(sql, (client_id,))
                        client = cursor.fetchone()                    
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for("agentDashbord"))
        
        if request.method =="POST":
            progress = request.form.get("progress")
            if progress == 'in progress' or progress == 'verifying documents' or progress == 'completed' or progress == 'rejected':
                try:
                    with get_connection() as conn:
                        with conn.cursor() as cursor:
                            sql = "UPDATE visa_application SET progress = %s WHERE client_id = %s"
                            cursor.execute(sql, (progress, client_id,))
                            conn.commit()
                            flash("Progress Updated","success")
                            return render_template("agent/updateProgress.html", client = client)
                except Exception as e:
                    flash('Error: {}'.format(e), 'danger')
                    return redirect(url_for("agentDashbord"))
            else:
                flash("Invalid Progress","danger")
                return redirect(url_for("updateProgress"))        
        else:
            return render_template("agent/updateProgress.html", client = client)
    else:
        flash('Session Expired', 'info')
        return redirect(url_for("index"))

app.route("/report", methods =["GET", "POST"])
def submitReport():
    if 'user_id' in session:
        if request.method =="POST":
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:                        
                        report = request.form.get("report")
                        sql = "INSERT INTO agent_report (agent_id, content) VALUES (%s, %s)"
                        cursor.execute(sql, (session['agent_id'],report,))
                        conn.commit()
                        flash("Report Submitted","success")
                        return redirect(url_for("agentDashbord"))
            except Exception as e:
                flash('Error: {}'.format(e), 'danger')
                return redirect(url_for("agentDashbord"))
        else:
            return render_template("agent/dailyReport.html")
    else:
        flash('Session Expired', 'info')
        return redirect(url_for("index"))      

app.route("/updatesales", methods =["GET", "POST"])
def updateSales():
    if 'user_id' in session:
        if request.method =="POST":
            try:
                clientID = (request.form.get("clientID"))
            except ValueError:
                flash("Invalid Client ID", "danger")
                return redirect(url_for("updateSales"))
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql = "SELECT * FROM sales WHERE client_id = %s"
                        cursor.execute(sql, (clientID,))
                        sales = cursor.fetchone()
                        if sales == None:
                            flash('Client  not found', 'danger')
                            return redirect(url_for("updateSales"))
                        else:
                            session['client_id'] = clientID
                            return redirect(url_for("updateSales1"))
            except Exception as e:
                flash('Error1: {}'.format(e), 'danger')
                return redirect(url_for("agentDashbord"))
        else: 
            return render_template("agent/updateSales.html")
    else:
        flash('Session Expired', 'info')
        return redirect(url_for("index"))
    
@app.route("/updatesales1", methods=["GET", "POST"])  
def updateSales1():
    if 'user_id' in session:
        if request.method =="POST":
            client_id = session['client_id']              
            paid = request.form.get("paid")
            valid_fields = ['registration', 'doc_process', 'visa_process', 'consulting']

            if paid not in valid_fields:
                flash("Invalid field", "danger")
                return redirect(url_for("updateSales1"))
        
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql_get = "SELECT registration, doc_process, visa_process, consulting, remaining FROM sales WHERE client_id = %s"
                        cursor.execute(sql_get, (client_id,))
                        result = cursor.fetchone()

                        if result:
                            # registration, doc_process, visa_process, consulting, remaining = result
                            if paid == 'registration':
                                paid_value = result.get('registration')
                            elif paid == 'doc_process':
                                paid_value = result.get('doc_process')
                            elif paid == 'visa_process':
                                paid_value = result.get('visa_process')
                            elif paid == 'consulting':
                                paid_value = result.get('consulting')
                            remaining_value = result.get('remaining')       
                            new_remaining = float(remaining_value) - float(paid_value)
                            sql_update = "UPDATE sales SET {} = 0, remaining = %s WHERE client_id = %s".format(paid)
                            cursor.execute(sql_update, (new_remaining, client_id))
                            conn.commit()
                            flash("Sales Updated", "success")
                        else:
                            flash("client not found", "danger")
                        return redirect(url_for("updateSales"))
            except Exception as e:
                flash('Error2: {}'.format(e), 'danger')
                return redirect(url_for("agentDashbord"))
        else:
            client_id = session['client_id']
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql = f"SELECT registration,doc_process,visa_process,consulting FROM sales WHERE client_id = {client_id}"
                        cursor.execute(sql)
                        sales = cursor.fetchone()

                        sql = "SELECT * FROM sales WHERE client_id = %s"
                        cursor.execute(sql, (client_id,))
                        client = cursor.fetchone()

                        unpaid = []
                        if sales:
                            columns = ['registration','doc_process','visa_process','consulting']
                            unpaid = [col for col, val in zip(columns, sales) if val != 0]
                            return render_template("agent/updateSales1.html", unpaid=unpaid,client = client)
            except Exception as e:
                flash('Error3: {}'.format(e), 'danger')
                return redirect(url_for("agentDashbord"))
    else:
        flash('Session Expired', 'info')
        return redirect(url_for("index"))




if __name__=='__main__':
    app.run(debug=True)