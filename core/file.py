
from core.api.base import Processor


class FileObj:

    def __init__(self, path: str, processor: Processor):
        self.path = path
        self._processor = processor
        self.name = None
        self.set_name()

    def __call__(self, *args, **kwargs) -> str | None:
        result = None
        if kwargs.get("action", None) is not None:
            action = kwargs.get("action")
            result = self.action[action]()
        return result

    @property
    def processor(self) -> Processor:
        return self._processor

    @processor.setter
    def processor(self, value: Processor):
        self._processor = value

    def upload(self) -> str:
        tmp = "File {}: is {}.\n"
        result = self.processor.upload(self)
        tmp = tmp.format(self.name, "created") if result else tmp.format(self.name, "not created")
        return tmp

    def delete(self) -> str:
        tmp = "File {}: is {}.\n"
        result = self.processor.delete(self)
        tmp = tmp.format(self.name, "deleted") if result else tmp.format(self.name, "not deleted")
        return tmp

    def set_name(self) -> None:
        _name = self.path.split("/")
        self.name = _name[-1] if len(_name) > 1 else _name[0]

    @property
    def action(self) -> dict:
        return {"upload": self.upload, "delete": self.delete}
