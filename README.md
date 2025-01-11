# Gestion IPAM et DNS avec Ansible
## 1. Introduction
Notre objectif est de créer des modules Ansible indépendants qui consomment des APIs distantes pour gérer les adresses IP et les enregistrements DNS. Ce projet se compose de trois modules principaux : ipam_free_ip, dns_register, et manager_access. Chaque module peut être exécuté indépendamment sans dépendre des autres, et tous utilisent le même fichier server.py pour l'API.

## 2. Modules
### 2.1 Module IPAM : ipam_free_ip
Le module ipam_free_ip sélectionne une adresse IP disponible de manière aléatoire à partir d'un fichier JSON dédié.

Exemple de fichier JSON pour ce module :

```json
{
  "ipam": [
    {"ip": "1.1.1.1", "hostname": ""},
    {"ip": "1.1.1.2", "hostname": ""}
  ]
}
```
### 2.2 Module DNS : dns_register
Le module dns_register fonctionne de manière totalement indépendante du module ipam_free_ip. Il utilise son propre fichier dns.json pour valider et enregistrer les adresses IP et les noms d'hôte.

- Fonctionnalités :

  Valide une adresse IP fournie en entrée.
  Vérifie si l'adresse IP est déjà utilisée dans le fichier dns.json.
  Ajoute l'adresse IP et le nom d'hôte dans le fichier dns-list.json si elle est disponible.

Exemple de fichier JSON pour ce module :

```json
{
  "dns": [
    {"ip": "1.1.1.1", "hostname": "server1"},
    {"ip": "1.1.1.2", "hostname": "server2"}
  ]
}
```
### 2.3 Module Accès Manager : manager_access
Le module manager_access génère des noms d'utilisateur et des mots de passe pour chaque IP, représentant un serveur distant. Il fonctionne indépendamment des autres modules.

Exemple de fichier JSON pour ce module :

```json
{
  "manager_access": [
    {"user": "admin1", "hostname": "server1", "password": "pass123"},
    {"user": "admin2", "hostname": "server2", "password": "pass456"}
  ]
}
```
## 3. Exécution des Modules
Chaque module peut être exécuté indépendamment sans nécessiter un playbook unique. Tous les modules utilisent le même fichier server.py pour l'API.

### 3.1 Prérequis
Python 3.9

Ansible

Flask

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
- Pour exécuter un module spécifique, utilisez la commande suivante :

```sh
ansible-playbook <nom_du_module>.yml
```
- Par exemple :
- Pour exécuter le module ipam_free_ip :
```sh
ansible-playbook ipam_free_ip.yml
```
- Pour exécuter le module dns_register :

```sh
ansible-playbook dns_register.yml
```
- Pour exécuter le module manager_access :

```sh
ansible-playbook manager_access.yml
```
## 4. Structure des Fichiers
```sh
.
├── server.py                # API Flask pour les modules
├── ipam_free_ip.yml         # Playbook pour le module IPAM
├── dns_register.yml         # Playbook pour le module DNS
├── manager_access.yml       # Playbook pour le module Manager Access
├── data/
│   ├── ip-list.json            # Fichier JSON pour le module IPAM
│   ├── dns-list.json             # Fichier JSON pour le module DNS
│   └── access-list.json  # Fichier JSON pour le module Manager Access
|
└── README.md                # Documentation du projet
```
### 5. Conclusion

Ce projet permet une gestion flexible et modulaire des adresses IP et des enregistrements DNS grâce à des modules Ansible indépendants. Chaque module fonctionne de manière autonome, avec ses propres fichiers JSON, ce qui facilite la maintenance et l'extension du système. L'utilisation d'une API Flask centralisée permet une intégration facile et une communication efficace entre les différents modules.