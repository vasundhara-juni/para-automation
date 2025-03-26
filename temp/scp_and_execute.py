import subprocess
import logging
import sys

def run_cmd(cmd):
    try:
        logging.info(f"Running command: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e}")
        sys.exit(1)

def copy_and_execute_script(vm_ip, username="root", script_path="postconfig22.py", remote_path="/root/ssh_config_setup.py"):
    try:
        logging.info(f"Copying {script_path} to {username}@{vm_ip}:{remote_path}")
        run_cmd(f"scp {script_path} {username}@{vm_ip}:{remote_path}")

        logging.info(f"Executing the script on {username}@{vm_ip}")
        run_cmd(f"ssh {username}@{vm_ip} 'python3 {remote_path}'")

        logging.info("Script executed successfully.")
    except Exception as e:
        logging.error(f"Failed to copy or execute script: {e}")
        sys.exit(1)

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

    if len(sys.argv) != 2:
        logging.error("Usage: python3 scp_and_execute.py <vm_ip>")
        sys.exit(1)

    vm_ip = sys.argv[1]
    copy_and_execute_script(vm_ip)

if __name__ == "__main__":
    main()
