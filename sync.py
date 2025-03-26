# import subprocess

# def run_remote_script(server_ip, username, password, script_path):
#     print(f"Running {script_path} on {server_ip}")
#     try:
#         command = (
#             f"sshpass -p '{password}' ssh {username}@{server_ip} 'python3 {script_path}'"
#         )
#         result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         print(result.stdout.decode())
#         print(f"{script_path} completed successfully on {server_ip}.")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"Error in {script_path} on {server_ip}: {e.stderr.decode()}")
#         return False

# def main():
#     server_ip = input("Enter the server IP address: ")
#     username = input("Enter the username: ")
#     password = input("Enter the password: ")

#     script_order = [
#         './setup.py',
#         './resize_add_disk.py',
#     ]

#     print("Starting remote script execution...")

#     for script_path in script_order:
#         if not run_remote_script(server_ip, username, password, script_path):
#             print("Terminating. Fix the issue before rerunning.")
#             return

#     print("All scripts executed successfully on the remote server!")

# if __name__ == "__main__":
#     main()
# import subprocess
# import json
# from flask import Flask, request, render_template_string

# app = Flask(__name__)

# HTML_FORM = '''
# <!doctype html>
# <html>
#   <body>
#     <h2>Enter Server Details</h2>
#     <form method="post">
#       Server IP: <input type="text" name="server_ip" required><br>
#       Username: <input type="text" name="username" required><br>
#       Password: <input type="password" name="password" required><br>
#       <input type="submit" value="Submit">
#     </form>
#   </body>
# </html>
# '''

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         server_data = {
#             "server_ip": request.form['server_ip'],
#             "username": request.form['username'],
#             "password": request.form['password']
#         }
#         with open('server_data.json', 'w') as f:
#             json.dump(server_data, f)
#         print("Server details saved to server_data.json")
#         run_scripts_from_file()
#         return "Scripts execution started! Check the console for updates."
#     return render_template_string(HTML_FORM)

# def run_remote_script(server_ip, username, password, script_path):
#     print(f"Uploading {script_path} to {server_ip}")
#     try:
#         upload_command = f"sshpass -p '{password}' scp {script_path} {username}@{server_ip}:~/{script_path}"
#         subprocess.run(upload_command, shell=True, check=True)

#         print(f"Running {script_path} on {server_ip}")
#         command = f"sshpass -p '{password}' ssh {username}@{server_ip} 'python3 ~/{script_path}'"
#         result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         print(result.stdout.decode())
#         print(f"{script_path} completed successfully on {server_ip}.")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"Error in {script_path} on {server_ip}: {e.stderr.decode()}")
#         return False


# def run_scripts_from_file():
#     with open('server_data.json', 'r') as f:
#         server_data = json.load(f)

#     server_ip = server_data['server_ip']
#     username = server_data['username']
#     password = server_data['password']

#     script_order = [
#         './prereq.py',
#         './setup.py',
        
#     ]

#     print("Starting remote script execution...")

#     for script_path in script_order:
#         if not run_remote_script(server_ip, username, password, script_path):
#             print("Terminating. Fix the issue before rerunning.")
#             return

#     print("All scripts executed successfully on the remote server!")

# if __name__ == "__main__":
#     print("Starting web UI at http://127.0.0.1:5009")
#     app.run(debug=True, port=5009)

import subprocess
import json
from flask import Flask, request, render_template_string
from json_utils import load_json_file, get_value_from_json
app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<html>
  <body>
    <h2>Enter Server Details</h2>
    <form method="post">
      Server IP: <input type="text" name="server_ip" required><br>
      Username: <input type="text" name="username" required><br>
      Password: <input type="password" name="password" required><br>
      <input type="submit" value="Submit">
    </form>
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        server_data = {
            "server_ip": request.form['server_ip'],
            "username": request.form['username'],
            "password": request.form['password']
        }
        with open('server_data.json', 'w') as f:
            json.dump(server_data, f)
        print("Server details saved to server_data.json")
        run_scripts_from_file()
        return "Scripts execution started! Check the console for updates."
    return render_template_string(HTML_FORM)


def copy_files_to_server(server_ip, username, password, files, remote_path):
    """
    Copies a list of files to the remote server using scp.
    """
    for file in files:
        print(f"📤 Copying {file} to {server_ip}:{remote_path}...")
        try:
            # Using 'file' instead of 'script_path' to reference the actual file being copied
            upload_command = f"sshpass -p '{password}' scp {file} {username}@{server_ip}:{remote_path}/{file}"
            subprocess.run(upload_command, shell=True, check=True)

            print(f"✅ {file} copied successfully to {server_ip}:{remote_path}.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to copy {file} to {server_ip}:{remote_path}: {e}")
            return False
    return True

def run_remote_script(server_ip, username, password, script_path):
    print(f"Uploading {script_path} to {server_ip}")
    try:
        # Upload script to the remote server
        upload_command = f"sshpass -p '{password}' scp {script_path} {username}@{server_ip}:~/{script_path}"
        subprocess.run(upload_command, shell=True, check=True)

        # Detect and run based on file extension
        if script_path.endswith('.py'):
            print(f"Running Python script {script_path} on {server_ip}")
            command = f"sshpass -p '{password}' ssh {username}@{server_ip} 'python3 ~/{script_path}'"
        elif script_path.endswith('.sh'):
            print(f"Running Bash script {script_path} on {server_ip}")
            command = f"sshpass -p '{password}' ssh {username}@{server_ip} 'bash ~/{script_path}'"
        else:
            print(f"Unsupported script format: {script_path}")
            return False

        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        print(f"{script_path} completed successfully on {server_ip}.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error in {script_path} on {server_ip}: {e.stderr.decode()}")
        return False

def run_scripts_from_file():
    with open('server_data.json', 'r') as f:
        server_data = json.load(f)

    server_ip = server_data['server_ip']
    username = server_data['username']
    password = server_data['password']
    files_to_copy = [
        './c1_setup.py',
        './c1_control.py',
        './updateconfig.py',
        './updateinventory.py',
        './inventory',
        './config.yml'

    ]
    remote_path = "/root/"  # Destination directory on the server

    # Copy files to the server
    if not copy_files_to_server(server_ip, username, password, files_to_copy, remote_path):
        print("❌ File copying failed. Terminating.")
        return

    print("✅ All files copied successfully to the remote server.")

    script_order = [
        './prereq.py',
         './setup.py',
        './resize.py',  # Add your Bash script here
        # './c1_setupserver.py',
        # './c1_controlserver.py',
        'c1_preparation.py',
        './paragoninventory_config.py',
        './deploy.py'
    ]

    print("Starting remote script execution...")

    for script_path in script_order:
        if not run_remote_script(server_ip, username, password, script_path):
            print("Terminating. Fix the issue before rerunning.")
            return

    print("All scripts executed successfully on the remote server!")

if __name__ == "__main__":
    print("Starting web UI at http://127.0.0.1:5009")
    app.run(debug=True, port=5009)
