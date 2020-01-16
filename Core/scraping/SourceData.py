class SourceInfo:
    def __init__(self, param, ignoreTerm):
        self.param = param
        self.ignoreTerm = ignoreTerm


class SourceData:
    def __init__(self, url: str, name: str, info: SourceInfo = None):
        self.url = url
        self.name = name
        self.info = info
