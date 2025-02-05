import logging
import os

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging.basicConfig(
        filename='logs/pipeline.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


import yaml
from src.load_data import LoadDataStage
from src.clean_data import TransformStage
from src.qa_transform import QATransformStage
from logging import getLogger

def execute_pipeline(keyword: str, question: str):
    # Set up logging
    setup_logging()
    logger = getLogger("Pipeline")

    # Load config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Execute each pipeline stage
    logger.info("Starting pipeline execution.")
    
    load_stage = LoadDataStage()
    data = load_stage.execute(keyword=keyword)

    transform_stage = TransformStage()
    structured_data = transform_stage.execute(data)

    qa_stage = QATransformStage(qa_model=config['qa_model'])
    result = qa_stage.execute(structured_data, question=question)

    logger.info("Pipeline execution completed.")
    return result

