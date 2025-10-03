from abc import ABC, abstractmethod


class Source(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def data_to_prompt(self):
        pass
