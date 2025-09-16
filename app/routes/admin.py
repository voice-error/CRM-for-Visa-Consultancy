from flask import Flask, session,render_template,flash, request,redirect,url_for
import secrets
from app.backend.connection import get_connection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/admin", methods =["GET", "POST"])
def adminDashboard():
        if 'admin_id' in session:          
            return render_template("admin/admin.html")
        else:
            flash('Valid user not found', 'info')
            return redirect(url_for("index"))

@app.route("/checkRegistrations", methods =["GET", "POST"] )
def checkRegistrations():
    if 'admin_id' in session:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = 'SELECT id,username FROM user WHERE id IN (SELECT user_id FROM unverified where status = %s)'                             
                cursor.execute(sql, (1,))
                unregistered_client = cursor.fetchall()
                sql = 'SELECT id,username FROM user WHERE id IN (SELECT user_id FROM unverified_agent where status = %s)'                             
                cursor.execute(sql, (1,))
                unregistered_agent = cursor.fetchall()
                unregistered = unregistered_client + unregistered_agent
                if unregistered == None:
                    flash('No Registrations', 'info')
                return render_template("admin/checkReg.html", users = unregistered)
    else:
        flash('Valid user not found', 'info')
        return redirect(url_for("index"))
                
@app.route("/reviewApplication/<int:user_id>", methods =["GET", "POST"] )
def reviewApplication(user_id):
    if 'admin_id' in session:

        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM unverified WHERE user_id = %s"
                    cursor.execute(sql, (user_id,))
                    user = cursor.fetchone()
                    sql = "SELECT * FROM unverified_agent WHERE user_id = %s"
                    cursor.execute(sql, (user_id,))
                    agent = cursor.fetchone()
                    if user:
                        sql = "SELECT name as country FROM country WHERE id = %s"
                        cursor.execute(sql, (user['country_id'],))
                        country = cursor.fetchone()
                        sql = "SELECT name as university FROM university WHERE id = %s"
                        cursor.execute(sql, (user['university_id'],))
                        university = cursor.fetchone()
                        sql = "SELECT name as program FROM program WHERE id = %s"
                        cursor.execute(sql, (user['program_id'],))
                        program = cursor.fetchone()
                        user = user|country|university|program
                        return render_template("admin/reviewApplication.html", user = user)
                    elif agent:
                        return render_template("admin/reviewAgentApplication.html", user = agent)
                    else :
                        flash('User not found', 'info')
                        return redirect(url_for("checkRegistrations"))

                
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for("adminDashboard"))
    else:
        flash('Valid user not found', 'info')
        return redirect(url_for("index"))
    
@app.route("/approveApplication/<int:user_id>", methods =["GET", "POST"] )
def aprove(user_id):
    if request.method == 'POST':
        if 'admin_id' in session and 'userkoid' in session:
            agent_id = request.form.get("agent_id")
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql = "SELECT * FROM unverified WHERE user_id = %s"
                        cursor.execute(sql, (user_id,))
                        user = cursor.fetchone()
                        print(user)
                        sql = "INSERT INTO client (user_id, first_name, last_name, phone) VALUES (%s, %s,%s,%s)"
                        cursor.execute(sql, (user['user_id'], user['first_name'], user['last_name'], user['phone'],))
                        conn.commit()
                        sql = "Select id from client where user_id = %s"
                        cursor.execute(sql, (user['user_id'],))
                        client_id = cursor.fetchone()
                        print('ok!!!!!!!!!!!!!')
                        sql = "INSERT INTO visa_application (client_id,agent_id, university_id) VALUES (%s, %s,%s)"
                        cursor.execute(sql, (client_id['id'],agent_id,user['university_id'],))
                        conn.commit()
                        print('ok2!!!!!!!!!!!!!!!!')
                        sql = "INSERT INTO sales (client_id) VALUES (%s)"
                        cursor.execute(sql, (client_id['id'],))
                        conn.commit()
                        sql = "Select * from sales where client_id = %s"
                        cursor.execute(sql, (client_id['id'],))
                        sales = cursor.fetchone()                        
                        sql = "Update sales set remaining = %s where client_id = %s"
                        cursor.execute(sql, ( sales['registration']+sales['doc_process']+sales['visa_process']+sales['consulting'],client_id['id'],))
                        conn.commit()
                        sql = "Update user set role_id = %s where id = %s"
                        cursor.execute(sql, (1 ,user['user_id'],))
                        conn.commit()
                        sql = "DELETE FROM unverified WHERE user_id = %s"
                        cursor.execute(sql, (user_id,))
                        conn.commit()
                        session.pop('userkoid')
                        flash('Application Approved', 'success')
                        return redirect(url_for("adminDashboard"))
            except Exception as e:
                flash('Error: {}'.format(e), 'danger')
                return redirect(url_for("adminDashboard")) 
        else:
            flash('Valid user not found', 'info')
            return redirect(url_for("index"))
    else:
        if 'admin_id' in session:
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql = "SELECT id, first_name, last_name FROM agent"
                        cursor.execute(sql)
                        agent = cursor.fetchall()
            except Exception as e:
                flash('Error: {}'.format(e), 'danger')
                return redirect(url_for("adminDashboard"))
            session['userkoid'] = user_id
            return render_template("admin/assignAgent.html", data = agent)
        else:
            flash('Valid user not found', 'info')
            return redirect(url_for("index")) 

