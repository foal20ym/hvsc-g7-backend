from apispec import APISpec
from flask import Flask, jsonify, render_template, send_from_directory, redirect, url_for
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='./swagger/templates')

@app.route('/')
def index():
    """Redirect to Swagger documentation"""
    return redirect(url_for('swagger_docs'))

spec = APISpec(
    title='HVSC-G7-Backend',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())

class PositionSchema(Schema):
    longitude = fields.Float()
    latitude = fields.Float()
    timestamp = fields.DateTime()

class MoverResponseSchema(Schema):
    moverId = fields.Int()
    positions = fields.List(fields.Nested(PositionSchema))

@app.route('/mover/<int:moverId>')
def mover(moverId):
    """Get the information of a single mover by moverId
    ---
    get:
        description: Get the information of a single mover by moverId
        parameters:
          - in: path
            name: moverId
            schema:
              type: integer
            required: true
            description: ID of the mover
        responses:
            200:
                description: Return the information of a mover by moverId
                content:
                    application/json:
                        schema: MoverResponseSchema
    """

    dummy_data = {
        'moverId': moverId,
        'positions': [
            {
                'longitude': 53.13,
                'latitude': 109.09,
                'timestamp': '2021-07-01T00:00:00Z'
            }, 
            {
                'longitude': 53.15,
                'latitude': 109.10,
                'timestamp': '2021-07-01T00:01:00Z'
            }
        ]
    }

    return jsonify(dummy_data)

with app.test_request_context():
    spec.path(view=mover)

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', secure_filename(path))

if __name__ == '__main__':
    app.run(debug=True)