#! /bin/env/python3
import json
import requests
import time
import os
import datetime
import sys
from collections import deque

class SlackSink:
    ''' What the class does '''

    debug = False
    if "DEBUG" in os.environ:
        debug = True if os.environ["DEBUG"] in ["true","True","TRUE"] else False

    def __init__(self, influx_host,reasons, 
                    influx_port=8086, 
                    database="k8s", 
                    interval=5,
                    deque_size=20):

        self.url = os.environ["URL"]
        self.path="/query"
        self.influx_url=""
        self.database = database
        self.interval = interval
        self.reasons = reasons
        self.deque_size = deque_size
        self.influx_url="http://" + influx_host + ":" + influx_port + self.path
        self.time_threshold = datetime.datetime.strptime("2017-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

    def catchEvents(self, sentlist, permit_send=False):
        """ catchEvents function retrieves the last X events from influxdb 
            and sends them to slack (only once)

            parameters:
                - object self   : current object
                - deque sentlist: sentlist the lits with the already proccessed events 
                - boolean permit_send  : send to slack or not (used in initialization)
            return: 
                - boolean res    : true if a connection towards db could be established
                - deque sentlist : the list with the already proccessed events 
        """

        # function variables initialization 
        tries = 0
        trying = True
        payload={}
        eventList = []
        formatter_string = "%Y-%m-%dT%H:%M:%SZ"

        # start retrieving data from the database
        while trying:
            try:
                query = "select * from events ORDER BY DESC limit " + str(self.deque_size)

                # create paylod for influx get 
                del payload
                payload={}
                payload.update({"db":self.database})
                payload.update({"q":query})

                if self.debug is True:
                    print("\n%s DEBUG: Hitting '%s' with '%s' (backoff %ds)" % 
                        (datetime.datetime.now(), self.influx_url, query, tries))
                    sys.stdout.flush()

                # make the request towards influxdb    
                res = requests.get(self.influx_url,params=payload)
                trying = False

            except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
                data = {'has_error':True, 'error_message':e.message}
                print(data)
                sys.stdout.flush()
                time.sleep(1)
            finally:
                tries = tries + 1
            
            if (tries == 120):
                # after 2 minutes program ends
                trying = False

        # if last try was unsusccessfull terminate the loop
        if (tries == 60 and res is false):
            if self.debug is True:
                print("%s DEBUG: catchEvents() timer expired"% (datetime.datetime.now()))    
                sys.stdout.flush()
            return False,[]

        # print the http status code returned
        if self.debug is True:
            print("%s DEBUG: Returned with %d (%s)" % (datetime.datetime.now(), res.status_code, res.ok))    
            sys.stdout.flush() 

        if res.status_code == 200:
            try:
                data = res.json()
            except ValueError as e:
                msg = "Cannot read response, %s" %(e.message)
        
            index = 0
            if "series" in  data["results"][0]:
                # at least one event was returned
                for event_raw in reversed(data["results"][0]["series"][0]["values"]):

                    # if event should be sent to slack
                    if event_raw[9] in self.reasons:

                        # check if we have already sent the event
                        # find the date and time from time columnof the event serie
                        datetime_object = datetime.datetime.strptime(event_raw[0], formatter_string)

                        if event_raw[11] not in sentlist: 
                            print("Element %3d" % (index))
                            print("%s DEBUG: sending raw %s)" % (datetime.datetime.now(), event_raw))
                            sys.stdout.flush()

                            # push event to slack
                            if permit_send:
                                self.sendSlack(event_raw)

                            # add the event to the sent list
                            if len(sentlist) == 20:
                                # deque is full, remove items from the begining
                                sentlist.popleft()
                            
                            # add events to send list and event list
                            sentlist.append(event_raw[11])
                        else:
                            if self.debug is True:
                                print("%s DEBUG: %s is already sent to slack)" % (datetime.datetime.now(), event_raw[11]))  
                                sys.stdout.flush()
                    # increment index counter            
                    index=index + 1
                        
            else:
                # no events found
                if self.debug is True:
                    print("%s DEBUG: No events found %s" % (datetime.datetime.now(), data))
                    sys.stdout.flush()

        return True, sentlist
        #'columns': ['time', 'cluster_name', 'component', 'hostname', 'kind', 'message', 'namespace_name', 'object_name', 'pod_id', 'reason', 'type', 'uid'],



    def sendSlack(self, event):
        """what the functions does"""
        
        # Object
        object_type ={}
        object_type.update({"title":"Object"})  
        object_type.update({"value":event[4]})  
        object_type.update({"short":"true"})  
        
        # Message
        message = {}
        message.update({"title":"Message"})  
        message.update({"value":event[5]})  
        message.update({"short":"true"})  

        # Podname
        podname = {}
        podname.update({"title":"Name"})  
        podname.update({"value":event[7]})  
        podname.update({"short":"true"})  

        # Reason
        reason = {}
        reason.update({"title":"Reason"})  
        reason.update({"value":event[9]})  
        reason.update({"short":"true"})  

        # UID
        # uid = {}
        # uid.update({"title":"UID"})  
        # uid.update({"value":event[11]})  
        # uid.update({"short":"true"})  

        # timestamp
        # uid = {}
        # uid.update({"title":"timestamp"})  
        # uid.update({"value": str(datetime.datetime.strptime(event[0], "%Y-%m-%dT%H:%M:%SZ"))})  
        # uid.update({"short":"true"})  
        
        if event[9] in ["Created","CreatedLoadBalancer","Pulled","RegisteredNode", \
                        "Scheduled","SuccessfulCreate","SuccessfulDelete","Started", \
                        "UpdatedLoadBalancer"] :
            color = "good"
            text = "Notification message"
            author_icon = "https://slack-files.com/T849YB57X-F86NPAJUW-d13d263e33"
        elif event[9] in ["killing","Pulling","CreatingLoadBalancer", \
                            "ScalingReplicaSet","LeaderElection"] :
            color = "warning"
            text = "Warning message "
            author_icon = "https://slack-files.com/T849YB57X-F86NHUBRU-7f95f724c9"
        else :
            color = "danger"
            text = "Error message"
            author_icon = "https://slack-files.com/T849YB57X-F85B39W57-ae5e076772"

        fields = [object_type, podname, message, reason]

        attachments_payload = {}
        attachments_payload.update({"color": color})
        attachments_payload.update({"author_name": "k8s Eventer"})
        attachments_payload.update({"author_icon": author_icon})
        attachments_payload.update({"title": "New Event created in k8s cluster"})
        attachments_payload.update({"text": text})
        attachments_payload.update({"fields": fields})

        attachments = [attachments_payload]
        payload = {}
        payload.update({"attachments":attachments})

        r = requests.post(self.url, data=json.dumps(payload))
        return
  
    def startPolling(self):
        """ startpolling function polls database for events and sends them to slack

            parameters:
                - object self   : current object
        """

        # initialization
        sent_list = deque()

        # the first call is used to initialize sent_list . only new events 
        # will be shown to slack. No old events are sent at program start.
        res,sent_list = self.catchEvents(sent_list, False)

        # search for new events and forward them to slack
        while True:
            res,sent_list = self.catchEvents(sent_list, True)
            if res:
                if not sent_list:
                    if self.debug is True:
                        print("%s DEBUG: startPolling() < catchEvents() returned an empty list >" % (datetime.datetime.now()))
                else:
                    if self.debug is True:
                        print("%s DEBUG: startPolling() < events sent %s >" % (datetime.datetime.now(), sent_list))
            else:
                if self.debug is True:
                    print("%s DEBUG: startPolling() < Could not connect to database. timer expired %s >" % (datetime.datetime.now()))
                
                self.sendSlack(["0","1","2","3","Pod","Timeout <Cannot connect to influxdb. Check influxdb and restart pod>","6",os.environ["HOSTNAME"],"8","Unhealthy"])
                break

            # poll after self.interval seconds
            time.sleep(self.interval)