from flask import Flask, render_template, request, jsonify
import subprocess
import platform

app = Flask(__name__)

# Determine OS (for appropriate ping command)
is_windows = platform.system().lower() == "windows"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ping", methods=["POST"])
def ping():
    target = request.form.get("target")
    if not target:
        return jsonify({"error": "Please enter an IP address or hostname"}), 400

    try:
        # Define the ping command based on OS
        command = ["ping", "-n", "4", target] if is_windows else ["ping", "-c", "4", target]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            return jsonify({"success": True, "output": result.stdout})
        else:
            return jsonify({"success": False, "output": result.stderr})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
