from .endpoint import Endpoint


class Model:
    def __init__(
            self, name: str, endpoint: Endpoint, input_size: int, output_size: int, time: float, ignore: bool = False
    ):
        self._name = name
        self._endpoint = endpoint
        self._input_size = input_size
        self._output_size = output_size
        self._time = time
        self._ignore = ignore

    @property
    def name(self) -> str:
        return self._name

    @property
    def endpoint(self) -> Endpoint:
        return self._endpoint

    @property
    def input_size(self) -> int:
        return self._input_size

    @property
    def output_size(self) -> int:
        return self._output_size

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, value: float) -> None:
        self._time = value

    @property
    def ignore(self) -> bool:
        return self._ignore

    @ignore.setter
    def ignore(self, value: bool) -> None:
        self._ignore = value

    def serialize(self) -> dict:
        return {
            'name': self._name,
            'endpoint': self._endpoint.serialize(),
            'input_size': self._input_size,
            'output_size': self._output_size,
            'time': self._time,
            'ignore': self._ignore
        }

    def __repr__(self):
        return (
            f'Model('
            f'name={self.name!r}, '
            f'endpoint={self.endpoint!r}, '
            f'input_size={self.input_size!r}, '
            f'output_size={self.output_size!r}, '
            f'time={self.time!r}, '
            f'ignore={self.ignore!r}'
            f')'
        )
