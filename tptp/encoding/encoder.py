from ..core import Problem
from .encodingResult import EncodingResult



class Encoder():
    def encode(self, problem:Problem, tempSource:bool=False) -> EncodingResult:
        raise NotImplementedError()