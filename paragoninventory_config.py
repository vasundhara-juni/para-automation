# import subprocess
# import time

# # File paths and IP addresses
# SCRIPT_1_PATH = "./updateconfig.py"
# SCRIPT_2_PATH = "./updatedinventory.py"
# FILE_1_PATH = "./pathfinder_config_updated.yaml"  # Path of the first generated file
# FILE_2_PATH = "./inventory_updated"  # Path of the second generated file
# REMOTE_IP = "10.219.94.145"  # Replace with the IP to copy the files to
# REMOTE_PATH = "/root/para/Paragon_24.1/config-dir"  # Replace with the desired destination path on the remote system

# def run_script(script_path):
#     """ Run the given script to generate files. """
#     print(f"💻 Running script: {script_path}...")
#     subprocess.run(["python3", script_path], check=True)

# def scp_files_to_remote(file_paths, remote_ip, remote_path):
#     """ SCP the generated files to the remote IP and path. """
#     for file_path in file_paths:
#         print(f"📤 Copying {file_path} to {remote_ip}:{remote_path}...")
#         subprocess.run(["scp", file_path, f"root@{remote_ip}:{remote_path}"], check=True)

# def main():
#     # Run the two scripts to generate the files
#     try:
#         print("⏳ Running the first script to generate file 1...")
#         run_script(SCRIPT_1_PATH)

#         print("⏳ Running the second script to generate file 2...")
#         run_script(SCRIPT_2_PATH)

#         # After both scripts finish, SCP the generated files
#         print("⏳ SCPing the generated files to remote location...")
#         scp_files_to_remote([FILE_1_PATH, FILE_2_PATH], REMOTE_IP, REMOTE_PATH)

#         print("✅ All operations completed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"❌ An error occurred: {e}")

# if __name__ == "__main__":
#     main()
import subprocess
import time

SCRIPT_1_PATH = "./updateconfig.py"
SCRIPT_2_PATH = "./updateinventory.py"
FILE_1_PATH = "./pathfinder_config_updated.yml"  # Path of the first generated file
FILE_2_PATH = "./inventory_updated"  # Path of the second generated file
REMOTE_IP = "10.219.90.101"  # Replace with the IP to copy the files to
REMOTE_PATH = "/root/para/Paragon_24.1/config-dir"  # Replace with the desired destination path on the remote system
 # Replace with the desired destination path on the remote system
REMOTE_FILE_1_NAME = "config.yml"  # The name to give the first file on the remote machine
REMOTE_FILE_2_NAME = "inventory"  # The name to give the second file on the remote machine

def run_script(script_path):
    """ Run the given script to generate files. """
    print(f"💻 Running script: {script_path}...")
    subprocess.run(["python3", script_path], check=True)

def file_exists_on_remote(remote_ip, remote_file_path):
    """ Check if a file exists on the remote machine. """
    check_command = f"ssh root@{remote_ip} '[ -f {remote_file_path} ] && echo exists || echo not_exists'"
    result = subprocess.run(check_command, shell=True, capture_output=True, text=True)
    return 'exists' in result.stdout.strip()

def scp_files_to_remote(file_paths, remote_ip, remote_path, remote_file_names):
    """ SCP the generated files to the remote IP and path. Replace files if they exist. """
    for file_path, remote_file_name in zip(file_paths, remote_file_names):
        remote_file_path = f"{remote_path}/{remote_file_name}"

        # Check if the file already exists on the remote
        if file_exists_on_remote(remote_ip, remote_file_path):
            print(f"⚠️ File {remote_file_name} exists on the remote machine. It will be replaced.")
        
        print(f"📤 Copying {file_path} to {remote_ip}:{remote_file_path}...")
        subprocess.run(["scp", file_path, f"root@{remote_ip}:{remote_file_path}"], check=True)

def main():
    try:
        # Run the two scripts to generate the files
        print("⏳ Running the first script to generate file 1...")
        run_script(SCRIPT_1_PATH)

        print("⏳ Running the second script to generate file 2...")
        run_script(SCRIPT_2_PATH)

        # After both scripts finish, SCP the generated files
        print("⏳ SCPing the generated files to remote location...")
        scp_files_to_remote(
            [FILE_1_PATH, FILE_2_PATH],  # Local files
            REMOTE_IP,  # Remote IP
            REMOTE_PATH,  # Remote destination folder
            [REMOTE_FILE_1_NAME, REMOTE_FILE_2_NAME]  # Remote file names
        )

        print("✅ All operations completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
