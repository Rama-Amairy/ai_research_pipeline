import logging
from src.load_data import LoadDataStage
from src.clean_data import TransformStage
from src.qa_transform import QATransformStage


class Pipeline:
    """
    A simple pipeline that fetches Wikipedia data, transforms it,
    and performs Q&A using one of two models:
      - 'qa'      => QAModelHandler
      - 'deepseek' => DeepSeekModelHandler
    """
    
    def __init__(self, model_name: str, model_type: str, api_key: str = None):
        """
        :param model_name: Name of the model to load (e.g. 'distilbert-base-uncased')
        :param model_type: Either 'qa' or 'deepseek', indicating which model class to use
        :param api_key:    Optional API key if required for your model (e.g. for HF Hub)
        """
        self.logger = logging.getLogger("PipelineLogger")

        # Instantiate the stages in a fixed order
        self.load_data_stage = LoadDataStage()  # No arguments in constructor
        self.transform_stage = TransformStage() # No arguments in constructor
        self.qa_transform_stage = QATransformStage(
            model_name=model_name,
            model_type=model_type,
            api_key=api_key
        )
    

    def run(self, keyword: str, question: str):
        """
        Orchestrate the pipeline:
          1) Load data
          2) Transform data
          3) Perform Q&A
        """
        self.logger.info("---- Pipeline Started ----")

        # 1) Load
        self.logger.info("Running LoadDataStage...")
        data = self.load_data_stage.execute(keyword)

        # 2) Transform
        self.logger.info("Running TransformStage...")
        data = self.transform_stage.execute(data)

        # 3) Q&A
        self.logger.info("Running QATransformStage...")
        data = self.qa_transform_stage.execute(data, question)

        self.logger.info("---- Pipeline Completed ----")
        return data
