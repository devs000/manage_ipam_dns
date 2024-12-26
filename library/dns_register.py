

from ansible.module_utils.basic import AnsibleModule
import requests
import json
import random
import string

def generate_username(hostname):
    """Generate a username based on the hostname."""
    return f"user_{hostname.replace('.', '_')}"

def generate_password(length=12):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def main():
    module_args = dict(
        api_url=dict(type="str", required=True),
        ip=dict(type="str", required=True),
        hostname=dict(type="str", required=False),
        dns_file=dict(type="str", required=True),
    )

    module = AnsibleModule(argument_spec=module_args)
    url = module.params["api_url"]
    ip = module.params["ip"]
    hostname = module.params["hostname"]
    dns_file = module.params["dns_file"]

    try:
        # Lire le fichier dns_list.json
        with open(dns_file, 'r') as file:
            dns_data = json.load(file)

        # Vérifier si l'IP existe déjà
        existing_entry = next((entry for entry in dns_data['dns'] if entry['ip'] == ip), None)

        if existing_entry:
            module.exit_json(changed=False, message="IP already exists in DNS list")
        else:
            # Générer un nom d'utilisateur et un mot de passe
            username = generate_username(hostname)
            password = generate_password()

            # Ajouter la nouvelle entrée
            new_entry = {"ip": ip, "hostname": hostname, "username": username, "password": password}
            dns_data['dns'].append(new_entry)

            # Écrire les modifications dans le fichier dns_list.json
            with open(dns_file, 'w') as file:
                json.dump(dns_data, file, indent=4)

            # Faire une requête POST vers l'API
            payload = {"ip": ip, "hostname": hostname, "username": username, "password": password}
            response = requests.post(f"{url}/dns/register_dns", json=payload)
            response.raise_for_status()
            module.exit_json(changed=True, message="DNS entry registered successfully")

    except requests.exceptions.RequestException as e:
        module.fail_json(msg=str(e))
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == "__main__":
    main()
