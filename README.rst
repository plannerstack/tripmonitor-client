Tripmonitor client
==================

A client for the PlannerStack trip monitoring system.


Setting up a development environment
------------------------------------

Use Virtualenv_ and Pip_ to set up a development environment::

    virtualenv .
    . bin/activate
    pip install -e .


.. _Virtualenv: http://www.virtualenv.org/
.. _Pip: http://www.pip-installer.org/


Using the client
----------------

.. note:: The trip monitoring interface is in development and is subject to change.

The monitoring client has three functions: planning a trip, setting up a monitoring subscription and connecting to the service to receive updates.

Settings are loaded from a configuration file. An example is shown here::

    [default]
    url = http://localhost:8088
    monitor_url = tcp://localhost:8081/monitoring
    username = develop
    password = develop

    [bree]
    url = http://rancingpony.com/monitoring
    monitor_url = tcp://racingpony.com/monitoring
    username = underhill
    password = secret

The default location is ``~/.tripmonitorrc`` but you can change this using the ``-c`` option. The configuration file is divided up into profile sections. The default section is named ``default``. If you have multiple monitoring endpoints you can use the ``-p`` option to select one.

First start the monitoring service::

    tripmonitor-client monitor

In another terminal, plan a trip::

    tripmonitor-client plan FROM TO DATETIME

Example::

    tripmonitor-client plan 52.005173970555695,4.350585937499999 52.15118665954508,5.386047363281249 now

Result in JSON::
    
    {"debug": {"totalTime": 317, "pathCalculationTime": 305, "renderingTime": 2, "timedOut": false, "precalculationTime": 10, "pathTimes": [305]}, "plan": {"date": 1380575422000, "to": {"arrival": null, "name": "Arnhemseweg", "platformCode": null, "stopSequence": null, "lon": 5.385457016403417, "departure": null, "zoneId": null, "stopId": null, "stopCode": null, "lat": 52.15133788184729, "stopIndex": null, "orig": null}, "itineraries": [{"walkTime": 809, "fare": null, "legs": [{"transitLeg": false, "realTime": false, "alightRule": null, "headsign": null, "routeLongName": null, "intermediateStops": null, "duration": 518000, "rentedBike": false, "routeShortName": null, "tripId": null, "agencyUrl": null, "routeColor": null, "alerts": [{"alertDescriptionText": null, "effectiveStartDate": null, "alertUrl": null, "alertHeaderText": {"translations": {"en": "inrijden vanaf Coenderstraat verboden voor auto's"}, "someTranslation": "inrijden vanaf Coenderstraat verboden voor auto's"}}],
    (...)
    area": false, "alerts": null, "lon": 5.386435700000001, "stayOn": false, "absoluteDirection": "SOUTHWEST", "lat": 52.1524665, "exit": null, "bogusName": false, "streetName": "Arnhemseweg"}], "mode": "WALK", "tripBlockId": null, "endTime": 1380581492000, "routeTextColor": null}], "walkDistance": 1002.7951344328909, "tooSloped": false, "walkLimitExceeded": true, "waitingTime": 852, "elevationLost": 0.0, "monitorId": "49e01a65f60676e4f40545d5a3e2879f0de03f43", "elevationGained": 0.0, "startTime": 1380575448000, "transfers": 2, "duration": 6044000, "transitTime": 4383, "endTime": 1380581492000}], "from": {"arrival": null, "name": "Pootstraat", "platformCode": null, "stopSequence": null, "lon": 4.3506851524691585, "departure": null, "zoneId": null, "stopId": null, "stopCode": null, "lat": 52.00509669072431, "stopIndex": null, "orig": null}}, "requestParameters": {"arriveBy": "False", "maxWalkDistance": "750", "date": "2013-09-30", "mode": "TRANSIT,WALK", "showIntermediateStops": "False", "time": "23:10:21.953332", "fromPlace": "52.005173970555695,4.350585937499999", "toPlace": "52.15118665954508,5.386047363281249"}, "error": null}

The ``FROM`` and ``TO`` parameters can be in any form accepted by OpenTripPlanner_. The ``DATETIME`` parameter is optional. It defaults to ``now`` when nothing is specified. If you want to plan on another ``DATETIME``, please use the following format ``YYYYMMDDTHHMM`` (20130930T2100). The output contains a ``monitorId`` parameter that can be used to subscribe to updates for a trip::

    tripmonitor-client subscribe MONITOR_ID

Example::

    tripmonitor-client subscribe 49e01a65f60676e4f40545d5a3e2879f0de03f43

The monitoring service will now receive trip updates. To unsubscribe call::

    tripmonitor-client unsubscribe MONITOR_ID

Example::

    tripmonitor-client unsubscribe 49e01a65f60676e4f40545d5a3e2879f0de03f43

.. _OpenTripPlanner: http://opentripplanner.org/
