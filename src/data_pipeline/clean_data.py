import pandas as pd
import re
from src.base import PipelineStage

class TransformStage(PipelineStage):
    def __init__(self):
        super().__init__("TransformStage")

    def execute(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Transform raw Wikipedia data into structured pages and summaries.
        """
        self.logger.info("Starting data transformation.")
        
        raw_text = data['search_result'].iloc[0]
        pattern = r"Page:\s*(.*?)\s+Summary:\s*(.*?)(?=\nPage:|$)"
        matches = re.findall(pattern, raw_text, re.DOTALL)

        records = [{'page': page.strip(), 'Summary': summary.strip()} for page, summary in matches]
        result_df = pd.DataFrame(records)

        self.logger.info(f"Transformed data: {len(result_df)} records found.")
        return result_df
