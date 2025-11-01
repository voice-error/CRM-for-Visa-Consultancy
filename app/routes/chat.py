from flask import session, render_template, flash, request, redirect, url_for
import  random, string
from app.backend.connection import get_connection
from flask_socketio import join_room, emit
def init_chat_routes(app, socketio):
    def generate_code():
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=5))

    @app.route("/get_or_create_code", methods =["GET", "POST"])
    def get_or_create_code():
        if 'user_id' not in session:
            flash('Valid user not found', 'info')
            return redirect(url_for("index"))
        if 'client_id' in session:
            try:
                with get_connection() as conn: 
                    with conn.cursor() as cursor:
                        sql = "SELECT agent_id FROM visa_application WHERE client_id = %s"
                        cursor.execute(sql, (session['client_id'],))
                        agent = cursor.fetchone()
                        print(agent)
                        session['agentko_id'] = agent['agent_id']
                        sql = "SELECT id,created_on FROM chat_room WHERE client_id = %s AND agent_id = %s"
                        cursor.execute(sql, (session['client_id'],session['agentko_id'],))
                        data = cursor.fetchone()
                        print('pass00')
                        if data:
                            session['room_id'] = data['id']
                            session['created_on'] = data['created_on']
                        else:
                            while True:
                                room_id = generate_code()
                                sql = "SELECT id FROM chat_room WHERE id = %s"
                                cursor.execute(sql, (room_id,))
                                if not cursor.fetchone():
                                    break
                            sql = "INSERT INTO chat_room (id,client_id,agent_id) VALUES (%s,%s,%s)"
                            cursor.execute(sql, (room_id,session['client_id'],session['agentko_id'],))
                            conn.commit()
                            print('pass1')
                            sql = "SELECT id,created_on FROM chat_room WHERE client_id = %s AND agent_id = %s"
                            cursor.execute(sql, (session['client_id'],session['agentko_id'],))
                            data = cursor.fetchone()
                            print(data)
                            session['room_id'] = data['id']
                            session['created_on'] = data['created_on']
            except Exception as e:
                flash('Error1: {}'.format(e), 'danger')
                return redirect(url_for("index"))
            return redirect(url_for("chat_room", room_id=session['room_id']))
        else:
            flash('Valid user not found', 'info')
            return redirect(url_for("index"))



    @app.route("/get_create_code/<int:client_id>", methods =["GET", "POST"])
    def get_create_code(client_id):
        if 'user_id' not in session:
            flash('Valid user not found', 'info')
            return redirect(url_for("index"))
        if 'agent_id' in session:
            try:
                with get_connection() as conn: 
                    with conn.cursor() as cursor:
                        sql = "SELECT id,created_on FROM chat_room WHERE client_id = %s AND agent_id = %s"
                        cursor.execute(sql, (client_id,session['agent_id'],))
                        data = cursor.fetchone()
                        if data:
                            session['room_id'] = data['id']
                            session['created_on'] = data['created_on']
                        else:
                            while True:
                                room_id = generate_code()
                                sql = "SELECT id FROM chat_room WHERE id = %s"
                                cursor.execute(sql, (room_id,))
                                if not cursor.fetchone():
                                    break    
                            sql = "INSERT INTO chat_room (id,client_id,agent_id) VALUES (%s,%s,%s)"
                            cursor.execute(sql, (room_id,client_id,session['agent_id'],))
                            conn.commit()
                            sql = "SELECT id,created_on FROM chat_room WHERE client_id = %s AND agent_id = %s"
                            cursor.execute(sql, (client_id,session['agent_id'],))
                            data = cursor.fetchone()
                            session['room_id'] = data['id']
                            session['created_on'] = data['created_on']
                            session['clientko_id'] = client_id
            except Exception as e:
                flash('Error2: {}'.format(e), 'danger')
                return redirect(url_for("index"))
            return redirect(url_for("chat_room", room_id=session['room_id']))
        else:
            flash('Valid user not found', 'info')
            return redirect(url_for("index"))

    @app.route("/chatroom/<string:room_id>")
    def chat_room(room_id):
        user_id = session.get("user_id")
        if not user_id:
            flash("You must be logged in to view a chat room.", "warning")
            return redirect(url_for("index"))

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                sql = "SELECT client_id, agent_id FROM chat_room WHERE id = %s"
                cur.execute(sql, (room_id,))
                room = cur.fetchone()

                if not room:
                    flash("Room not found.", "info")
                    return redirect(url_for("index"))

                is_client_in_room = 'client_id' in session and room["client_id"] == session['client_id']
                is_agent_in_room = 'agent_id' in session and room["agent_id"] == session['agent_id']

                if not (is_client_in_room or is_agent_in_room):
                    flash('Access denied.', 'danger')
                    return redirect(url_for("index"))


                sql = """
                    SELECT
                        cm.message,
                        cm.sent_on,
                        cm.sender_id,
                        -- Use COALESCE to get the name from whichever table has a match
                        COALESCE(c.first_name, a.first_name) AS first_name,
                        COALESCE(c.last_name, a.last_name) AS last_name
                    FROM
                        chat_message cm
                    LEFT JOIN
                        client c ON cm.sender_id = c.user_id  -- CORRECTED LINE
                    LEFT JOIN
                        agent a ON cm.sender_id = a.user_id   -- CORRECTED LINE
                    WHERE
                        cm.room_id = %s
                    ORDER BY
                        cm.sent_on ASC;
                """
                cur.execute(sql, (room_id,))
                messages = cur.fetchall()

        except Exception as e:
            flash(f'Error loading chat: {e}', 'danger')
            return redirect(url_for("index"))

        
        return render_template("chatwithagent.html",room_id=room_id, messages=messages,current_username=session.get("first_name"))

    def save_message(room_id, sender_id, message):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                sql ="""INSERT INTO chat_message (room_id, sender_id, message)
                    VALUES (%s, %s, %s)"""
                cursor.execute(sql, (room_id, sender_id, message))
                conn.commit()
        except Exception as e:
            flash('Error6: {}'.format(e), 'danger')
            return redirect(url_for("index"))

    @socketio.on("join")
    def on_join(data):
        username = session.get("first_name", "A user")
        room_id = data.get("room")

        if not room_id:
            print("Join attempt failed: No room_id provided.")
            return
           

        join_room(room_id)
        emit("status", {"msg": f"{username} has joined the room."}, room=room_id)
        print(f"'{username}' joined room '{room_id}'")

    @socketio.on("send_message")
    def handle_message(data):
        user_id = session.get("user_id")
        first_name = session.get("first_name", "")
        last_name = session.get("last_name", "")
        room_id = session.get("room_id")
        message = data["message"]

        if not all([user_id, room_id, message]):
            return

        save_message(room_id, user_id, message)

        payload = {
            "sender_id": user_id,
            "sender_name": f"{first_name} {last_name}".strip(),
            "message": message,
        }

        emit("receive_message", payload, room=str(room_id), skip_sid=request.sid)
