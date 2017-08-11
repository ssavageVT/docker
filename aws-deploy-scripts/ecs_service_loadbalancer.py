import json


class ServiceLoadBalancer:
    def __init__(self, container_name, container_port):
        self.loadBalancerName = ""
        self.targetGroupArn = ""
        self.containerName = container_name
        self.containerPort = container_port

    def add_arn(self,arn):
        self.targetGroupArn = arn

    def add_elb_name(self, elb_name):
        self.loadBalancerName = elb_name

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)