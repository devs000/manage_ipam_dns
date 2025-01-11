from flask import Flask, jsonify, request
import json
import random
import string
import os
import re


app = Flask(__name__)

IPAM_FILE="data/ip_list.json"
SECRET_FILE = "data/access_list.json"
DNS_FILE = "data/dns_list.json"

#_____________________________________________________________________________________________________
ipv4_regex = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')


@app.route('/ipam/free_ip', methods=['GET'])
def get_free_ip():
    try:
        with open(IPAM_FILE, 'r') as file:
            ipam_data = json.load(file)
        
        # Filtrer les IPs libres (hostname vide)
        ips_libre = [item for item in ipam_data['ipam'] if item['hostname'] == ""]
        
        if not ips_libre:
            response = {"free_ip": ""}
            return jsonify(response), 200 
        
        valid_ips = [] 
        for item in ips_libre:
            if ipv4_regex.match(item['ip']):  
                valid_ips.append(item) 

        if not valid_ips:
            response = {
                "free_ip": "",
                "message": "No valid IPv4 address available."
            }
            return jsonify(response), 200

            # Sélectionner une IP aléatoire
        chosen_ip_info = random.choice(ips_libre)
        response = {
                "free_ip": chosen_ip_info['ip']
            }
        return jsonify(response), 200
    except Exception as e:
        response = {"message": str(e)}
        return jsonify(response), 500
#_____________________________________________________________________________________________________

@app.route('/ipam/reserve_ip', methods=['POST'])
def reserve_ip():

    data = request.json
    ip = data.get('ip')
    hostname = data.get('hostname')
    print(f"Received request to reserve IP: {ip} for hostname: {hostname}")

    # Charger le fichier JSON
    try:
        with open(IPAM_FILE, 'r') as f:
            ipam_data = json.load(f)
    except FileNotFoundError:
        return jsonify({"message": f"File '{IPAM_FILE}' not found."}), 404

    # Vérifier si le hostname existe déjà
    for item in ipam_data['ipam']:
        if item.get('hostname') == hostname:
            return jsonify({"message": f"Hostname '{hostname}' is already in use by another IP."}), 400

    # Vérifier si l'IP existe déjà
    for item in ipam_data['ipam']:
        if item['ip'] == ip:
            if item.get('hostname') == "":
                # Ajouter le hostname à l'IP existante
                item['hostname'] = hostname
                with open(IPAM_FILE, 'w') as f:
                    json.dump(ipam_data, f)
                return jsonify({"message": f"Hostname '{hostname}' has been successfully assigned to IP '{ip}'.", "hostname": hostname}), 200
            else:
                return jsonify({"message": f"IP '{ip}' is already reserved by another hostname."}), 400

    # Si l'IP n'est pas trouvée dans le fichier JSON, ajouter une nouvelle entrée
    ipam_data['ipam'].append({"ip": ip, "hostname": hostname})
    with open(IPAM_FILE, 'w') as f:
        json.dump(ipam_data, f)
    return jsonify({"message": f"New entry added: IP '{ip}' with hostname '{hostname}'.", "hostname": hostname}), 201

#______________________________________________________________________________________________

@app.route('/dns/reserve_dns', methods=['POST'])
def reservation_ip():
    data = request.json
    ip = data.get('ip')
    hostname = data.get('hostname')
    print(f"Received request to reserve IP: {ip} for hostname: {hostname}")  # Log the received data

    try:
        with open(DNS_FILE, 'r') as file:
            dns_data = json.load(file)
        for item in dns_data['dns']:
            if item['ip'] == ip:
                if item['hostname'] == hostname:
                    return jsonify({"message": "IP already registered with the correct hostname"}), 200
                else:
                    return jsonify({"message": "IP is already reserved by another hostname"}), 400
        # If IP is not reserved, register it
        dns_data['dns'].append({
            "ip": ip,
            "hostname": hostname
        })
        # Save the updated DNS data back to the file
        with open(DNS_FILE, 'w') as file:
            json.dump(dns_data, file, indent=4)
        return jsonify({"message": f"IP {ip} reserved with the correct hostname {hostname}."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
# #_____________________________________________________________________________________________________

def generate_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for i in range(length))
    return password

# #_____________________________________________________________________________________________________

@app.route('/access/manage_secret', methods=['POST'])
def manager_secret():
    data = request.json
    hostname = data.get('hostname')
    username = data.get('username')

    try:
        if not os.path.exists(SECRET_FILE):
            return jsonify({"message": f"File {SECRET_FILE} does not exist"}), 500

        with open(SECRET_FILE, 'r') as f:
            secret_data = json.load(f)

        for item in secret_data['manager_access']:
            if item['hostname'] == hostname and item['username'] == username:
                return jsonify({"message": "hostname already exists"}), 500
        password = generate_password()
        secret_data["manager_access"].append({
            "hostname": hostname,
            "username": username,
            "password": password
        })
        with open(SECRET_FILE, 'w') as f:
            json.dump(secret_data, f, indent=4)
            app.logger.debug(f"Updated secret data: {secret_data}")

        return jsonify({"message": "Parameters added successfully", "hostname": hostname, "username": username, "password": password}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500

#_____________________________________________________________________________________________________

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
