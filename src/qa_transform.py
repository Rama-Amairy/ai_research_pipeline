import pandas as pd
from src.base import PipelineStage
from src.models.huggingFace import QAModelHandler
from src.models.deepseek_model import DeepSeekModelHandler

class QATransformStage(PipelineStage):
    def __init__(self, model_name: str, model_type: str, api_key: str = None):
        super().__init__("QATransformStage")
        
        # Dynamically load the right model handler
        if model_type == "qa":
            self.model_handler = QAModelHandler(model_name)
        elif model_type == "deepseek":
            self.model_handler = DeepSeekModelHandler(model_name, api_key)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        self.model_handler.load_model()

    def execute(self, data: pd.DataFrame, question: str, **kwargs) -> pd.DataFrame:
        """
        Perform question-answering using the given question and summaries.
        """
        self.logger.info(f"Starting Q&A with question: {question}")

        answers = []
        confidences = []

        for idx, row in data.iterrows():
            context = row['Summary']
            result = self.model_handler.predict(context, question)
            answers.append(result["answer"])
            confidences.append(result["score"])

        data['answer'] = answers
        data['confidence'] = confidences

        self.logger.info(f"Q&A completed with {len(data)} answers generated.")
        return data
