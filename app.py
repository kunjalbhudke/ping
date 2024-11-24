from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['POST'])
def ping():
    target = request.form.get('target')  # Get the target (IP/Hostname) from the form

    if not target:
        return "Error: Please provide a valid IP address or hostname.", 400

    try:
        # Run the ping command (compatible with different platforms)
        command = ["ping", "-c", "4", target] if not is_windows else ["ping", target]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            return f"<pre>Ping Successful:\n{result.stdout}</pre>"
        else:
            return f"<pre>Ping Failed:\n{result.stderr}</pre>"

    except Exception as e:
        return f"Error occurred: {str(e)}", 500

# Check the operating system
import platform
is_windows = platform.system().lower() == "windows"

if __name__ == "__main__":
    app.run(debug=True)
