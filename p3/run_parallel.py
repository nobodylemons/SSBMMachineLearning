'''
Created on Oct 25, 2017

@author: Robert
'''
import os
from subprocess import call

file_loc = os.path.dirname(os.path.realpath(__file__))
i = 0
docker_str = "docker run --rm --volume=\"/Users/Robert/Documents/docker/smashparallel/1:/home/root/SSBMMachineLearning/p3\" -i -t smashbot /bin/bash"
#call docker command
command = []
while os.path.isdir(file_loc+"/"+str(i)):
    volume_string = file_loc+"/"+str(i)+":/home/root/SSBMMachineLearning/p3"
    command.append("docker")
    command.append("run")
    command.append("--rm")
    command.append("-v")
    command.append(volume_string) 
    command.append("-t")
    command.append("smashbot")
    call(command)
    i = i + 1
