import json
class MountPoint:
    def __init__(self, sourceVolume, containerPath, readOnly):
        self.sourceVolume = sourceVolume
        self.containerPath = containerPath
        self.readOnly = readOnly


class Volume:
    def __init__(self, name):
        self.name = name
        self.host ={}

    def add_source_path(self, path):
        self.host.__setitem__("sourcePath",path)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)