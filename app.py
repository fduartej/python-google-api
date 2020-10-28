import compliance_google as compliance

import json

from flask import request
from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    data = {
        "health": "active",
        "message": "Google Due Diligence"
    }
    json_msg = json.dumps(data)
	
    return json_msg

@app.route("/compliance-duediligence", methods=['POST'])
def exec_duediligence():
    req_data = request.get_json()
    json_msg = compliance.due_diligence(req_data)

    return json_msg

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)