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
    monitor_url = http://localhost:8081/monitoring
    username = develop
    password = develop

    [bree]
    url = http://rancingpony.com/monitoring
    monitor_url = http://racingpony.com/monitoring
    username = underhill
    password = secret

The default location is ``~/.tripmonitorrc`` but you can change this using the ``-c`` option. The configuration file is divided up into profile sections. The default section is named ``default``. If you have multiple monitoring endpoints you can use the ``-p`` option to select one.

First start the monitoring service::

    tripmonitor-client monitor

In another terminal, plan a trip::

    tripmonitor-client plan FROM TO

The ``FROM`` and ``TO`` parameters can be in any form accepted by OpenTripPlanner_. The output contains a ``monitoring_id`` parameter that can be used to subscribe to updates for a trip::

    tripmonitor-client subscribe MONITORING_ID

The monitoring service will now receive trip updates. To unsubscribe call::

    tripmonitor-client unsubscribe MONITORING_ID

.. _OpenTripPlanner: http://opentripplanner.org/
