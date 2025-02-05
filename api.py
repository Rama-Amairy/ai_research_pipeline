from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from pipeline import execute_pipeline
#from flask_restplus import Api, Resource, fields
import sys
import os

# Add project root to Python path
MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(MAIN_DIR)

app = Flask(__name__)
api = Api(app, version='1.0', title='Q&A Pipeline API', description='API for Wikipedia Q&A pipeline')

qa_model = api.model('QAPayload', {
    'keyword': fields.String(required=True, description='Keyword for Wikipedia search'),
    'question': fields.String(required=True, description='Question to be answered')
})

@api.route('/qa')
class QAPipeline(Resource):
    @api.expect(qa_model)
    def post(self):
        data = request.json
        keyword = data['keyword']
        question = data['question']
        result = execute_pipeline(keyword, question)
        return jsonify(result.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
