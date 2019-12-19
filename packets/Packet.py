from abc import ABC, abstractmethod


class Packet(ABC):

    @abstractmethod
    def parse(self):
        pass
