Gestion IPAM et DNS avec Ansible
1. Introduction
Notre objectif est de développer des modules Ansible autonomes qui interagissent avec des APIs dans le fichier json  pour gérer les adresses IP et les enregistrements DNS. Ce projet est structuré autour de quatres modules principaux : `ipam_free_ip, reserve_ip, dns_register, manager_access`.

- Le module ipam_free_ip est chargé de sélectionner une adresse IP libre dans le système IPAM. 
- Si l'adresse IP est disponible, un hostname lui est attribué, à condition que ce dernier soit également libre. 
- Ensuite, le module manager_access permet d'associer un nom d'utilisateur (username) et un mot de passe (password) à cette adresse IP pour en gérer l'accès.

Chaque module fonctionne de manière indépendante, sans dépendance vis-à-vis des autres, tout en utilisant un fichier API commun, server.py, pour assurer la cohérence et la communication avec les systèmes distants.


### Module 1 : ipam_free_ip

Ce module est utilisé pour récupérer une adresse IP libre depuis le système IPAM.

Paramètres
`api_url` : L'URL de l'API IPAM (exemple : http://127.0.0.1:8000).

```yaml
- name: Obtenir une IP libre depuis IPAM
  ipam_free_ip:
    api_url: "http://127.0.0.1:8000"
  register: ipam_result
```

Le module retourne un objet JSON contenant l'adresse IP libre dans la clé response.free_ip.

### Module 2 : ipam_reserve_ip

Ce module permet de réserver une adresse IP libre et de lui associer un hostname dans le système IPAM.

Paramètres
- `api_url` : L'URL de l'API IPAM (exemple : http://127.0.0.1:8000).
- `ip` : L'adresse IP à réserver celle qu'on a récupérée via ipam_free_ip.
- `hostname`: Le hostname à associer à l'adresse IP.

```yaml
- name: Reserve IP and add hostname
  uri:
    url: "http://127.0.0.1:8000/ipam/reserve_ip"
    method: POST
    body_format: json
    body:
      ip: "{{ ipam_result.response.free_ip }}"
      hostname: "{{ hostname }}"
    return_content: no
  register: hostname_result
```

Le module retourne un objet JSON confirmant la réservation de l'IP et l'association du hostname.

### Module 3 : dns_register

Ce module permet d'enregistrer l'adresse IP et le hostname dans le système DNS.

Paramètres
- api_url : L'URL de l'API DNS (exemple : http://127.0.0.1:8000).
- ip : celle qu'on a recupérée dans free ip.
- hostname : le hostname comme variable dans le playbook.


```yaml
- name: Reserve IP and Hostname
  dns_register:
    api_url: "http://127.0.0.1:8000"
    ip: "{{ ipam_result.response.free_ip }}"
    hostname: "{{ hostname }}"
  register: result_ip
```
Le module retourne un objet JSON confirmant l'enregistrement DNS.

### Module 4 : manager_access

Ce module permet de gérer les accès en associant un nom d'utilisateur (username) et un mot de passe (password) à un hostname.

#### Paramètres
- `api_url  ` : L'URL de l'API de gestion des accès (exemple : http://127.0.0.1:8000).
- `hostname ` : On recupere hostname dans reserve_ip et dns
- `username ` : ROOT
- `password ` : Le mot de passe à associer (si non fourni, un mot de passe par défaut peut être généré).


```yaml
- name: Send POST request to manage_access
  uri:
    url: "http://127.0.0.1:8000/access/manage_secret"
    method: POST
    body_format: json
    body:
      hostname: "{{ hostname }}"
      username: "root"
    return_content: yes
    status_code: 201  # Accepter le code de statut 201
  register: response
```
#### Résultat
Le module retourne un objet JSON confirmant la création des informations d'accès.

## 3. Exécution des Modules
Chaque module peut être exécuté indépendamment sans nécessiter un playbook unique. Tous les modules utilisent le même fichier server.py pour l'API.

### 3.1 Prérequis
- Python 3.9
- Ansible
- Flask

### 3.2 Configuration de l'environnement
```sh
python -m venv venv
source venv/bin/activate
```
### 3.3 Lancement de l'API Flask
```sh
python3 server.py
```
### 3.4 Exécution des Modules
- Pour exécuter les modules  :

```sh
ansible-playbook playbook.yml
```
## 4. Structure des Fichiers
```sh
.
├── README.md
├── data
│   ├── access_list.json
│   ├── dns_list.json
│   └── ip_list.json
├── inventoty.ini
├── library
│   ├── dns_register.py
│   ├── ipam_free_ip.py
│   ├── manage_access_secret.py
│   └── reserve_ip.py
├── playbook.yml
└── server.py
```
### 5. Conclusion

Ce projet permet une gestion flexible et modulaire des adresses IP et des enregistrements DNS grâce à des modules Ansible indépendants. Chaque module fonctionne de manière autonome, avec ses propres fichiers JSON, ce qui facilite la maintenance et l'extension du système. L'utilisation d'une API Flask centralisée permet une intégration facile et une communication efficace entre les différents modules.