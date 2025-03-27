# import os
# import subprocess
# import libvirt


# vms = {
#     "c1": {"memory": 12288, "vcpu": 2, "network": "mgmt",  "ip": "10.219.94.140"},
#     "p1": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.94.141"},
#     "p2w1": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.94.142"},
#     "p3w2": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.94.143"},
#     "w3": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.94.144"},
# }

# libvirt_pool_dir = "/var/lib/libvirt/images"
# base_image_name = "bionic-server-cloudimg-amd64.img"
# vm_root_pass = "juniper123"
# ssh_key_path = "/root/.ssh/id_rsa.pub"
# gateway = "10.219.94.129"
# dns_server = "66.129.233.81"
# subnet_mask = "/25"
# interface_name = "enp1s0"

# def system_setup():
#     print("Installing required packages and setting up environment...")
#     # Install system-level dependencies
#     run_cmd("apt update && apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager libguestfs-tools ")
#     run_cmd("systemctl enable --now libvirtd")
#     run_cmd("systemctl is-active libvirtd")
#     run_cmd("usermod -aG libvirt $USER")
#     run_cmd("usermod -aG kvm $USER")
    
#     # Install the libvirt Python module
#     print("Installing the libvirt Python module...")
#     run_cmd("pip3 install libvirt-python")
    
#     print("System setup complete. You may need to re-login for group changes to apply.")


# def run_cmd(cmd):
#     subprocess.run(cmd, shell=True, check=True)


# def populate_hosts_file():
#     print("Skipping /etc/hosts population as this needs inventory parsing.")


# def create_network_yaml_files():
#     output_dir = "/root/paragon"
#     os.makedirs(output_dir, exist_ok=True)

#     for vm_name, config in vms.items():
#         yaml_content = f"""network:
#   ethernets:
#     {interface_name}:
#       dhcp4: no
#       dhcp6: no
#       addresses: [{config['ip']}{subnet_mask}]
#       gateway4: {gateway}
#       nameservers:
#         addresses: [{dns_server}]
#   version: 2
# """
#         yaml_path = os.path.join(output_dir, f"{vm_name}.yaml")
#         with open(yaml_path, "w") as yaml_file:
#             yaml_file.write(yaml_content)
#         print(f"Generated network YAML for {vm_name} at {yaml_path}")


# def list_vms():
#     conn = libvirt.open("qemu:///system")
#     if conn is None:
#         raise Exception("Failed to open connection to qemu:///system")
#     vms_list = [vm.name() for vm in conn.listAllDomains()]
#     conn.close()
#     return vms_list

# def copy_image(vm_name):
#     src = f"/root/{base_image_name}"
#     dest = f"{libvirt_pool_dir}/{vm_name}.qcow2"
#     if not os.path.exists(dest):
#         run_cmd(f"cp {src} {dest}")
#         os.chmod(dest, 0o660)
#         return True
#     return False


# def resize_image(vm_name):
#     image_path = f"{libvirt_pool_dir}/{vm_name}.qcow2"
#     run_cmd(f"qemu-img resize {image_path} +200G")


# def configure_image(vm_name):
#     yaml_path = f"/root/paragon/{vm_name}.yaml"
#     image_path = f"{libvirt_pool_dir}/{vm_name}.qcow2"
#     run_cmd(f"""
#         virt-customize -a {image_path} \
#         --root-password password:{vm_root_pass} \
#         --hostname {vm_name} \
#         --upload {yaml_path}:/etc/netplan/00-installer-config.yaml \
#         --mkdir /root/.ssh \
#         --copy-in {ssh_key_path}:/root/.ssh/ \
#         --copy {ssh_key_path}:/root/.ssh/authorized_keys \
#         --run-command 'sed -i "s/.*PubkeyAuthentication yes/PubkeyAuthentication yes/g" /etc/ssh/sshd_config' \
#         --run-command 'sed -i "s/.*PasswordAuthentication no/PasswordAuthentication yes/g" /etc/ssh/sshd_config' \
#          --run-command 'sed -i "s/.*AllowTCPForwarding yes/AllowTCPForwarding yes/g" /etc/ssh/sshd_config' \
#         --run-command 'sed -i "s/.*PermitRootLogin prohibit-password/PermitRootLogin yes/g" /etc/ssh/sshd_config' \
#         --run-command 'sed -i "s/Unattended-Upgrade \\"1\\"/Unattended-Upgrade \\"0\\"/g" /etc/apt/apt.conf.d/20auto-upgrades' \
#         --run-command 'dpkg-reconfigure -pmedium unattended-upgrades' \
#         --run-command 'dpkg-reconfigure openssh-server'
#     """)


