from flask import Flask, request, jsonify
import sys
import os
import yaml
 

MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print(f"Project root directory: {MAIN_DIR}")
if MAIN_DIR not in sys.path:
    sys.path.append(MAIN_DIR)

from flask_restx import Api, Resource, fields
from src.pipeline.pipeline import Pipeline 

# Optional: if you have a config.yaml for model settings:
# e.g., model_name, model_type, api_key
CONFIG_PATH = os.path.join("config.yaml")
with open(CONFIG_PATH, "r") as config_file:
    config = yaml.safe_load(config_file)

app = Flask(__name__)
api = Api(app, version='1.0', title='Q&A Pipeline API', 
          description='API for Wikipedia Q&A pipeline')


model_name = config['qa_stage']['model_name']
model_type = config['qa_stage']['model_type']
api_key = config['qa_stage'].get('api_key', None)

# Create a single pipeline instance for all requests
pipeline = Pipeline(model_name=model_name, model_type=model_type, api_key=api_key)


qa_model = api.model('QAPayload', {
    'keyword': fields.String(required=True, description='Keyword for Wikipedia search'),
    'question': fields.String(required=True, description='Question to be answered')
})


@api.route('/qa')
class QAPipelineResource(Resource):
    @api.expect(qa_model)
    def post(self):
        """
        POST /qa
        Body JSON: { "keyword": "some topic", "question": "what about X?" }
        
        Returns a JSON list of records with the final Q&A results.
        """
        data = request.json
        keyword = data['keyword']
        question = data['question']
        
        # Run the pipeline with the user-supplied keyword & question
        result_df = pipeline.run(keyword, question)
        
        # Convert to a list of dicts to return as JSON
        result_list = result_df.to_dict(orient='records')
        
        return jsonify(result_list)


if __name__ == "__main__":
    # Example: run on port 5000, accessible from all IPs
    app.run(host='0.0.0.0', port=5000, debug=True)