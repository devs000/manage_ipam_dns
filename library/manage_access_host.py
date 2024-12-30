from ansible.module_utils.basic import AnsibleModule
import requests
import json

def main():
    module_args = dict(
        api_url=dict(type="str", required=True),
        username=dict(type="str", required=True),
        password=dict(type="str", required=True)
    )

    module = AnsibleModule(argument_spec=module_args)
    api_url = module.params["api_url"]
    username = module.params["username"]
    password = module.params["password"]

    data = {
        "username": username,
        "password": password
    }

    try:
        # Appeler l'API
        response = requests.post(f"{api_url}/manage_access", json=data)

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
        module.fail_json(msg=f"Erreur HTTP : {e}", status_code=response.status_code)
    except Exception as e:
        # Gérer les autres erreurs inattendues
        module.fail_json(msg=f"Une erreur inattendue s'est produite : {e}", status_code=500)

if __name__ == '__main__':
    main()
