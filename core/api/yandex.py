import os
import sys
import time
from http import HTTPStatus
from typing import Callable

import colorama
from termcolor import colored

import requests
from requests import Response, HTTPError

from core.api.base import Processor, RETRY_CODES

BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
colorama.init(autoreset=True)


class YaProcessor(Processor):

    def __init__(self):
        self._headers = None
        self._token = "" # TOKEN
        self._endpoint = BASE_URL
        self.retries = 3
        self.path_upload = "/upload"
        self.dict_methods = self.methods()

    @property
    def token(self) -> str:
        return self._token

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value) -> None:
        self._endpoint = value

    @property
    def headers(self) -> dict:
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'OAuth {self.token}',
        }
        self._headers = headers
        return self._headers

    @headers.setter
    def headers(self, value) -> None:
        self._headers = value

    def upload(self, file_obj) -> bool:
        self.file = file_obj
        self._set_upload_endpoint(file_obj)
        return self._upload(file_obj)

    def _set_upload_endpoint(self, file_obj) -> None:
        payload = {
            "path": f"/backup/{file_obj.name}"
        }

        response = self.request("GET", path=self.path_upload, data=payload)
        upload_url = response.json().get("href", None)
        if upload_url is None:
            sys.stdout.write("Upload url does not exist\n")
            sys.exit(1)
        self._endpoint = upload_url

    def _upload(self, file_obj) -> bool:
        result = False
        with open(file_obj.path, 'rb') as f:
            files = {"file": f}
            response = self.request("PUT", data=files)

        if response.status_code == HTTPStatus.CREATED:
            self._endpoint = BASE_URL
            result = True

        return result

    def delete(self, file_obj) -> bool:
        result = False
        payload = {
            'path': f'/backup/{file_obj.name}',
            'permanently': True
        }

        response = self.request('DELETE', data=payload)
        if response.status_code == HTTPStatus.NO_CONTENT:
            result = True

        return result

    def request(self, method: str, path: str = None, data: dict = None) -> Response:
        if path is not None:
            self.endpoint += path

        data_color, endpoint_color, method_color, path_color = self.colored_text(data, method, path)
        print(f'Method: {method_color}, path: {path_color}, data: {data_color}\nendpoint: {endpoint_color}')
        for r in range(self.retries):
            try:
                response = self.dict_methods[method](data)
                response.raise_for_status()
                return response

            except HTTPError as exc:
                code = exc.response.status_code
                if code in RETRY_CODES:
                    time.sleep(2)
                    continue
                elif code == HTTPStatus.CONFLICT:
                    return self.conflict(data)
                raise exc

    def colored_text(self, data: dict | None, method: str, path: str) -> tuple:
        method_color = colored(f'{method}', color="white", on_color="on_magenta", attrs=["blink"])
        path_color = colored(f'{path}', color="cyan")
        data_color = colored(f'{data}', color="cyan")
        endpoint_color = colored(f'{self.endpoint}', color="cyan", )
        return data_color, endpoint_color, method_color, path_color

    def conflict(self, data: dict) -> Response | None:
        """
        Разрешает конфликт, когда такой файл уже существует - сначала удаляет старый, потом загружает новый файл.
        """
        self.endpoint = BASE_URL
        if self.delete(self.file):
            self.endpoint += self.path_upload
            return self._get(data)

    def _get(self, data: dict) -> Response:
        return requests.get(self.endpoint, params=data, headers=self.headers)

    def _put(self, data: dict) -> Response:
        return requests.put(self.endpoint, files=data)

    def _delete(self, data: dict) -> Response:
        return requests.delete(self.endpoint, params=data, headers=self.headers)

    def methods(self) -> dict[str, Callable[[dict], Response]]:
        return {"GET": self._get, "PUT": self._put, "DELETE": self._delete}
