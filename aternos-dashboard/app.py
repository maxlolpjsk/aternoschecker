from flask import Flask, jsonify, render_template
from python_aternos import Client
import os

app = Flask(__name__)

# Configured with your guest account details
ATERNOS_USER = os.getenv("ATERNOS_USER", "ourgroupmc")
ATERNOS_PASS = os.getenv("ATERNOS_PASS", "88888888")

def get_aternos_server():
    # Login and fetch the first server in your account
    aternos = Client.from_credentials(ATERNOS_USER, ATERNOS_PASS)
    servers = aternos.list_servers()
    return servers[0]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def check_status():
    try:
        srv = get_aternos_server()
        return jsonify({
            "success": True,
            "status": srv.status,      # "online", "offline", "starting", etc.
            "players": srv.players_count,
            "max_players": srv.max_players,
            "port": srv.port
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/start", methods=["POST"])
def start_server():
    try:
        srv = get_aternos_server()
        if srv.status == "offline":
            srv.start()
            return jsonify({"success": True, "message": "Server start sequence triggered!"})
        else:
            return jsonify({"success": True, "message": f"Server is already {srv.status}."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)