# def define_vm(vm_name, config):
#     run_cmd(f"""
#         virt-install --name {vm_name} \
#         --disk {libvirt_pool_dir}/{vm_name}.qcow2 \
#         --vcpus {config['vcpu']} \
#         --cpu host-model \
#         --memory {config['memory']} \
#          --network bridge={config['network']} \
#         --virt-type kvm \
#         --import \
#         --os-variant ubuntu20.04 \
#         --graphics vnc \
#         --serial pty \
#         --noautoconsole \
#         --console pty,target_type=virtio
#     """)


# def start_vm(vm_name):
#     conn = libvirt.open("qemu:///system")
#     if conn is None:
#         raise Exception("Failed to open connection to qemu:///system")
#     vm = conn.lookupByName(vm_name)
#     if vm is not None and not vm.isActive():
#         vm.create()
#     conn.close()


# def main():
#     system_setup()
#     populate_hosts_file()
#     create_network_yaml_files()

#     existing_vms = list_vms()
#     for vm_name, config in vms.items():
#         if vm_name in existing_vms:
#             print(f"{vm_name} already exists. Skipping...")
#             continue

#         copied = copy_image(vm_name)
#         resize_image(vm_name)

#         if copied:
#             configure_image(vm_name)

#         define_vm(vm_name, config)
#         start_vm(vm_name)
#         print(f"{vm_name} deployed and started.")


# if __name__ == "__main__":
#     main()

# import os
# import subprocess
# import libvirt
# import logging
# import sys
# import yaml

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# vms = {
#     "c1": {"memory": 12288, "vcpu": 2, "network": "mgmt",  "ip": "10.219.94.140"},
#     "p1": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.94.141"},
#     "p2w1": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.94.142"},
#     "p3w2": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.94.143"},
#     "w3": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.94.144"},
# }

# libvirt_pool_dir = "/var/lib/libvirt/images"
# base_image_name = "bionic-server-cloudimg-amd64.img"
# base_image_url = f"https://cloud-images.ubuntu.com/bionic/current/{base_image_name}"
# vm_root_pass = "juniper123"
# ssh_key_path = "/root/.ssh/id_rsa.pub"
# gateway = "10.219.94.129"
# dns_server = "66.129.233.81"
# subnet_mask = "/25"
# interface_name = "enp1s0"

# def system_setup():
#     logging.info("Installing required packages and setting up environment...")
#     run_cmd("apt update && apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager libguestfs-tools curl")
#     run_cmd("systemctl enable --now libvirtd")
#     run_cmd("systemctl is-active libvirtd")
#     run_cmd("usermod -aG libvirt $USER")
#     run_cmd("usermod -aG kvm $USER")

#     # logging.info("Installing the libvirt Python module...")
#     # run_cmd("pip3 install libvirt-python")
#     logging.info("System setup complete. You may need to re-login for group changes to apply.")

# def ensure_ssh_key_exists():
#     if not os.path.isfile(ssh_key_path):
#         logging.warning(f"SSH public key not found at {ssh_key_path}. Generating a new SSH key.")
#         try:
#             subprocess.run(f"ssh-keygen -t rsa -b 4096 -f {ssh_key_path[:-4]} -N ''", shell=True, check=True)
#             logging.info("SSH key generated successfully.")
#         except subprocess.CalledProcessError as e:
#             logging.error(f"Failed to generate SSH key: {e}")
#             sys.exit(1)
#     else:
#         logging.info(f"SSH public key found at {ssh_key_path}.")

# def run_cmd(cmd):
#     try:
#         logging.info(f"Running command: {cmd}")
#         subprocess.run(cmd, shell=True, check=True)
#     except subprocess.CalledProcessError as e:
#         logging.error(f"❌ Command failed: {e}")
#         sys.exit(1)

# def check_and_download_base_image():
#     base_image_path = f"/root/{base_image_name}"
#     if not os.path.exists(base_image_path):
#         logging.info(f"Base image not found. Downloading from {base_image_url}")
#         run_cmd(f"curl -o {base_image_path} {base_image_url}")
#     else:
#         logging.info(f"Base image found at {base_image_path}")

