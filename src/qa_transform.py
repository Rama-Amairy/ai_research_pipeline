from transformers import pipeline
import pandas as pd
from src.base import PipelineStage

class QATransformStage(PipelineStage):
    def __init__(self, qa_model: str):
        super().__init__("QATransformStage")
        self.qa_pipeline = pipeline("question-answering", model=qa_model)

    def execute(self, data: pd.DataFrame, question: str, **kwargs) -> pd.DataFrame:
        """
        Perform question-answering using the given question and summaries.
        """
        self.logger.info(f"Starting Q&A with question: {question}")

        answers = []
        confidences = []

        for idx, row in data.iterrows():
            context = row['Summary']
            if not context.strip():
                answers.append("No context provided.")
                confidences.append(0.0)
                continue

            result = self.qa_pipeline(question=question, context=context)
            answers.append(result.get("answer", "No answer returned"))
            confidences.append(result.get("score", 0.0))

        data['answer'] = answers
        data['confidence'] = confidences

        self.logger.info(f"Q&A completed with {len(data)} answers generated.")
        return data
