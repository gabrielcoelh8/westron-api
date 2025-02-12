class Endpoint:
    def __init__(self, url: str, key: str):
        self._url = url
        self._key = key

    @property
    def url(self) -> str:
        return self._url

    @property
    def key(self) -> str:
        return self._key

    def serialize(self) -> dict:
        return {
            'url': self._url,
            'key': '***'
        }

    def __repr__(self):
        return (
            f'Endpoint('
            f'url={self.url!r}, '
            f'key={self.key!r}'
            f')'
        )
