## Projet : Gestion IPAM et DNS avec Ansible

### 1. Introduction
Notre objectif est de créer des modules Ansible qui consomment des APIs distantes pour gérer les adresses IP et les enregistrements DNS. Ce projet se compose de trois modules principaux : `ipam_free_ip`, `dns_register`, et `manager_access`.


### 2. Module IPAM : ipam_free_ip

Le module `ipam_free_ip` sélectionne une adresse IP disponible de manière aléatoire à partir d'un fichier JSON.

- **Exemple de fichier JSON pour ce module :**

```json
{
  "ipam": [
    {"ip": "1.1.1.1", "hostname": ""},
    {"ip": "1.1.1.2", "hostname": ""}
  ]
}
``` 

### 3. Module DNS : 
Le module dns_register teste la validation de l'adresse IP sélectionnée par le module IPAM. Ensuite, il vérifie si l'IP n'est pas déjà utilisée, puis l'ajoute dans un fichier dns.json. 

- Voici un exemple de fichier JSON pour ce module :

```json
{
  "dns": [
    {"ip": "1.1.1.1", "hostname": ""},
    {"ip": "1.1.1.2", "hostname": ""}
  ]
}
```
### 4. Module Accès Manager : manager_access
Le module manager_access génère les noms d'utilisateur et mots de passe pour chaque IP, représentant un serveur distant. 

- Voici un exemple de fichier JSON pour ce module :

```json
{
  "manager_access": [
    {"user": "", "hostname": "", "password": ""},
    {"user": "", "hostname": "", "password": ""}
  ]
}
```

### 5. Exécution de playbook et de server Flask

- Prérequis
```sh
  - Python 3.9
  - Ansible
  - Flask
```
```sh
python -m venv venv
source venv/bin/activate
```
```sh
python3  server.py
```

```sh
ansible-playbook  playbook.yml
```



