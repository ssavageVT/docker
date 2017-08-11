import aws_clients
import ecs_utils
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--accesskey')
parser.add_argument('--secret')
parser.add_argument('--region')
parser.add_argument('--cluster')
parser.add_argument('--taskname')
parser.add_argument('--servicename')

my_args = parser.parse_args()

access_key = my_args.accesskey
secret_key = my_args.secret
region = my_args.region

ecs_client = aws_clients.getecsclient(access_key, secret_key, region)
ec2_client = aws_clients.getec2client(access_key, secret_key, region)

ecs_utils.update_ecs_service(ecs_client, my_args.cluster, my_args.servicename, my_args.taskname, 0)

ecs_utils.delete_ecs_service(ecs_client, my_args.cluster, my_args.servicename)

ecs_utils.delete_ecs_task_definition(ecs_client, my_args.taskname)
