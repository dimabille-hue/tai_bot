from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def free(self):
        pass

    @abstractmethod
    def get(self, item_id):
        pass