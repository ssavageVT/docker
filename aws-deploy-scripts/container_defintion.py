import json
from port_mapping import PortMapping
from mount_point import MountPoint,Volume,LogConfiguration
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
        self.dockerLabels = {}
        self.logConfiguration ={}

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

    def add_docker_label(self):
        self.dockerLabels['api-id'] = self.name

    def add_log_configuration(self, log_config, region, group):
        log_info = LogConfiguration(log_config)
        log_info.options['awslogs-region'] = region
        log_info.options['awslogs-group'] = group
        log_info.options['awslogs-stream-prefix'] = self.name
        self.logConfiguration = log_info

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)