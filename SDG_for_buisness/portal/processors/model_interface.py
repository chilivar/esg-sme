from ..models import *
from abc import ABC, abstractmethod

class ModelInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def post_data(self, data, **kwargs):
        pass