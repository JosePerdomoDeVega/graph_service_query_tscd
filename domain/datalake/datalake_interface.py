from abc import ABC, abstractmethod
from domain.models.record_models import DataLakeRecord


class DataLakeInterface(ABC):

    @abstractmethod
    def add_record(self, record: DataLakeRecord) -> None:
        """
        Persist a record in the datalake.
        """
        pass

    @abstractmethod
    def get_record(self, key: str) -> DataLakeRecord:
        """
        Get a record from the datalake.
        """
        pass

    @abstractmethod
    def get_prefix(self) -> str:
        """
        Return the storage prefix (e.g. date-based).
        """
        pass
