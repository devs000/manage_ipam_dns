from flask import Flask, jsonify, request
import json
import random
import string
import os

app = Flask(__name__)

IPAM_FILE="data/ip_list.json"
SECRET_FILE = "data/access_list.json"
DNS_FILE = "data/dns_list.json"


@app.route('/ipam/free_ip', methods=['GET'])
def get_free_ip():
    # Simuler une réponse avec une IP libre
    try:
        with open(IPAM_FILE, 'r') as file:
            ipam_data = json.load(file)
        ips_libre = [item for item in ipam_data['ipam'] if item['hostname'] == ""]

        if not ips_libre:
            response = {
            "free_ip": ""
             }
            
            return jsonify(response), 201

        chosen_ip_info = random.choice(ips_libre)
        response = {
            "free_ip": chosen_ip_info['ip']
             }

        return jsonify(response), 201
    

    except Exception as e:
        response = {"message": e }
        return jsonify(response), 500
    

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
        return jsonify({"message": "IP reserved with the correct hostname"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def generate_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for i in range(length))
    return password


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
            if item['hostname'] == hostname:
                return jsonify({"message": "hostname already exists"}), 400
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