# def populate_hosts_file():
#     logging.info("Skipping /etc/hosts population as this needs inventory parsing.")

# def create_network_yaml_files():
#     output_dir = "/root/paragon"
#     os.makedirs(output_dir, exist_ok=True)

#     for vm_name, config in vms.items():
#         yaml_content = f"""network:
#   ethernets:
#     {interface_name}:
#       dhcp4: no
#       dhcp6: no
#       addresses: [{config['ip']}{subnet_mask}]
#       gateway4: {gateway}
#       nameservers:
#         addresses: [{dns_server}]
#   version: 2
# """
#         yaml_path = os.path.join(output_dir, f"{vm_name}.yaml")
#         with open(yaml_path, "w") as yaml_file:
#             yaml_file.write(yaml_content)
#         logging.info(f"Generated network YAML for {vm_name} at {yaml_path}")

# def list_vms():
#     logging.info("Listing existing VMs...")
#     conn = libvirt.open("qemu:///system")
#     if conn is None:
#         logging.error("Failed to open connection to qemu:///system")
#         raise Exception("Failed to open connection to qemu:///system")
#     vms_list = [vm.name() for vm in conn.listAllDomains()]
#     conn.close()
#     logging.info(f"Existing VMs: {vms_list}")
#     return vms_list

# def copy_image(vm_name):
#     check_and_download_base_image()
#     src = f"/root/{base_image_name}"
#     dest = f"{libvirt_pool_dir}/{vm_name}.qcow2"
#     if not os.path.exists(dest):
#         logging.info(f"Copying base image for {vm_name}")
#         run_cmd(f"cp {src} {dest}")
#         os.chmod(dest, 0o660)
#         return True
#     logging.info(f"Image for {vm_name} already exists. Skipping copy.")
#     return False

# def resize_image(vm_name):
#     image_path = f"{libvirt_pool_dir}/{vm_name}.qcow2"
#     logging.info(f"Resizing image for {vm_name}")
#     run_cmd(f"qemu-img resize {image_path} +200G")


# def configure_image(vm_name):
#     yaml_path = f"/root/paragon/{vm_name}.yaml"
#     image_path = f"{libvirt_pool_dir}/{vm_name}.qcow2"
#     run_cmd(f"""
#         virt-customize -a {image_path} \
#         --root-password password:{vm_root_pass} \
#         --hostname {vm_name} \
#         --upload {yaml_path}:/etc/netplan/00-installer-config.yaml \
#         --mkdir /root/.ssh \
#         --copy-in {ssh_key_path}:/root/.ssh/ \
#         --copy {ssh_key_path}:/root/.ssh/authorized_keys \
#         --run-command 'sed -i "s/.*PubkeyAuthentication yes/PubkeyAuthentication yes/g" /etc/ssh/sshd_config' \
#         --run-command 'sed -i "s/.*PasswordAuthentication no/PasswordAuthentication yes/g" /etc/ssh/sshd_config' \
#          --run-command 'sed -i "s/.*AllowTCPForwarding yes/AllowTCPForwarding yes/g" /etc/ssh/sshd_config' \
#         --run-command 'sed -i "s/.*PermitRootLogin prohibit-password/PermitRootLogin yes/g" /etc/ssh/sshd_config' \
#         --run-command 'sed -i "s/Unattended-Upgrade \\"1\\"/Unattended-Upgrade \\"0\\"/g" /etc/apt/apt.conf.d/20auto-upgrades' \
#         --run-command 'dpkg-reconfigure -pmedium unattended-upgrades' \
#         --run-command 'dpkg-reconfigure openssh-server'
#     """)

# def define_vm(vm_name, config):
#     logging.info(f"Defining VM {vm_name}")
#     run_cmd(f"""
#         virt-install --name {vm_name} \
#         --disk {libvirt_pool_dir}/{vm_name}.qcow2 \
#         --vcpus {config['vcpu']} \
#         --cpu host-model \
#         --memory {config['memory']} \
#         --network bridge={config['network']} \
#         --virt-type kvm \
#         --import \
#         --os-variant ubuntu20.04 \
#         --graphics vnc \
#         --serial pty \
#         --noautoconsole \
#         --console pty,target_type=virtio
#     """)

