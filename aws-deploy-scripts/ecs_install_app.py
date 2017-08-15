import aws_clients
import ecs_utils
import pprint
import json
import argparse
from container_defintion import ContainerDefinition
from ecs_service_loadbalancer import ServiceLoadBalancer
from mount_point import Volume
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--accesskey')
parser.add_argument('--secret')
parser.add_argument('--region')
parser.add_argument('--cluster')
parser.add_argument('--createcluster')
parser.add_argument('--taskname')
parser.add_argument('--servicename')
parser.add_argument('--imageid')
parser.add_argument('--imagename')
parser.add_argument('--createinstance')
parser.add_argument('--instanceimageid')
parser.add_argument('--instancetype')
parser.add_argument('--instancerole')
parser.add_argument('--task')
parser.add_argument('--keyname')
parser.add_argument('--env')
parser.add_argument('--ports')
parser.add_argument('--memory')
parser.add_argument('--cpu')
parser.add_argument('--volumes')
parser.add_argument('--logdriver')
parser.add_argument('--loggroup')

my_args = parser.parse_args()

print(my_args)

ecs_client = aws_clients.getecsclient(my_args.accesskey, my_args.secret, my_args.region)
ec2_client = aws_clients.getec2client(my_args.accesskey, my_args.secret, my_args.region)

c = ContainerDefinition(my_args.imagename, my_args.imageid)
c.add_memory(int(my_args.memory))
c.add_cpu(int(my_args.cpu))
c.portMappings = utils.parse_port_mappings(my_args.ports)
c.environment = utils.parse_env_variables(my_args.env)
c.add_log_configuration(my_args.logdriver, my_args.region, my_args.loggroup)
c.add_docker_label()

vols ={}
vols = utils.parse_mountings(my_args.volumes,my_args.taskname)
c.mountPoints = vols.get("mounts")
volumes =[]
for vol in vols.get("volumes"):
    volumes.append(json.loads(vol.to_json()))

container_def = json.loads(c.toJSON())

response = ecs_utils.create_ecs_task_definition(ecs_client, container_def, my_args.taskname, volumes)

task = response["taskDefinition"]["family"]+":"+str(response["taskDefinition"]["revision"])
pprint.pprint("Created the task definition----")

#loadBalancer = ServiceLoadBalancer(container_name="jhipster_registry",container_port=8761)
#loadBalancer.add_arn("arn:aws:elasticloadbalancing:us-east-1:496675820197:targetgroup/MSLGTG/0a7f7d56d1057989")
#loadBalancer.add_elb_name("mytestelb")
loadbalancers=[]
#loadbalancers.append(json.loads(loadBalancer.to_json()))

pprint.pprint("Creating the services----")
exists = ecs_utils.is_service_active(ecs_client,my_args.cluster,my_args.servicename)
if exists is True:
    ecs_utils.update_ecs_service(ecs_client,my_args.cluster, my_args.servicename, task, 1)
elif exists is False:
    ecs_utils.create_ecs_service(ecs_client, my_args.cluster,my_args.servicename,1,task,my_args.instancerole,loadbalancers)
pprint.pprint("Created the services----")