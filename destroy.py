import subprocess
import os
from json_utils import load_json_file, extract_values

# nodes = ["p1","c1","p2w1","p3w2","w3"]
data = load_json_file("sample.json")


nodes=extract_values(data,"hostname")
# print(nodes)
for node in nodes:
    try:
        subprocess.run(["virsh", "destroy", node], check=True)
        print(f"Destroyed {node}")
    except subprocess.CalledProcessError:
        print(f"Failed to destroy {node} (might not be running)")

    try:
        subprocess.run(["virsh", "undefine", node], check=True)
        print(f"Undefined {node}")
    except subprocess.CalledProcessError:
        print(f"Failed to undefine {node} (might not be defined)")

    image_path = f"/var/lib/libvirt/images/{node}.qcow2"
    try:
        os.remove(image_path)
        print(f"Deleted disk image: {image_path}")
    except FileNotFoundError:
        print(f"Disk image {image_path} not found, skipping deletion")
    except Exception as e:
        print(f"Error deleting {image_path}: {e}")