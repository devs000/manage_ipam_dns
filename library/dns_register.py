from ansible.module_utils.basic import AnsibleModule
import requests
import json

def main():
    module_args = dict(
        api_url=dict(type="str", required=True),
        ip=dict(type="str", required=True),
        hostname=dict(type="str", required=True)
    )

    module = AnsibleModule(argument_spec=module_args)
    api_url = module.params["api_url"]
    ip = module.params["ip"]
    hostname = module.params["hostname"]

    data = {
        "ip": ip,
        "hostname": hostname
    }

    try:
        # Appeler l'API
        response = requests.post(f"{api_url}/dns/reserve_dns", json=data)
        # Vérifier si la requête a réussi
        response.raise_for_status()
        # Extraire les données de la réponse
        data = response.json()
        # Sortir avec les données de la réponse
        module.exit_json(changed=True, response=data)

    except requests.exceptions.RequestException as e:
        # Gérer les erreurs de connexion
        module.fail_json(msg=f"Erreur de connexion à l'API : {e}", status_code=500)
    except requests.exceptions.HTTPError as e:
        # Gérer les erreurs HTTP
        module.fail_json(msg=f"Erreur HTTP : {e}", status_code=response.status_code, response_text=response.text)    
    except Exception as e:
        # Gérer les autres erreurs inattendues
        module.fail_json(msg=f"Une erreur inattendue s'est produite : {e}", status_code=500)

if __name__ == "__main__":
    main()