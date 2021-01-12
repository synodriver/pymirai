import abc

from pydantic import BaseModel

from pymirai.binary.jce import JceReader


class IJceStruct(BaseModel, abc.ABC):
    @abc.abstractmethod
    def read_from(self, reader: JceReader):
        raise NotImplementedError