@app.route('/rejectApplication/<int:user_id>', methods =["GET", "POST"] )
def rejectApplication(user_id):
    if 'admin_id' in session:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "Update unverified set status = 0 where user_id = %s"
                    cursor.execute(sql, (user_id,))
                    conn.commit()
                    flash('Application Rejected', 'success')
                    return redirect(url_for("adminDashboard"))
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for("adminDashboard"))
    else:
        flash('Valid user not found', 'info')
        return redirect(url_for("index"))

@app.route("/approveAgentApplication/<int:user_id>", methods =["GET", "POST"] )
def aproveAgent(user_id):
        if 'admin_id' in session and 'userkoid' in session:
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        sql = "SELECT * FROM unverified_agent WHERE user_id = %s"
                        cursor.execute(sql, (user_id,))
                        user = cursor.fetchone()
                        print(user)
                        sql = "INSERT INTO agent (user_id, first_name, last_name, phone) VALUES (%s, %s,%s,%s)"
                        cursor.execute(sql, (user['user_id'], user['first_name'], user['last_name'], user['phone'],))
                        conn.commit()
                        sql = "Update user set role_id = %s where id = %s"
                        cursor.execute(sql, (2 ,user['user_id'],))
                        conn.commit()
                        sql = "DELETE FROM unverified_agent WHERE user_id = %s"
                        cursor.execute(sql, (user_id,))
                        conn.commit()
                        session.pop('userkoid')
                        flash('Application Approved', 'success')
                        return redirect(url_for("adminDashboard"))
            except Exception as e:
                flash('Error: {}'.format(e), 'danger')
                return redirect(url_for("adminDashboard")) 
        else:
            flash('Valid user not found', 'info')
            return redirect(url_for("index")) 

@app.route('/rejectAgentApplication/<int:user_id>', methods =["GET", "POST"] )
def rejectAgentApplication(user_id):
    if 'admin_id' in session:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "Update unverified_agent set status = %s where user_id = %s"
                    cursor.execute(sql, (0,user_id,))
                    conn.commit()
                    flash('Application Rejected', 'success')
                    return redirect(url_for("adminDashboard"))
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for("adminDashboard"))
    else:
        flash('Valid user not found', 'info')
        return redirect(url_for("index"))
    
@app.route("/lookClients", methods =["GET", "POST"] )
def lookClients():
    if 'admin_id' in session:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = """SELECT 
                            u.username,c.user_id,c.first_name,c.last_name,un.name AS university,
                            p.name AS program,co.name AS country,a.progress FROM client c 
                            JOIN visa_application a ON c.id = a.client_id JOIN user u 
                            ON c.user_id = u.id LEFT JOIN university un ON a.university_id = un.id
                            LEFT JOIN program p ON a.program_id = p.id LEFT JOIN country co 
                            ON a.country_id = co.id"""
                    cursor.execute(sql)
                    clients = cursor.fetchall()
                    return render_template("admin/viewClients.html", data = clients)
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for("adminDashboard"))
    else:
        flash('Valid user not found', 'info')
        return redirect(url_for("index"))

@app.route("/lookAgents", methods=["GET"])
@app.route("/lookAgents/<int:agent_id>", methods=["GET"])
def lookAgents(agent_id=None):
    if 'admin_id' not in session:
        return redirect(url_for("adminDashboard"))

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                if agent_id is None:
                    sql = "SELECT * FROM agent"
                    cursor.execute(sql)
                    agents = cursor.fetchall()
                    print(agents)
                    return render_template("admin/viewAgent.html", data=agents)
                else:
                    sql = """
                        SELECT ar.agent_id, a.first_name, a.last_name, a.phone, ar.content, ar.date
                        FROM agent_report ar
                        LEFT JOIN agent a ON ar.agent_id = a.id
                        WHERE ar.agent_id = %s
                        ORDER BY ar.date DESC
                    """
                    cursor.execute(sql, (agent_id,))
                    reports = cursor.fetchall()
                    print(reports)
                    return render_template("admin/agentReports.html", data=reports)
    except Exception as e:
        flash(f"Error 1: {e}", "danger")
        return redirect(url_for("adminDashboard"))


        
if __name__=='__main__':
    app.run(debug=True)