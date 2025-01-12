from ansible.module_utils.basic import AnsibleModule
import requests
import json

def main():
    module_args = dict(
        api_url=dict(type="str", required=True)  # Plus besoin du paramètre 'ip'
    )

    module = AnsibleModule(argument_spec=module_args)
    api_url = module.params["api_url"]

    try:
        response = requests.get(f"{api_url}/ipam/free_ip")  # Pas de paramètre 'ip'
        # Vérifier si la requête a réussi
        response.raise_for_status()
        # Extraire les données de la réponse
        data = response.json()
        # Sortir avec les données de la réponse
        module.exit_json(changed=True, response=data)

    except requests.exceptions.HTTPError as http_err:
        # Gérer les erreurs HTTP
        module.fail_json(msg=f"Erreur HTTP : {http_err}", status_code=response.status_code)
    except requests.exceptions.ConnectionError as conn_err:
        # Gérer les erreurs de connexion
        module.fail_json(msg=f"Erreur de connexion : {conn_err}", status_code=503)
    except requests.exceptions.Timeout as timeout_err:
        # Gérer les erreurs de timeout
        module.fail_json(msg=f"Erreur de timeout : {timeout_err}", status_code=504)
    except requests.exceptions.RequestException as req_err:
        # Gérer les autres erreurs de requête
        module.fail_json(msg=f"Erreur de requête : {req_err}", status_code=500)
    except json.JSONDecodeError as json_err:
        # Gérer les erreurs de décodage JSON
        module.fail_json(msg=f"Erreur de décodage JSON : {json_err}", status_code=500)
    except Exception as e:
        # Gérer les autres erreurs inattendues
        module.fail_json(msg=f"Une erreur inattendue s'est produite : {e}", status_code=500)

if __name__ == "__main__":
    main()