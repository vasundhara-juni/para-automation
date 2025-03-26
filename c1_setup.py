import subprocess
import os

def run_command(command, check=True):
    """Run a shell command and handle errors."""
    subprocess.run(command, shell=True, check=check)

def main():
    try:
        print("🔄 Updating packages...")
        run_command("apt-get update")

        print("🔄 Installing required packages...")
        run_command("apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common wget openssh-server")

        print("🔄 Installing sshpass...")
        run_command("apt-get install -y sshpass")

        print("🔄 Adding Docker GPG key...")
        run_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -")

        print("🔄 Adding Docker repository...")
        run_command('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')

        print("🔄 Updating packages...")
        run_command("apt-get update")

        print("🔄 Installing Docker...")
        run_command("apt-get install -y docker-ce docker-ce-cli containerd.io")

        print("🔄 Generating SSH key...")
        ssh_dir = os.path.expanduser("~/.ssh")
        ssh_key_path = os.path.join(ssh_dir, "id_rsa")
        if not os.path.exists(ssh_key_path):
            os.makedirs(ssh_dir, exist_ok=True)
            run_command(f"ssh-keygen -t rsa -N '' -f {ssh_key_path}")
            print("✅ SSH key generated successfully!")
        else:
            print("ℹ️ SSH key already exists. Skipping key generation.")

        print("✅ Setup completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()