"""
Client for the PlannerStack trip monitoring system.
"""

from __future__ import print_function

import argparse
from base64 import b64encode
from ConfigParser import ConfigParser, NoSectionError
import json
import simplejson
import logging
import os
import sys
import zmq
from dateutil.parser import parse
from datetime import datetime

import requests

logger = logging.getLogger(__name__)


DEFAULT_PROFILE = 'default'
DEFAULT_CONFIG = '~/.tripmonitorrc'
DEFAULT_URL = 'http://localhost:8099'
DEFAULT_MONITOR_URL = "tcp://localhost:8098"

def plan(options, config):
    """
    Plan a trip. Currently, only planning with departure time is supported.
    """
    if options.time is None or options.time == 'now':
        dt = datetime.now()
    else:
        dt = parse(options.time)
    url = config['url'] + '/plan'
    params = {
        'fromPlace': options.from_location,
        'toPlace': options.to_location,
        'time': str(dt.time()),
        'date': str(dt.date()),
        'arriveBy': False,
        'showIntermediateStops': False,
        'maxWalkDistance': 750,
        'mode': 'TRANSIT,WALK',
    }
    r = requests.get(url, params=params,
            auth=(config['username'], config['password']))
    r.raise_for_status()
    result = r.json()
    print_result(result)

def print_result(result):
    print (result)
    if result['plan'] is None:
        print('\nSomething went wrong while planning this trip\n')
        return
    print('\nTrip from %s to %s\nMonitorId - %s' % ( \
            str(result['plan']['from']['name']), \
            str(result['plan']['to']['name']), \
            str(result['plan']['itineraries'][0]['monitorId']) \
        ) \
    )
    print('\n\t\t\tLegs:')
    for leg in result['plan']['itineraries'][0]['legs']:
        print('%s:\n\tFrom %s @ %s (delayed - %s)\n\tTo %s @ %s (delayed - %s)' % ( \
                str(leg['mode']), \
                str(leg['from']['name']), \
                str(ts2datetime(leg['from']['departure'])), \
                str(leg['departureDelay']), \
                str(leg['to']['name']), \
                str(ts2datetime(leg['to']['arrival'])), \
                str(leg['arrivalDelay']) \
            )
        )
    print('\n')


def ts2datetime(ts):
    return datetime.fromtimestamp(ts/1000)


def subscribe(options, config):
    """
    Subscribe to trip updates.
    """
    url = config['url'] + '/subscribe/%s' % options.monitoring_id
    r = requests.post(url, auth=(config['username'], config['password']))
    r.raise_for_status()
    print(r.text)


def unsubscribe(options, config):
    """
    Unsubscribe to trip updates.
    """
    url = config['url'] + '/unsubscribe/%s' % options.monitoring_id
    r = requests.post(url, auth=(config['username'], config['password']))
    r.raise_for_status()
    print(r.text)


def monitor(options, config):
    """
    Connect to the monitoring service and receive trip updates.
    """
    context = zmq.Context()
    notifications_zmq = context.socket(zmq.SUB)
    notifications_zmq.connect(config['monitor_url'])
    notifications_zmq.setsockopt(zmq.SUBSCRIBE, '')
    while True:
        notification = notifications_zmq.recv()
        print(notification)
        notification = simplejson.loads(notification)
        print_result(notification)

def parse_args(args=None):
    parser = argparse.ArgumentParser(
            description='Client for the trip monitoring system')
    parser.epilog ="Use %s COMMAND -h to show command help." % parser.prog

    parser.add_argument('-p', '--profile', metavar='PROFILE',
            default=DEFAULT_PROFILE,
            help='the configuration section (default: %s)' % DEFAULT_PROFILE)
    parser.add_argument('-c', '--config', metavar='CONFIG',
            help='the configuration file (default: %s)' % DEFAULT_CONFIG)
    parser.add_argument('-q', '--quiet', action='store_true',
            help='hide informational output')
    parser.add_argument('-d', '--debug', action='store_true',
            help='show debugging output; overrides --quiet')

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
            help='the departure time (example format: YYYYMMDDTHHMMSS; default: now)')

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

    options = parser.parse_args(args)
    if options.config is None:
        options.config = os.path.expanduser(DEFAULT_CONFIG)
    return options

def get_config(options):
    defaults = {'url': DEFAULT_URL, 'monitor_url': DEFAULT_MONITOR_URL}
    config = ConfigParser(defaults)
    config.read(options.config)
    try:
        options = config.items(options.profile)
    except NoSectionError:
        if not os.path.exists(options.config):
            fail("Configuration file does not exist: %s" % options.config)
        sections = "\n  ".join(config.sections())
        if sections:
            profiles = "Available profiles:\n  %s" % sections
        else:
            profiles = "No profiles found"
        fail("Configuration file '%s' contains no profile section '%s'\n%s" %
                (options.config, options.profile, profiles))
    return dict(options)


def setup_logging(args):
    if args.debug:
        log_level = logging.DEBUG
        httplib.HTTPConnection.debuglevel = 1
    elif args.quiet:
        log_level = logging.WARN
    else:
        log_level = logging.INFO

    logging.basicConfig(format='%(message)s', level=log_level)

    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.WARN)
    requests_log.propagate = True


def fail(message):
        print(message, end='\n', file=sys.stderr)
        sys.exit(1)


def main():
    options = parse_args()
    setup_logging(options)
    config = get_config(options)
    options.command_func(options, config)


if __name__ == '__main__':
    main()
