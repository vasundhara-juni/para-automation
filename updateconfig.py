import re
import subprocess

# Define your variables
INGRESS_VIP = "10.0.0.100"
Insights_VIP = "10.0.0.101"
NTP_SERVER = "ntp.juniper.net"
WEB_HOSTNAME = "para.example.net"
NGINX_INGRESS_VIP = "10.0.0.102"
CRPD_PEER = "10.0.1.1"
BGP_ASN= "65000"    
# Input and output file paths
input_file = 'config.yml'
output_file = 'pathfinder_config_updated.yml'

# Read input file
with open(input_file, 'r') as file:
    data = file.read()

# Replace variables using regex
replacements = {
    r'\$INGRESS_VIP': INGRESS_VIP,
    r'\$Insights_VIP': Insights_VIP,
    r'\$NTP_SERVER': NTP_SERVER,
    r'\$WEB_HOSTNAME': WEB_HOSTNAME,
    r'\$NGINX_INGRESS_VIP': NGINX_INGRESS_VIP,
    r'\$CRPD_PEER': CRPD_PEER,
    r'\{\{bgp_asn\}\}': BGP_ASN

}

for pattern, replacement in replacements.items():
    data = re.sub(pattern, replacement, data)

# Write output file
with open(output_file, 'w') as file:
    file.write(data)

print(f"Variables replaced and saved to {output_file}")

# # Copy the updated file to the server using scp
# remote_user = "user"
# remote_host = "server.example.com"
# remote_path = "/path/to/destination"

# scp_command = ["scp", output_file, f"{remote_user}@{remote_host}:{remote_path}"]
# try:
#     subprocess.run(scp_command, check=True)
#     print(f"File transferred to {remote_user}@{remote_host}:{remote_path}")
# except subprocess.CalledProcessError as e:
#     print(f"Error during file transfer: {e}")
