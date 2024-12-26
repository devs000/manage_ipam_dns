
from ansible.module_utils.basic import AnsibleModule
import json
import random
import string

def generate_username(hostname):
    """Generate a username based on the hostname."""
    return f"user_{hostname.replace('.', '_')}"

def generate_password(length=12):
    """Generate a random password."""
    c = string.ascii_letters + string.digits + '#@&é%$*+=!?'
    return ''.join(random.choice(c) for i in range(length))

def main():
    module_args = dict(
        dns_file=dict(type="str", required=True),
        manager_access_file=dict(type="str", required=True),
    )

    module = AnsibleModule(argument_spec=module_args)
    dns_file = module.params["dns_file"]
    manager_access_file = module.params["manager_access_file"]

    try:
        # Lire le fichier dns_list.json
        with open(dns_file, 'r') as file:
            dns_data = json.load(file)

        # Lire (read) le fichier manager_access.json
        with open(manager_access_file, 'r') as file:
            manager_access_data = json.load(file)

        # Générer des noms d'utilisateur et des mots de passe pour chaque hostname
        for entry in dns_data['dns']:
            host = entry['hostname']
            existing_entry = next((item for item in manager_access_data['manager_access'] if item['hostname'] == host), None)

            if not existing_entry:
                username = generate_username(host)
                password = generate_password()
                new_entry = {"user": username, "hostname": host, "password": password}
                manager_access_data['manager_access'].append(new_entry)

        # Écrire (write) les modifications dans le fichier manager_access.json
        with open(manager_access_file, 'w') as file:
            json.dump(manager_access_data, file, indent=4)

        module.exit_json(changed=True, message="Username & passwords generés avec succes")

    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == "__main__":
    main()
