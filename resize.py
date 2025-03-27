import subprocess

VMS = ["10.219.90.101", "10.219.90.102", "10.219.90.103", "10.219.90.104", "10.219.90.105"]
USER = "root"
PASSWORD = "juniper123"

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def execute_ssh_command(vm, command):
    ssh_command = f"sshpass -p {PASSWORD} ssh -o StrictHostKeyChecking=no {USER}@{vm} '{command}'"
    run_command(ssh_command)

def check_partition(vm, partition):
    # Check if the partition exists and is 100% full
    check_command = f"sshpass -p {PASSWORD} ssh -o StrictHostKeyChecking=no {USER}@{vm} 'df -h /dev/{partition} | grep -v Filesystem | awk \'{{print $5}}\''"
    result = subprocess.run(check_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        usage = result.stdout.decode('utf-8').strip()  # Get the usage percentage
        if usage == "100%":
            return True  # Partition is 100% full
        else:
            return False  # Partition is not 100% full
    else:
        print(f"Error checking partition {partition} on {vm}")
        return False

def process_vm(vm, is_first_vm):
    print(f"Processing VM: {vm}")

    # Perform /dev/vda operations if not already done and if /dev/vda1 is not 100% full
    if not check_partition(vm, 'vda1'):
        print(f"Growing partition on {vm}...")
        execute_ssh_command(vm, "sudo growpart /dev/vda 1 || echo 'growpart failed'")
        execute_ssh_command(vm, "sudo resize2fs /dev/vda1 || echo 'resize2fs failed'")
    else:
        print(f"/dev/vda1 is 100% full or already exists on {vm}. Skipping growpart and resize2fs.")

    # Perform /dev/vdb operations for all VMs except the first one
    if not is_first_vm:
        print(f"Configuring /dev/vdb on {vm}...")
        execute_ssh_command(vm, "sudo parted /dev/vdb mklabel gpt || echo 'Failed to create GPT partition table'")
        execute_ssh_command(vm, "sudo parted -a optimal /dev/vdb mkpart primary ext4 0% 100% || echo 'Partition creation failed'")
    else:
        print(f"Skipping /dev/vdb steps for {vm}")

    print("Verifying partitions...")
    execute_ssh_command(vm, "lsblk")

# Process all VMs
for i, vm in enumerate(VMS):
    process_vm(vm, i == 0)

print("✅ All operations completed.")