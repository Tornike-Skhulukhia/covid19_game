from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/covid19_game/save_data', methods=['POST'])
def index():
    print(dict(request.form))
    return jsonify({'OK': True})
    # return jsonify({'OK': False})


app.run(debug=True)
