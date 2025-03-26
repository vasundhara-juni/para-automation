import subprocess
import time

C1_IP = "10.219.94.145"
VM_NAME = "c1"
SCRIPTS = [
    ("./c1_setup.py", "/root/c1_inside_setup.py")
    ("./c1_control.py", "/root/cluster_setup.py"),
    
]

def run_command(command):
    subprocess.run(command, check=True)

def is_vm_running(vm_name):
    result = subprocess.run(["virsh", "domstate", vm_name], capture_output=True, text=True)
    return "running" in result.stdout.strip()

def start_vm(vm_name):
    print(f"▶️ Starting {vm_name}...")
    run_command(["virsh", "start", vm_name])
    time.sleep(10)

def copy_script_to_vm(local_path, ip, remote_path):
    print(f"📤 Copying {local_path} to {ip}...")
    run_command(["scp", local_path, f"root@{ip}:{remote_path}"])

def run_script_in_vm(ip, script_path):
    print(f"💻 Running script on {ip}...")
    run_command(["ssh", f"root@{ip}", f"python3 {script_path}"])

def ensure_vm_running(vm_name, ip):
    if not is_vm_running(vm_name):
        start_vm(vm_name)
    else:
        print(f"ℹ️ {vm_name} is already running.")
    
    print("⏳ Waiting for VM to be ready for SSH...")
    time.sleep(3)

def main():
    try:
        ensure_vm_running(VM_NAME, C1_IP)
        for local_path, remote_path in SCRIPTS:
            copy_script_to_vm(local_path, C1_IP, remote_path)
            run_script_in_vm(C1_IP, remote_path)
        print("✅ All scripts executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
