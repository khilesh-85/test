from flask import Flask, render_template, request
import subprocess
import threading
import time
from datetime import datetime

app = Flask(__name__)

# 🔥 CHANGE THIS PATH (IMPORTANT)
REPO_PATH = "/Users/khushaggarwal/Documents/test"

# ------------------ RUN GIT COMMAND ------------------
def run_git(cmd):
    return subprocess.getoutput(f"cd {REPO_PATH} && {cmd}")


# ------------------ AUTO BACKUP ------------------
def auto_backup():
    while True:
        output = run_git("git status --porcelain")

        if output.strip() != "":
            print("Auto backup running...")

            run_git("git add .")

            msg = f"Auto backup: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            run_git(f'git commit -m "{msg}"')

            run_git("git push origin main")

        time.sleep(60)  # every 1 minute


# ------------------ HOME PAGE ------------------
@app.route("/")
def home():
    return render_template("index.html")


# ------------------ MANUAL BACKUP ------------------
@app.route("/backup")
def backup():
    run_git("git add .")
    run_git('git commit -m "Manual backup from web"')
    run_git("git push origin main")
    return "✅ Backup Done <br><a href='/'>⬅ Back</a>"


# ------------------ HISTORY DASHBOARD ------------------
@app.route("/history")
def history():
    log = run_git("git log --oneline")

    return f"""
    <html>
    <head>
        <title>Backup History</title>
        <style>
            body {{
                font-family: Arial;
                background: #f4f6f8;
                text-align: center;
            }}
            .box {{
                background: white;
                padding: 20px;
                margin: 50px auto;
                width: 60%;
                border-radius: 10px;
                box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
            }}
            pre {{
                text-align: left;
                background: #eee;
                padding: 10px;
                border-radius: 5px;
            }}
            a {{
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: white;
                background: #667eea;
                padding: 10px 15px;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>

        <div class="box">
            <h2>📊 Backup History</h2>
            <pre>{log}</pre>
            <a href="/">⬅ Back to Dashboard</a>
        </div>

    </body>
    </html>
    """


# ------------------ RESTORE ------------------
@app.route("/restore", methods=["POST"])
def restore():
    commit = request.form.get("commit")

    run_git(f"git checkout {commit}")

    return f"""
    <h3>✅ Restored to {commit}</h3>
    <a href="/">⬅ Back</a>
    """


# ------------------ START AUTO BACKUP THREAD ------------------
threading.Thread(target=auto_backup, daemon=True).start()


# ------------------ RUN APP ------------------
if __name__ == "__main__":
    app.run(debug=True)
