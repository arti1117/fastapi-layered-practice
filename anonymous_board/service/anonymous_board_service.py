from abc import ABC, abstractmethod


class AnonymousBoardService(ABC):

    @abstractmethod
    def create(self, title: str, content: str):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def read(self, board_id: str):
        pass