# def main():
#     system_setup()
#     populate_hosts_file()
#     ensure_ssh_key_exists()
#     check_and_download_base_image()
#     create_network_yaml_files()

#     existing_vms = list_vms()
#     for vm_name, config in vms.items():
#         if vm_name in existing_vms:
#             logging.info(f"{vm_name} already exists. Skipping...")
#             continue

#         copied = copy_image(vm_name)
#         resize_image(vm_name)

#         if copied:
#             configure_image(vm_name)

#         define_vm(vm_name, config)
#         logging.info(f"{vm_name} deployed and started.")

# if __name__ == "__main__":
#     main()
import os
import subprocess
import libvirt
import logging
import sys
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

vms = {
    #  "ubuntu": {"memory": 12288, "vcpu": 2, "network": "mgmt",  "ip": "10.219.94.155"},
    "c1": {"memory": 12288, "vcpu": 2, "network": "mgmt",  "ip": "10.219.90.101"},
    "p1": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.90.102"},
    "p2w1": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.90.103"},
    "p3w2": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.90.104"},
    "w3": {"memory": 32768, "vcpu": 8, "network": "mgmt", "ip": "10.219.90.105"},
}

libvirt_pool_dir = "/var/lib/libvirt/images"
base_image_name = "bionic-server-cloudimg-amd64.img"
base_image_url = f"https://cloud-images.ubuntu.com/bionic/current/{base_image_name}"
vm_root_pass = "juniper123"
ssh_key_path = "/root/.ssh/id_rsa.pub"
gateway = "10.219.94.129"
dns_server = "66.129.233.81"
subnet_mask = "/25"
interface_name = "enp1s0"

def system_setup():
    logging.info("Installing required packages and setting up environment...")
    run_cmd("apt update && apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager libguestfs-tools curl")
    run_cmd("systemctl enable --now libvirtd")
    run_cmd("systemctl is-active libvirtd")
    run_cmd("usermod -aG libvirt $USER")
    run_cmd("usermod -aG kvm $USER")

    logging.info("System setup complete. You may need to re-login for group changes to apply.")

def ensure_ssh_key_exists():
    if not os.path.isfile(ssh_key_path):
        logging.warning(f"SSH public key not found at {ssh_key_path}. Generating a new SSH key.")
        try:
            subprocess.run(f"ssh-keygen -t rsa -b 4096 -f {ssh_key_path[:-4]} -N ''", shell=True, check=True)
            logging.info("SSH key generated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to generate SSH key: {e}")
            sys.exit(1)
    else:
        logging.info(f"SSH public key found at {ssh_key_path}.")

def run_cmd(cmd):
    try:
        logging.info(f"Running command: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Command failed: {e}")
        sys.exit(1)

def check_and_download_base_image():
    base_image_path = f"/root/{base_image_name}"
    if not os.path.exists(base_image_path):
        logging.info(f"Base image not found. Downloading from {base_image_url}")
        run_cmd(f"curl -o {base_image_path} {base_image_url}")
    else:
        logging.info(f"Base image found at {base_image_path}")

def populate_hosts_file():
    logging.info("Skipping /etc/hosts population as this needs inventory parsing.")

def create_network_yaml_files():
    output_dir = "/root/paragon"
    os.makedirs(output_dir, exist_ok=True)

    for vm_name, config in vms.items():
        yaml_content = f"""network:
  ethernets:
    {interface_name}:
      dhcp4: no
      dhcp6: no
      addresses: [{config['ip']}{subnet_mask}]
      gateway4: {gateway}
      nameservers:
        addresses: [{dns_server}]
  version: 2
"""
        yaml_path = os.path.join(output_dir, f"{vm_name}.yaml")
        with open(yaml_path, "w") as yaml_file:
            yaml_file.write(yaml_content)
        logging.info(f"Generated network YAML for {vm_name} at {yaml_path}")

def list_vms():
    logging.info("Listing existing VMs...")
    conn = libvirt.open("qemu:///system")
    if conn is None:
        logging.error("Failed to open connection to qemu:///system")
        raise Exception("Failed to open connection to qemu:///system")
    vms_list = [vm.name() for vm in conn.listAllDomains()]
    conn.close()
    logging.info(f"Existing VMs: {vms_list}")
    return vms_list

