from flask import Flask, jsonify, request
import json
import random
import string

app = Flask(__name__)

ipam_file="ip_list.json"
access_file = "access_list.json"

@app.route('/ipam/free_ip', methods=['GET'])
def get_free_ip():
    # Simuler une réponse avec une IP libre
    try:
        with open(ipam_file, 'r') as file:
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
    
@app.route('/ipam/reserve_ip', methods=['POST'])
def reservation_ip():
    data = request.json
    ip = data.get('ip')
    hostname = data.get('hostname')

    try:
        with open(ipam_file, 'r') as file:
            ipam_data = json.load(file)
    
        ips_reserve = [item for item in ipam_data['ipam'] if item['ip'] == ip]
        
        if not ips_reserve:
            response = { "message": "IP not exist"}
            return jsonify(response), 500
        
        if len(ips_reserve)>1:
            response = { "message": "IP exite plusieurs fois  "}
            return jsonify(response), 500
        
        if ips_reserve[0]['hostname'] != "" :
            if ips_reserve[0]['hostname'] == str(hostname[0]):
                response = { "message": "IP deja enregistré  avec le bon hostname" }
                return jsonify(response), 200
        
            if ips_reserve[0]['hostname'] != str(hostname[0]):
                response = { "message": "IP est déja reservé par un autre hostname " }
                return jsonify(response), 400
        

        for item in ipam_data['ipam']:
            if item['ip'] == ip:
                item['hostname'] = str(hostname[0])
      
        # Save the updated IPAM data back to the file
        with open(ipam_file, 'w') as file:
            json.dump(ipam_data, file)

        response = { "message": "IP est reservé avec un bon hostname " }
        return jsonify(response), 200

    except Exception as e:
        response = { "message": e }
        return jsonify(response), 500    


@app.route('/manage_access', methods=['POST'])
def manage_access():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        response = {"message": "Username and password are required"}
        return jsonify(response), 400

    try:
        # Lire le fichier ip_list.json
        with open(ipam_file, 'r') as f:
            ipam_data = json.load(f)

        # Lire le fichier access_file.json
        try:
            with open(access_file, 'r') as f:
                access_data = json.load(f)
        except FileNotFoundError:
            access_data = {"manager_access": []}

        # Récupérer les hostnames non vides et les enregistrer dans access_file.json
        for item in ipam_data['ipam']:
            if item['hostname'] != "":
                # Vérifier si le hostname existe déjà dans access_data["manager_access"]
                host_exists = False
                for tab in access_data["manager_access"]:
                    if tab['hostname'] == item['hostname']:
                        host_exists = True
                        break

                if not host_exists:
                    access_data["manager_access"].append({
                        "ip": item['ip'],
                        "hostname": item['hostname'],
                        "username": username,
                        "password": password
                    })

        # Sauvegarder les données mises à jour dans le fichier access_file.json
        with open(access_file, 'w') as file:
            json.dump(access_data, file, indent=4)

        response = {"message": "Access managed successfully"}
        return jsonify(response), 200

    except Exception as e:
        response = {"message": str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
