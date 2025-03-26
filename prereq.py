import subprocess
import sys
import shutil
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to terminal
        logging.FileHandler("prereq.log")  # Log to a file
    ]
)

def run_cmd(cmd, check=True):
    """Run a shell command and return the result."""
    try:
        logging.info(f"Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e}")
        sys.exit(1)

def check_python():
    """Ensure Python 3 is installed."""
    logging.info("🔍 Checking for Python 3...")
    if shutil.which("python3") is None:
        logging.error("❌ Python 3 is not installed. Please install it and try again.")
        sys.exit(1)
    logging.info("✅ Python 3 is installed.")

def check_pip():
    """Ensure pip3 is installed."""
    logging.info("🔍 Checking for pip3...")
    if shutil.which("pip3") is None:
        logging.warning("❌ pip3 is not installed. Installing pip3...")
        run_cmd("apt update && apt install -y python3-pip")
    logging.info("✅ pip3 is installed.")

def check_sshpass():
    """Ensure sshpass is installed."""
    logging.info("🔍 Checking for sshpass...")
    if shutil.which("sshpass") is None:
        logging.warning("❌ sshpass is not installed. Installing sshpass...")
        run_cmd("apt update && apt install -y sshpass")
    logging.info("✅ sshpass is installed.")

def main():
    check_python()
    check_pip()
    check_sshpass()
    logging.info("🏁 All prerequisites are satisfied.")

if __name__ == "__main__":
    main()