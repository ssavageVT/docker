class PortMapping:

    def __init__(self, containerPort, hostPort, protocol):
        self.containerPort = containerPort
        self.hostPort = hostPort
        self.protocol = protocol