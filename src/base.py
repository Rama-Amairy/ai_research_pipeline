import logging
from abc import ABC, abstractmethod

class PipelineStage(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)

    @abstractmethod
    def execute(self, data=None, **kwargs):
        """
        Abstract method for pipeline stages.
        
        """
        pass
