import logging
import subprocess
import sys
import os

def create_ssh_config():
    logging.info("Creating high-priority SSH configuration file.")
    config_path = "/etc/ssh/sshd_config.d/99-custom.conf"
    config_content = """PasswordAuthentication yes
PermitRootLogin yes
PubkeyAuthentication yes
AllowTcpForwarding yes
"""
    try:
        # Ensure the directory exists
        config_dir = os.path.dirname(config_path)
        if not os.path.exists(config_dir):
            logging.info("Creating directory: %s", config_dir)
            os.makedirs(config_dir, exist_ok=True)

        # Write the SSH configuration file
        with open(config_path, "w") as config_file:
            config_file.write(config_content)
        logging.info("SSH configuration created at %s", config_path)

        # Restart the SSH service
        logging.info("Restarting SSH service...")
        subprocess.run("sudo systemctl restart sshd", shell=True, check=True)
        logging.info("SSH service restarted successfully.")
    except Exception as e:
        logging.error(f"Failed to create or restart SSH configuration: {e}")
        sys.exit(1)

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to terminal
        ]
    )

    logging.info("Starting SSH configuration setup...")
    create_ssh_config()
    logging.info("SSH configuration setup completed successfully.")

if __name__ == "__main__":
    main()