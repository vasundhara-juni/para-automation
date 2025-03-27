import subprocess


# IPs of the other nodes (excluding c1 itself)
VM_IPS = [
    "10.219.90.102",  # p1
    "10.219.90.103",  # p2w1
    "10.219.90.104",  # p3w2
    "10.219.90.105",  # w3
]

# WGET_URL = "https://cdn.juniper.net/software/pa/24.1.0/Paragon_24.1.tar.gz?SM_USER=pvasundhara&__gda__=1741323017_842da3934288d090489b67c079ac0b5d"
WGET_URL="http://10.219.82.112/Paragon_24.1.tar.gz"
PASSWORD = "juniper123"
TAR_NAME = "Paragon_24.1.tar.gz"


def run_command(cmd):
    print(f"➡️ Running: {cmd}")
    subprocess.run(cmd, check=True, shell=True)


def copy_ssh_keys():
    print("\n🔑 Copying SSH key to all other VMs...")
    for ip in VM_IPS:
        subprocess.run(f"ssh-keygen -R {ip}", shell=True)
        subprocess.run(f"ssh-keyscan -H {ip} >> ~/.ssh/known_hosts", shell=True)
        run_command(f"sshpass -p '{PASSWORD}' ssh-copy-id -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa.pub root@{ip}")
    print("✅ SSH key copied to all other VMs.")


def setup_para():
    print("\n📦 Setting up 'para' directory and running initialization...")

    run_command("mkdir -p para")
    run_command(f"cd para && wget -O {TAR_NAME} '{WGET_URL}'")

    print(f"📦 Using tarball: {TAR_NAME}")

    run_command(f"cd para && tar -xzf {TAR_NAME}")

    extracted_dir = subprocess.check_output(
        f"cd para && tar -tf {TAR_NAME} | head -1 | cut -f1 -d'/'",
        shell=True,
        universal_newlines=True
    ).strip()
    print(f"📂 Detected extracted directory: {extracted_dir}")

    run_command(f"cd para/{extracted_dir} && chmod +x run")
    run_command(f"cd para/{extracted_dir} && ./run -c config-dir init")
    run_command(f"cp ~/.ssh/id_rsa para/{extracted_dir}/config-dir/")
    # run_command(f"cd para/{extracted_dir} && ./run -c config-dir inv")

    print("✅ 'para' setup complete.")


def main():
    copy_ssh_keys()
    setup_para()


if __name__ == "__main__":
    main()