def copy_image(vm_name):
    check_and_download_base_image()
    src = f"/root/{base_image_name}"
    dest = f"{libvirt_pool_dir}/{vm_name}.qcow2"
    if not os.path.exists(dest):
        logging.info(f"Copying base image for {vm_name}")
        run_cmd(f"cp {src} {dest}")
        os.chmod(dest, 0o660)
        return True
    logging.info(f"Image for {vm_name} already exists. Skipping copy.")
    return False

def resize_image(vm_name):
    image_path = f"{libvirt_pool_dir}/{vm_name}.qcow2"
    logging.info(f"Resizing image for {vm_name}")
    run_cmd(f"qemu-img resize {image_path} +200G")

def configure_image(vm_name):
    yaml_path = f"/root/paragon/{vm_name}.yaml"
    image_path = f"{libvirt_pool_dir}/{vm_name}.qcow2"
    run_cmd(f"""
        virt-customize -a {image_path} \
        --root-password password:{vm_root_pass} \
        --hostname {vm_name} \
        --upload {yaml_path}:/etc/netplan/00-installer-config.yaml \
        --mkdir /root/.ssh \
        --copy-in {ssh_key_path}:/root/.ssh/ \
        --copy {ssh_key_path}:/root/.ssh/authorized_keys \
        --run-command 'sed -i "s/.*PubkeyAuthentication yes/PubkeyAuthentication yes/g" /etc/ssh/sshd_config' \
        --run-command 'sed -i "s/.*PasswordAuthentication no/PasswordAuthentication yes/g" /etc/ssh/sshd_config' \
         --run-command 'sed -i "s/.*AllowTCPForwarding yes/AllowTCPForwarding yes/g" /etc/ssh/sshd_config' \
        --run-command 'sed -i "s/.*PermitRootLogin prohibit-password/PermitRootLogin yes/g" /etc/ssh/sshd_config' \
        --run-command 'sed -i "s/Unattended-Upgrade \\"1\\"/Unattended-Upgrade \\"0\\"/g" /etc/apt/apt.conf.d/20auto-upgrades' \
        --run-command 'dpkg-reconfigure -pmedium unattended-upgrades' \
        --run-command 'dpkg-reconfigure openssh-server'
    """)
def ensure_extra_disk_exists(vm_name, libvirt_pool_dir):
    """
    Ensure the extra disk for the VM exists. If not, create one with a size of 30GB.
    """
    extra_disk_path = f"{libvirt_pool_dir}/{vm_name}_extra.qcow2"
    if not os.path.exists(extra_disk_path):
        logging.info(f"Extra disk {extra_disk_path} not found. Creating a new 30GB disk...")
        run_cmd(f"qemu-img create -f qcow2 {extra_disk_path} 30G")
        logging.info(f"✅ Extra disk {extra_disk_path} created successfully.")
    else:
        logging.info(f"✅ Extra disk {extra_disk_path} already exists.")

def define_vm(vm_name, config):
    logging.info(f"Defining VM {vm_name}")
    
    # Path for additional 30GB disk
    extra_disk_path = f"{libvirt_pool_dir}/{vm_name}_extra.qcow2"
    ensure_extra_disk_exists(vm_name, libvirt_pool_dir)
  
    # Run virt-install with an additional disk for each VM
    run_cmd(f"""
        virt-install --name {vm_name} \
        --disk {libvirt_pool_dir}/{vm_name}.qcow2 \
        --disk {extra_disk_path},size=30 \
        --vcpus {config['vcpu']} \
        --cpu host-model \
        --memory {config['memory']} \
        --network bridge={config['network']} \
        --virt-type kvm \
        --import \
        --os-variant ubuntu20.04 \
        --graphics vnc \
        --serial pty \
        --noautoconsole \
        --console pty,target_type=virtio
    """)

def main():
    system_setup()
    populate_hosts_file()
    ensure_ssh_key_exists()
    check_and_download_base_image()
    create_network_yaml_files()

    existing_vms = list_vms()
    for vm_name, config in vms.items():
        if vm_name in existing_vms:
            logging.info(f"{vm_name} already exists. Skipping...")
            continue

        copied = copy_image(vm_name)
        resize_image(vm_name)

        if copied:
            configure_image(vm_name)

        define_vm(vm_name, config)
        logging.info(f"{vm_name} deployed and started.")

if __name__ == "__main__":
    main()
