import json
import aws_clients
import ecs_utils
from container_defintion import ContainerDefinition
from ecs_service_loadbalancer import ServiceLoadBalancer

c = ContainerDefinition("myorg_Hello_World", 'HelloWorld')
c.add_memory(100)
c.add_cpu(200)
c.add_port_mappings("10", "10", "tcp")
c.add_port_mappings("20", "20", "HTTP")

c.add_environment("User", "john doe")
c.add_environment("password", "test")
c.add_docker_label()
c.add_log_configuration("awslogs")

c.add_mount_points("my_vol", "/test/dir1", False)
c.add_mount_points("my_vol1", "/test/dir2", True)
container_def = json.loads(c.toJSON())


print(c.toJSON())
container_def['hostname'] = "localhost"
print(container_def)

loadBalancer = ServiceLoadBalancer(container_name="mycontainer",container_port=8080)
loadBalancer.add_elb_name("myelb")
print(loadBalancer.to_json())
