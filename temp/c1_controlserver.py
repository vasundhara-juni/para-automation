import subprocess

# IP of c1 node
C1_IP = "10.219.94.145"

# Path to your local cluster_setup.py script
LOCAL_SCRIPT_PATH = "./c1_control.py"

# Remote path on c1
REMOTE_SCRIPT_PATH = "/root/cluster_setup.py"

def copy_script_to_c1(local_path, remote_ip, remote_path):
    print(f"📤 Copying {local_path} to c1 ({remote_ip})...")
    subprocess.run(["scp", local_path, f"root@{remote_ip}:{remote_path}"], check=True)
    print("✅ Script copied to c1.")

def run_script_on_c1(remote_ip, remote_path):
    print(f"🚀 Running the script on c1 ({remote_ip})...")
    subprocess.run(["ssh", f"root@{remote_ip}", f"python3 {remote_path}"], check=True)
    print("🏁 Script executed successfully on c1.")

def main():
    try:
        copy_script_to_c1(LOCAL_SCRIPT_PATH, C1_IP, REMOTE_SCRIPT_PATH)
        run_script_on_c1(C1_IP, REMOTE_SCRIPT_PATH)
        print("🏁 All done!")
    except subprocess.CalledProcessError as e:
        print(f"❌ An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()