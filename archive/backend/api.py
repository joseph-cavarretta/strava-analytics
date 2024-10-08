from flask import Flask, jsonify, request
from errors import APIError, MessageError

app = Flask(__name__)


@app.errorhandler(404)
def handle_exception(err):
    """Returns JSON 404 error"""
    return jsonify(error=str(err)), 404


@app.errorhandler(500)
def handle_exception(err):
    """Returns JSON 500 error"""
    return jsonify(error=str(err)), 500


@app.errorhandler(APIError)
def handle_exception(err):
    """Returns custom JSON when APIError is raised"""
    response = {'error': err.description, 'message': ''}
    if len(err.args) > 0:
        response['message'] = err.args[0]
    app.logger.error(f"{err.description}: {response['message']}")
    return jsonify(response), err.code


@app.route('/health', methods=['GET'])
def index():
    """Returns message if service is running"""
    return jsonify(message='Activity service is running!'), 200


@app.route('/summary', methods=['GET'])
def get_data():
    """Returns full processed activity dataset"""
    try:
        content = request.get_json()
        response = jsonify(message=content['message'])
        return response, 200
    except KeyError:
        raise MessageError('Please reformat request and try again')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)