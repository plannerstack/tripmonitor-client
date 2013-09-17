Tripmonitor client
==================

A client for the PlannerStack trip monitoring system.


Setting up a development environment
------------------------------------

Use Virtualenv_ and Pip_ to set up a development environment::

    virtualenv .
    . bin/activate
    pip install -e .


Using the client
----------------

The monitoring client has three functions: planning a trip, setting up a monitoring subscription and connecting to the service to receive updates.

First start the monitoring service::

    tripmonitor-client -u URL connect

In another terminal, plan a trip::

    tripmonitor-client -u URL plan FROM TO

The ``from`` and ``TO`` parameters can be in any form accepted by OpenTripPlanner_. The output contains a ``monitoring_id`` parameter that can be used to subscribe to updates for a trip::

    tripmonitor-client -u URL subscribe MONITORING_ID

The monitoring service will now receive trip updates. To unsubscribe call::

    tripmonitor-client -u URL unsubscribe MONITORING_ID

.. _OpenTripPlanner: http://opentripplanner.org/
