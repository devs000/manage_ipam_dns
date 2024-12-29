from ansible.module_utils.basic import AnsibleModule
import requests
import json

def main():
    module_args = dict(
        api_url=dict(type="str", required=True),
        hostname=dict(type="str", required=True),
        ip=dict(type="str", required=True)
    )

    module = AnsibleModule(argument_spec=module_args)
    api_url = module.params["api_url"]
    host = module.params["hostname"]
    ip_addr = module.params["ip"]

    data = {
        "ip": ip_addr,
        "hostname": host
    }

    # Appeler l'API
    try:
        response = requests.post(f"{api_url}/ipam/reserve_ip", json=data)

        # Vérifier si la requête a réussi
        response.raise_for_status()

        # Extraire les données de la réponse
        data = response.json()

        # Sortir avec les données de la réponse
        module.exit_json(changed=True, response=data)

    except requests.exceptions.HTTPError as http_err:
        # Gérer les erreurs HTTP
        if response.status_code == 500:
            module.fail_json(msg=f"Erreur HTTP : {http_err.response.json().get('message', 'Erreur interne du serveur')}", status_code=500)
        elif response.status_code == 400:
            module.fail_json(msg=f"Erreur HTTP : {http_err.response.json().get('message', 'Requête incorrecte')}", status_code=400)
        elif response.status_code == 401:
            module.fail_json(msg=f"Erreur HTTP : {http_err.response.json().get('message', 'Non autorisé')}", status_code=401)
        elif response.status_code == 403:
            module.fail_json(msg=f"Erreur HTTP : {http_err.response.json().get('message', 'Interdit')}", status_code=403)
        elif response.status_code == 404:
            module.fail_json(msg=f"Erreur HTTP : {http_err.response.json().get('message', 'Non trouvé')}", status_code=404)
        elif response.status_code == 409:
            module.fail_json(msg=f"Erreur HTTP : {http_err.response.json().get('message', 'Conflit')}", status_code=409)
        elif response.status_code == 429:
            module.fail_json(msg=f"Erreur HTTP : {http_err.response.json().get('message', 'Trop de requêtes')}", status_code=429)
        else:
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
