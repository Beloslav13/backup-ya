from abc import ABC, abstractmethod
from http import HTTPStatus

from requests import Response


RETRY_CODES = [
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
]


class Processor(ABC):

    @abstractmethod
    def upload(self, file_obj) -> bool:
        pass

    @abstractmethod
    def delete(self, file_obj) -> bool:
        pass

    @abstractmethod
    def request(self, *args, **kwargs) -> Response:
        pass
