import boto3
import pprint
import aws_clients
import os

def create_ecs_cluster(ecs_client, cluster_name):
    response = ecs_client.create_cluster(
        clusterName=cluster_name
    )
    pprint.pprint(response)
    return response


def create_ecs_cluster_instances(ec2_client, cluster_name,
                                 image_id, instance_type, instance_role, key_name):
    response = ec2_client.run_instances(
        # Image Id
        ImageId=image_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=key_name,
        IamInstanceProfile={
            "Name": instance_role
        },
        UserData="#!/bin/bash \n echo ECS_CLUSTER=" + cluster_name + " >> /etc/ecs/ecs.config"
    )
    pprint.pprint(response)
    return response


def list_ecs_cluster_instances(ecs_client, cluster_name):
    response = ecs_client.list_container_instances(
        cluster = cluster_name,
        status = 'ACTIVE'
    )
    pprint.pprint("Called the list container instances")
    pprint.pprint(response)
    return response["containerInstanceArns"]


def create_ecs_task_definition(ecs_client, container_def, task_name, volumes):
    response = ecs_client.register_task_definition(
        containerDefinitions=[container_def],
        family=task_name,
        volumes=volumes
    )
    pprint.pprint(response)
    return response


def create_ecs_service(ecs_client, cluster_name, service_name, count, task_name, role, load_balancers):
    response = ecs_client.create_service(
        cluster=cluster_name,
        serviceName=service_name,
        taskDefinition=task_name,
        desiredCount=count,
        clientToken='msecstest1234567',
        #loadBalancers = load_balancers,
        #role = role,
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 50
        }
    )
    pprint.pprint(response)
    return response


def update_ecs_service(ecs_client, cluster_name, service_name, task_definition, count):
    try:
        # Set desired service count to 0 (obligatory to delete)
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service_name,
            desiredCount=count,
            taskDefinition = task_definition
        )
        pprint.pprint(response)
        return response
    except:
        print("Service not found or not active")


def delete_ecs_service(ecs_client, cluster_name, service_name):
    try:
        response= ecs_client.delete_service(
            cluster= cluster_name,
            service= service_name
        )
        pprint.pprint(response)
        return response
    except:
        print("Service not found or nor active")


def delete_ecs_task_definition(ecs_client, task_name):
    response = ecs_client.list_task_definitions(
        familyPrefix=task_name,
        status='ACTIVE'
    )
    pprint.pprint(response)

    # De-Register all task definitions
    for task_definition in response["taskDefinitionArns"]:
        # De-register task definition(s)
        de_register_response = ecs_client.deregister_task_definition(
            taskDefinition=task_definition
        )
        pprint.pprint(de_register_response)


def delete_ecs_container_instances(ecs_client, ec2_client, cluster_name):
    response = ecs_client.list_container_instances(
        cluster=cluster_name
    )
    pprint.pprint(response)
    if response["containerInstanceArns"]:
        container_instance_resp = ecs_client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=response["containerInstanceArns"]
        )
        pprint.pprint(container_instance_resp)

        for ec2_instance in container_instance_resp["containerInstances"]:
            ec2_termination_resp = ec2_client.terminate_instances (
                DryRun=False,
                InstanceIds=[
                    ec2_instance["ec2InstanceId"],
                ]
            )
            pprint.pprint(ec2_termination_resp)


def delete_ecs_cluster(ecs_client, cluster_name):
    response = ecs_client.delete_cluster(
        cluster=cluster_name
    )
    pprint.pprint(response)


def describe_ecs_service(ecs_client, cluster_name, service_name):
    service_names=[]
    service_names.append(service_name)
    response = ecs_client.describe_services(
        cluster=cluster_name,
        services=service_names
    )
    pprint.pprint(response)
    return response


def is_service_active(ecs_client, cluster_name, service_name):
    response = describe_ecs_service(ecs_client,cluster_name, service_name)
    if response is not None:
        if response["services"]:
            services = response["services"]
            if services[0]["status"] == "ACTIVE":
                return True

    return False


def ecs_desciribe_task_definition(ecs_client, task):
    response = ecs_client.describe_task_definition(
        taskDefinition = task
    )
    pprint.pprint(response)


def ecs_describe_tasks(ecs_client, cluster, tasks):
    response = ecs_client.describe_tasks(
        cluster = cluster,
        tasks = tasks
    )

    pprint.pprint(response)
