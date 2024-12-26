from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/ipam/free_ip', methods=['GET'])
def get_free_ip():
    # Simuler une réponse avec une IP libre
    response = {
        "message": "It's Ok"
    }
    
    return jsonify(response), 200

@app.route('/dns/register_dns', methods=['POST'])
def register_dns():
    data = request.json
    ip = data.get('ip')
    hostname = data.get('hostname')
    # Ajoutez ici la logique pour enregistrer l'entrée DNS
    return jsonify({"message": "DNS entry registered successfully"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
