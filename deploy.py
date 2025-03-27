import subprocess

# VM details
VM_IP = "10.219.90.101"  # Replace with the IP of your VM
USER = "root"  # Replace with the correct username for the VM
PASSWORD = "juniper123"  # Replace with the actual password for the VM

def run_command_on_vm(vm_ip, user, password, command):
    """ Run a command on the VM using sshpass, change directory, and deploy. """
    # This command changes the directory and then runs the deploy command
    ssh_command = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{vm_ip} 'cd /root/para/Paragon_24.1/ && {{deploy_command}}'".format(deploy_command=command)
    print(f"💻 Running command: {ssh_command}")

    # Use subprocess to run the command and fetch live logs
    with subprocess.Popen(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        for line in process.stdout:
            print(line, end='')  # Print stdout
        for line in process.stderr:
            print(line, end='', flush=True)  # Print stderr

    # Wait for the process to complete and get the exit code
    process.wait()
    return process.returncode

def main():
    # Replace this with your actual deploy command
    deploy_command = "./run -c config-dir deploy"  # Example: "deploy.sh" or a specific deploy script/command

    # Run the deploy command on the VM
    return_code = run_command_on_vm(VM_IP, USER, PASSWORD, deploy_command)

    if return_code == 0:
        print("✅ Deploy command executed successfully.")
    else:
        print(f"❌ Deploy command failed with exit code {return_code}.")

if __name__ == "__main__":
    main()
