import re

# Hardcoded variables
k8s_masters = ["10.29.90.102", "10.219.90.103", "10.219.90.104"]
k8s_workers = ["10.219.90.105"]
tsdb_nodes = []
storage_nodes = ["10.219.90.103", "10.219.90.104", "10.219.90.105"]
ansible_user = "root"
ssh_key_file = "config/id_rsa"
ansible_password = "juniper123"
k8s_cluster_name = "k8scluster"
# Derive storage_master_nodes and storage_worker_nodes
storage_master_nodes = sorted([node for node in storage_nodes if node in k8s_masters])
storage_worker_nodes = sorted([node for node in storage_nodes if node in k8s_workers])

# Input and output file paths
input_file = 'inventory'
output_file = 'inventory_updated'

# Read input file
with open(input_file, 'r') as file:
    data = file.read()

# Replace variables using regex
replacements = {
    r'\{master_hosts\}': '\n'.join([f"            {host}: {{}}" for host in k8s_masters]),
    r'\{worker_hosts\}': '\n'.join([f"            {host}: {{}}" for host in k8s_workers]),
    r'\{storage_master_hosts\}': '\n'.join([f"            {host}: {{}}" for host in storage_master_nodes]),
    r'\{storage_worker_hosts\}': '\n'.join([f"            {host}: {{}}" for host in storage_worker_nodes]),
   r'\{ansible_user\}': ansible_user,
    r'\{ssh_key_file\}': ssh_key_file,
    r'\{ansible_password\}': ansible_password,
    r'\{k8s_cluster_name\}': k8s_cluster_name
}

for pattern, replacement in replacements.items():
    data = re.sub(pattern, replacement, data)

# Write output file
with open(output_file, 'w') as file:
    file.write(data)

print(f"Variables replaced and saved to {output_file}")