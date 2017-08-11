from port_mapping import PortMapping
from container_defnition_environment import Environment
from mount_point import MountPoint,Volume


def parse_port_mappings(port_mappings=str):
    port_maps=[]
    if port_mappings is not None:
        mappings= port_mappings.split("^")
        for mapping in mappings:
            ports = mapping.split("*")
            if len(ports) == 3:
                port_map = PortMapping(int(ports[0]), int(ports[1]),ports[2])
                port_maps.append(port_map)
            elif len(ports) == 3:
                port_map = PortMapping(int(ports[0]), int(ports[1]),"tcp")
                port_maps.append(port_map)
            elif len(ports) == 1:
                port_map = PortMapping(int(ports[0]),int(ports[0]),"tcp")
                port_maps.append(port_map)

    return port_maps


def parse_env_variables(env_variables=str):
    variables=[]
    if env_variables is not None:
        env_vars =  env_variables.split("^")
        for env_var in env_vars:
            env = env_var.split("*")
            if len(env) == 2:
                environment = Environment(env[0],env[1])
                variables.append(environment)

    return variables


def parse_mountings(mounts=str, task_name=str):
    mount_dict = {}
    mount_points = []
    volumes = []
    if mounts is not None:
        mountings = mounts.split("^")
        i=0
        for mounting in mountings:
            mount_info = mounting.split("*")
            i=i+1
            if len(mount_info) == 2:
                mount_point = MountPoint(task_name+str(i),mount_info[0],False)
                mount_points.append(mount_point)
                volume = Volume(task_name+str(i))
                volume.add_source_path(mount_info[1])
                volumes.append(volume)

    mount_dict.__setitem__("mounts",mount_points)
    mount_dict.__setitem__("volumes", volumes)
    return mount_dict
