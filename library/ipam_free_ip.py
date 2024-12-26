
from ansible.module_utils.basic import AnsibleModule
import requests
import json
import random

def generate_hostname(ip):
    """Generate a hostname based on the IP address."""
    return f"host_{ip.replace('.', '_')}"

def main():
    
    module_args = dict(
        api_url=dict(type="str", required=True),
        ipam_file=dict(type="str", required=True),
    )
    module = AnsibleModule(argument_spec=module_args) 
    api_url = module.params["api_url"]  
    ipam_file = module.params["ipam_file"]  

    try:
        with open(ipam_file, 'r') as file:
            ipam_data = json.load(file)

        ips = [item for item in ipam_data['ipam'] if item['hostname'] == ""]

        if not ips:
            module.fail_json(msg="IP indisponible")

        chosen_ip_info = random.choice(ips)
        chosen_ip_info['hostname'] = generate_hostname(chosen_ip_info['ip'])

        response = requests.get(f"{api_url}/ipam/free_ip") 
        response.raise_for_status()
        data = response.json()
        
        module.exit_json(changed=True, free_ip=chosen_ip_info['ip'], hostname=chosen_ip_info['hostname'])

    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == "__main__":
    main()
