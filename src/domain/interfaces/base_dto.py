from dataclasses import dataclass
from typing import Generic, TypeVar, Type

ModelType = TypeVar("ModelType")
DTOType = TypeVar("DTOType")


@dataclass
class BaseDTO(Generic[ModelType, DTOType]):
    @classmethod
    def from_model(cls: Type[DTOType], model: ModelType) -> DTOType:
        model_dict = {key: value for key, value in model.__dict__.items() if not key.startswith('_')}
        return cls(**model_dict)

    def to_model(self: DTOType, model_cls: Type[ModelType]) -> ModelType:
        return model_cls(**self.__dict__)
