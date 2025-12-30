from flask import Flask, request, jsonify, render_template
import asyncio
import threading
import os
from core.client.manager import start_userbot

app = Flask(__name__)
PORT = int(os.getenv("PORT", 10000))

# ---------- Async loop ----------
loop = asyncio.new_event_loop()

def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/connect", methods=["POST"])
def connect():
    data = request.get_json(silent=True) or {}
    session = data.get("session", "").strip()

    if not session:
        return jsonify({
            "status": "failed",
            "text": "Session string is empty"
        }), 400

    try:
        future = asyncio.run_coroutine_threadsafe(
            start_userbot(session),
            loop
        )

        info = future.result(timeout=20)

        # ✅ Already running
        if info.get("already"):
            return jsonify({
                "status": "success",
                "text": "Userbot already connected and running",
                "details": {
                    "userId": info["user_id"],
                    "phoneNumber": info["phone"],
                    "dcId": info["dc_id"]
                }
            })

        # ✅ Newly connected
        return jsonify({
            "status": "success",
            "text": "Userbot connected successfully",
            "details": {
                "userId": info["user_id"],
                "phoneNumber": info["phone"],
                "dcId": info["dc_id"]
            }
        })

    except asyncio.TimeoutError:
        return jsonify({
            "status": "failed",
            "text": "Connection timeout, please try again"
        }), 504

    except Exception as e:
        return jsonify({
            "status": "failed",
            "text": str(e)
        }), 500


if __name__ == "__main__":
    t = threading.Thread(target=start_loop, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=PORT)
