import json
from port_mapping import PortMapping
from mount_point import MountPoint,Volume
from container_defnition_environment import Environment

class ContainerDefinition:

    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.portMappings = []
        self.mountPoints = []
        self.environment = []
        self.memory = 0
        self.cpu = 0
        self.essential = True

    def add_port_mappings(self, container_port, host_port, protocol):
        port_mapping = PortMapping (container_port, host_port, protocol)
        self.portMappings.append(port_mapping)

    def add_memory(self, memory):
        self.memory = memory

    def add_cpu(self, cpu):
        self.cpu = cpu

    def add_mount_points(self, source_volume, container_path, read_only):
        mount_point = MountPoint(source_volume, container_path, read_only)
        self.mountPoints.append(mount_point)

    def add_environment(self, name, value):
        env = Environment(name, value)
        self.environment.append(env)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)