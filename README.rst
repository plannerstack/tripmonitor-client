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
    
The updates are sent in the same format as the planning results::
  
    An example JSON can be found in the file response_example.json.

In another terminal, plan a trip::

    tripmonitor-client plan FROM TO DATETIME

Example::

    tripmonitor-client plan 52.005173970555695,4.350585937499999 52.15118665954508,5.386047363281249 now

Result in JSON::
    
    An example JSON can be found in the file response_example.json.
    
The ``FROM`` and ``TO`` parameters can be in any form accepted by OpenTripPlanner_. The ``DATETIME`` parameter is optional. It defaults to ``now`` when nothing is specified. If you want to plan on another ``DATETIME``, please use the following format ``YYYYMMDDTHHMM`` (20130930T2100). The output contains a ``monitorId`` parameter that can be used to subscribe to updates for a trip::

    tripmonitor-client subscribe MONITOR_ID

Example::

    tripmonitor-client subscribe 49e01a65f60676e4f40545d5a3e2879f0de03f43

The monitoring service will now receive trip updates. To unsubscribe call::

    tripmonitor-client unsubscribe MONITOR_ID

Example::

    tripmonitor-client unsubscribe 49e01a65f60676e4f40545d5a3e2879f0de03f43

.. _OpenTripPlanner: http://opentripplanner.org/
