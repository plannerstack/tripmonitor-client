"""
Client for the PlannerStack trip monitoring system.
"""

import sys
import argparse
import json
import logging

import requests
import websocket


logger = logging.getLogger(__name__)


DEFAULT_URL = 'http://localhost:8081/monitoring'


def plan(options):
    """
    Plan a trip. Currently, only planning with departure time is supported.
    """
    url = options.url + '/plan'
    params = {
        'from': options.from_location,
        'to': options.to_location,
        'time': options.time,
    }
    r = requests.get(url, params)
    r.raise_for_status()
    print r.text


def subscribe(options):
    """
    Subscribe to trip updates.
    """
    url = options.url + '/subscribe/%s' % options.monitoring_id
    r = requests.post(url)
    r.raise_for_status()
    print r.text


def unsubscribe(options):
    """
    Unsubscribe to trip updates.
    """
    url = options.url + '/unsubscribe/%s' % options.monitoring_id
    r = requests.post(url)
    r.raise_for_status()
    print r.text


def monitor(options):
    """
    Connect to the monitoring service and receive trip updates.
    """
    url = options.url + '/monitor'
    if url.startswith('http'):
        url = url.replace('http', 'ws', 1)
    ws = websocket.create_connection(url)
    while True:
        print ws.recv()


def parse_args(args=None):
    parser = argparse.ArgumentParser(
            description='Client for the trip monitoring system')
    parser.add_argument('-u', '--url', metavar='URL', default=DEFAULT_URL,
            help='monitoring URL (default: %s' % DEFAULT_URL)
    parser.add_argument('-d', '--debug', action='store_true',
            help='show debugging output')
    subparsers = parser.add_subparsers(metavar='COMMAND',
            help='monitoring command')

    plan_cmd = subparsers.add_parser('plan',
            description=plan.__doc__,
            help='plan a trip')
    plan_cmd.set_defaults(command_func=plan)
    plan_cmd.add_argument('from_location', metavar='FROM',
            help='the departure location')
    plan_cmd.add_argument('to_location', metavar='TO',
            help='the arrival location')
    plan_cmd.add_argument('time', metavar='TIME', nargs='?',
            help='the departure time (default: now)')

    subscribe_cmd = subparsers.add_parser('subscribe',
            description=subscribe.__doc__,
            help='subscribe to trip updates')
    subscribe_cmd.set_defaults(command_func=subscribe)
    subscribe_cmd.add_argument('monitoring_id', metavar='ID',
            help='the monitoring_id of the trip')

    unsubscribe_cmd = subparsers.add_parser('unsubscribe',
            description=unsubscribe.__doc__,
            help='unsubscribe from trip updates')
    unsubscribe_cmd.set_defaults(command_func=unsubscribe)
    unsubscribe_cmd.add_argument('monitoring_id', metavar='ID',
            help='the monitoring_id of the trip')

    monitor_cmd = subparsers.add_parser('monitor',
            description=monitor.__doc__,
            help='receive trip updates')
    monitor_cmd.set_defaults(command_func=monitor)

    return parser.parse_args(args)


def main():
    options = parse_args()
    logger.setLevel(logging.DEBUG if options.debug else logging.INFO)
    options.command_func(options)


if __name__ == '__main__':
    main()
