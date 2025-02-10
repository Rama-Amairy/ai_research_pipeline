from transformers import pipeline
from src.models.model_base import BaseModelHandler

class QAModelHandler(BaseModelHandler):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model = None

    def load_model(self):
        """Load the Q&A model using the pipeline."""
        self.model = pipeline("question-answering", model=self.model_name)

    def predict(self, context: str, question: str):
        """Run the Q&A prediction on the given context and question."""
        if not context.strip():
            return {"answer": "No context provided.", "score": 0.0}

        result = self.model(question=question, context=context)
        return {
            "answer": result.get("answer", "No answer returned"),
            "score": result.get("score", 0.0)
        }
