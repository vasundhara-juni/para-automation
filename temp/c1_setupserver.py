import subprocess
import time

VM_NAME = "c1"
VM_IP = "10.219.94.145"  # Replace with c1's IP
SCRIPT_LOCAL_PATH = "./c1_setup.py"
SCRIPT_REMOTE_PATH = "/root/c1_inside_setup.py"

def is_vm_running(vm_name):
    result = subprocess.run(["virsh", "domstate", vm_name], capture_output=True, text=True)
    return "running" in result.stdout.strip()

def start_vm(vm_name):
    print(f"▶️ Starting {vm_name}...")
    subprocess.run(["virsh", "start", vm_name], check=True)
    time.sleep(10)  # Optional: wait for boot

def copy_script_to_vm(ip, script_local_path, script_remote_path):
    print(f"📤 Copying setup script to {ip}...")
    subprocess.run(["scp", script_local_path, f"root@{ip}:{script_remote_path}"], check=True)

def run_script_in_vm(ip, script_path):
    print(f"💻 Running setup script on {ip}...")
    subprocess.run(["ssh", f"root@{ip}", f"python3 {script_path}"], check=True)

def main():
    if not is_vm_running(VM_NAME):
        start_vm(VM_NAME)
    else:
        print(f"ℹ️ {VM_NAME} is already running.")

    print("⏳ Waiting for VM to be ready for SSH...")
    time.sleep(3)  # Increase if boot time is slow

    copy_script_to_vm(VM_IP, SCRIPT_LOCAL_PATH, SCRIPT_REMOTE_PATH)
    run_script_in_vm(VM_IP, SCRIPT_REMOTE_PATH)
    print("✅ Setup completed on VM.")

if __name__ == "__main__":
    main()