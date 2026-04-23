from flask import Flask, render_template, request
import subprocess
import threading
import time
from datetime import datetime
import os

app = Flask(__name__)

# Automatically use the folder where app.py exists
REPO_PATH = os.path.dirname(os.path.abspath(__file__))

# ------------------ RUN GIT COMMAND ------------------
def run_git(cmd):
    return subprocess.getoutput(f'git -C "{REPO_PATH}" {cmd}')


# ------------------ AUTO BACKUP ------------------
def auto_backup():
    while True:
        output = run_git("status --porcelain")

        if output.strip() != "":
            print("Auto backup running...")

            run_git("add .")

            msg = f'Auto backup: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            commit_output = run_git(f'commit -m "{msg}"')
            print(commit_output)

<<<<<<< HEAD
            # Optional: push to GitHub too
            push_output = run_git("push origin main")
            print(push_output)

        time.sleep(10)   # check every 10 seconds
=======
            # push only if you want GitHub update too
            push_output = run_git("push origin main")
            print(push_output)

        time.sleep(60)
>>>>>>> 0b9e6b72b55024de1a56761bb7e6d44d1ae1e719


# ------------------ HOME PAGE ------------------
@app.route("/")
def home():
    return render_template("index.html")


# ------------------ MANUAL BACKUP ------------------
@app.route("/backup")
def backup():
    run_git("add .")
    commit_output = run_git('commit -m "Manual backup from web"')
    push_output = run_git("push origin main")

    return f"""
    <h3>✅ Backup Done</h3>
    <pre>{commit_output}
{push_output}</pre>
    <a href="/">⬅ Back</a>
    """


# ------------------ HISTORY DASHBOARD ------------------
@app.route("/history")
def history():
    log = run_git("log --oneline")

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
                white-space: pre-wrap;
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
    commit = request.form.get("commit", "").strip()

    if not commit:
        return "<h3>❌ Please enter a commit ID</h3><a href='/'>⬅ Back</a>"

    output = run_git(f"reset --hard {commit}")

    return f"""
    <h3>✅ Restored to {commit}</h3>
    <pre>{output}</pre>
    <a href="/">⬅ Back</a>
    """


<<<<<<< HEAD
# ------------------ RUN APP ------------------
=======
# ------------------ START AUTO BACKUP THREAD ------------------
>>>>>>> 0b9e6b72b55024de1a56761bb7e6d44d1ae1e719
if __name__ == "__main__":
    threading.Thread(target=auto_backup, daemon=True).start()
    app.run(debug=True, use_reloader=False)