import pandas as pd
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from src.base import PipelineStage

class LoadDataStage(PipelineStage):
    def __init__(self):
        super().__init__("LoadDataStage")

    def execute(self, keyword: str, **kwargs) -> pd.DataFrame:
        """
        Load data from Wikipedia using the provided keyword.
        """
        self.logger.info(f"Fetching Wikipedia data for keyword: {keyword}")

        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        response = wikipedia.run(keyword)

        df = pd.DataFrame([{
            'keyword': keyword,
            'search_result': response
        }])
        self.logger.info(f"Successfully loaded data for keyword: {keyword}")
        return df
