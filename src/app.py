#! /bin/env/python3
import json
import requests
from SlackSink import SlackSink
import os

if __name__ == "__main__":
    # execute only if run as a script
    if "INFLUX_HOST" in os.environ:
        influx_svc = os.environ["INFLUX_HOST"]  
    else:
        influx_svc = "localhost"

    if "INFLUX_PORT" in os.environ:
        influx_port = os.environ["INFLUX_PORT"] 
    else:
        influx_port = "8086"

    if "DEBUG" in os.environ:
        debug = True if os.environ["DEBUG"] in ["true","True","TRUE"] else False

    # event list to monitor
    monitoring_types = []

    # type: killing
    if "KILLING" in os.environ:
        if os.environ["KILLING"] in ["true","True","TRUE"] :
            killing = True  
            monitoring_types.append("killing")
        else :
            killing = False

    # type: Backoff
    if "BACKOFF" in os.environ:
        if os.environ["BACKOFF"] in ["true","True","TRUE"] :
            Backoff = True  
            monitoring_types.append("Backoff")
        else :
            Backoff = False

    # type: Created  
    if "CREATED" in os.environ:
        if os.environ["CREATED"] in ["true","True","TRUE"] :
            Created = True  
            monitoring_types.append("Created")
        else :
            Created = False

    # type: CREATEDLOADBALANCER    
    if "CREATEDLOADBALANCER" in os.environ:
        if os.environ["CREATEDLOADBALANCER"] in ["true","True","TRUE"] :
            CreatedLoadBalancer = True  
            monitoring_types.append("CreatedLoadBalancer")
        else :
            CreatedLoadBalancer = False

    # type: CreatingLoadBalancer 
    if "CREATINGLOADBALANCER" in os.environ: 
        if os.environ["CREATINGLOADBALANCER"] in ["true","True","TRUE"] :
            CreatingLoadBalancer = True  
            monitoring_types.append("CreatingLoadBalancer")
        else :
            CreatingLoadBalancer = False

    # type: Failed   
    if "FAILED" in os.environ:
        if os.environ["FAILED"] in ["true","True","TRUE"] :
            Failed = True  
            monitoring_types.append("Failed")
        else :
            Failed = False
    
    # type: FailedMount
    if "FAILEDMOUNT" in os.environ:
        if os.environ["FAILEDMOUNT"] in ["true","True","TRUE"] :
            FailedMount = True  
            monitoring_types.append("FailedMount")
        else :
            FailedMount = False
    
    # type: FailedSync
    if "FAILEDSYNC" in os.environ:
        if os.environ["FAILEDSYNC"] in ["true","True","TRUE"] :
            FailedSync = True  
            monitoring_types.append("FailedSync")
        else :
            FailedSync = False

    # type: FreeDiskSpaceFailed
    if "FREEDISKSPACEFAILED" in os.environ:
        if os.environ["FREEDISKSPACEFAILED"] in ["true","True","TRUE"] :
            FreeDiskSpaceFailed = True  
            monitoring_types.append("FreeDiskSpaceFailed")
        else :
            FreeDiskSpaceFailed = False
    
    # type: ImageGCFailed
    if "IMAGEGCFAILED" in os.environ:
        if os.environ["IMAGEGCFAILED"] in ["true","True","TRUE"] :
            ImageGCFailed = True  
            monitoring_types.append("ImageGCFailed")
        else :
            ImageGCFailed = False
    
    # type: InspectFailed
    if "INSPECTFAILED" in os.environ:
        if os.environ["INSPECTFAILED"] in ["true","True","TRUE"] :
            InspectFailed = True  
            monitoring_types.append("InspectFailed")
        else :
            InspectFailed = False

    # type: LeaderElection
    if "LEADERELECTION" in os.environ:
        if os.environ["LEADERELECTION"] in ["true","True","TRUE"] :
            LeaderElection = True  
            monitoring_types.append("LeaderElection")
        else :
            LeaderElection = False
    
    # type: Pulled
    if "PULLED" in os.environ:
        if os.environ["PULLED"] in ["true","True","TRUE"] :
            Pulled = True  
            monitoring_types.append("Pulled")
        else :
            Pulled = False
    
    # type: Pulling
    if "PULLING" in os.environ:
        if os.environ["PULLING"] in ["true","True","TRUE"] :
            Pulling = True  
            monitoring_types.append("Pulling")
        else :
            Pulling = False
    
    # type: RegisteredNode
    if "REGISTEREDNODE" in os.environ:
        if os.environ["REGISTEREDNODE"] in ["true","True","TRUE"] :
            RegisteredNode = True  
            monitoring_types.append("RegisteredNode")
        else :
            RegisteredNode = False
    
    # type: ScalingReplicaSet
    if "SCALINGREPLICASET" in os.environ:
        if os.environ["SCALINGREPLICASET"] in ["true","True","TRUE"] :
            ScalingReplicaSet = True  
            monitoring_types.append("ScalingReplicaSet")
        else :
            ScalingReplicaSet = False
    
    # type: Scheduled
    if "SCHEDULED" in os.environ:
        if os.environ["SCHEDULED"] in ["true","True","TRUE"] :
            Scheduled = True  
            monitoring_types.append("Scheduled")
        else :
            Scheduled = False
    
    # type: Started
    if "STARTED" in os.environ:
        if os.environ["STARTED"] in ["true","True","TRUE"] :
            Started = True  
            monitoring_types.append("Started")
        else :
            Started = False
    
    # type: SuccessfulCreate
    if "SUCCESSFULCREATE" in os.environ:
        if os.environ["SUCCESSFULCREATE"] in ["true","True","TRUE"] :
            SuccessfulCreate = True  
            monitoring_types.append("SuccessfulCreate")
        else :
            SuccessfulCreate = False
    
    # type: SuccessfulDelete
    if "SUCCESSFULDELETE" in os.environ:
        if os.environ["SUCCESSFULDELETE"] in ["true","True","TRUE"] :
            SuccessfulDelete = True  
            monitoring_types.append("SuccessfulDelete")
        else :
            SuccessfulDelete = False
    
    # type: Unhealthy
    if "UNHEALTHY" in os.environ:
        if os.environ["UNHEALTHY"] in ["true","True","TRUE"] :
            Unhealthy = True  
            monitoring_types.append("Unhealthy")
        else :
            Unhealthy = False

    # type: UpdatedLoadBalancer
    if "UPDATEDLOADBALANCER" in os.environ:
        if os.environ["UPDATEDLOADBALANCER"] in ["true","True","TRUE"] :
            UpdatedLoadBalancer = True  
            monitoring_types.append("UpdatedLoadBalancer")
        else :
            UpdatedLoadBalancer = False

    if debug is True:
         print("Monitoring types list is %s)" % (monitoring_types))

    app = SlackSink(influx_svc, monitoring_types, influx_port)
    app.startPolling()