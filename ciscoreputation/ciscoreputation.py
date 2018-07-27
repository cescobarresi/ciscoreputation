#! /usr/bin/env python
# encoding: utf-8
# filetype: python
"""
ciscoreputation
Get the email reputation for an IP address from talosintelligence.com

Usage:
    ciscoreputation <query> [options]
    ciscoreputation reputation <query> [options]
    ciscoreputation volumes <query> [options]
    ciscoreputation --help

Commands:
    reputation      Get the reputation for the given <query>
    volumes         Get the volume for last month and current day for the given <query>

Arguments:
    query           The ip address to query for.

Options:
    --tos                  Accept TalosIntelligence Term of Service
    --values               Output only the requested value, useful when using in another script
    --version              Print version.
    -h --help              Show this screen.

Note: Use wisely, don't query like crazy.
"""
from __about__ import __version__
from docopt import docopt
import requests, re, socket

def get_data(search_string, search_by='ip'):
    """
    Download data from talosintelligence.com for the given IP

    Return tabbed data text
    """
    r_details = requests.get('https://talosintelligence.com/sb_api/query_lookup',
            headers={'referer':'https://talosintelligence.com/reputation_center/lookup?search=%s'%search_string},
            params = {
                'query':'/api/v2/details/ip/',
                'query_entry':search_string
                }).json()

    r_wscore = requests.get('https://talosintelligence.com/sb_api/remote_lookup',
            headers={'referer':'https://talosintelligence.com/reputation_center/lookup?search=%s'%search_string},
            params = {'hostname':'SDS', 'query_string':'/score/wbrs/json?url=%s' % search_string}).json()

    r_talos_blacklist = requests.get('https://www.talosintelligence.com/sb_api/blacklist_lookup',
            headers={'referer':'https://talosintelligence.com/reputation_center/lookup?search=%s'%search_string},
            params = {'query_type':'ipaddr', 'query_entry':search_string}).json()

    # would be nice to plot this values
    #r_volume = requests.get('https://talosintelligence.com/sb_api/query_lookup',
    #        params = {
    #            'query':'/api/v2/volume/ip/',
    #            'query_entry':search_string
    #            }).json()

    # No used for now
    #r_related_ips = requests.get('https://talosintelligence.com/sb_api/query_lookup',
    #        params = {
    #            'query':'/api/v2/related_ips/ip/',
    #            'query_entry':search_string
    #            }).json()

    
    talos_blacklisted = {'status':False}
    if 'classifications' in r_talos_blacklist['entry']:
        talos_blacklisted['status'] = True
        talos_blacklisted['classifications'] = ", ".join(r_talos_blacklist['entry']['classifications'])
        talos_blacklisted['first_seen'] = r_talos_blacklist['entry']['first_seen'] + "UTC"
        talos_blacklisted['expiration'] = r_talos_blacklist['entry']['expiration'] + "UTC"

    data = {
        'address':search_string,
        'hostname':r_details['hostname'] if 'hostname' in r_details else "nodata",
        'volume_change':r_details['daychange'] if 'daychange' in r_details else "nodata",
        'lastday_volume':r_details['daily_mag'] if 'daily_mag' in r_details else "nodata",
        'month_volume':r_details['monthly_mag'] if 'monthly_mag' in r_details else "nodata",
        'email_reputation':r_details['email_score_name'] if 'email_score_name' in r_details else "nodata",
        'web_reputation':r_details['web_score_name'] if 'web_score_name' in r_details else "nodata",
        'weighted_reputation_score':r_wscore['response'],
        'talos_blacklisted':"Yes" if talos_blacklisted['status'] else "No"
        #'weighted_reputation_score':r_wscore[0]['response']['wbrs']['score'],
        #'volumes':zip(*r_volume['data'])
    }

    return data

def do_main():
    # Parse arguments from user
    arguments = docopt(__doc__, version=__version__)

    if not arguments['--values']:
        print "ciscoreputation %s" % __version__

    # Agree terms of use
    if not arguments['--tos']:
        print "Must explicitly accept Term of Use setting option '--tos'"
        raise SystemExit(-1)

    try:
        socket.inet_aton(arguments['<query>'])
    except socket.error:
        print "Error: <query> must be a valid IP address. Found: %s" % arguments['<query>']
        raise SystemExit(-1)

    # Get data
    data = get_data(arguments['<query>'])
    if not data:
        if arguments['--values']:
            print "unknown"
        else:
            print "Reputation: unknown"
        raise SystemExit
    elif isinstance(data, int):
        if arguments['--values']:
            print "unknown"
        else:
            print "Reputation: unknown\n Got status code: %s" % data
        raise SystemExit

    # Output volumes
    if arguments['volumes']:
        if arguments['--values']:
            print "%s,%s" % (data['month_volume'], data['lastday_volume'])
        else:
            print "talosintelligence.com data for %s [%s]" % (data['address'], data['hostname'])
            print "Last month volume: %s\nDay volume: %s" % (data['month_volume'], data['lastday_volume'])
    # Output reputation
    elif arguments['reputation']:
        if arguments['--values']:
            print "%s,%s" % (data['email_reputation'], data['web_reputation'])
        else:
            print "talosintelligence.com data for %s [%s]" % (data['address'], data['hostname'])
            print "Email reputation: %s" % data['email_reputation']
            print "Web reputation: %s" % data['web_reputation']
    # Ouput all
    else:
        if arguments['--values']:
            print "%s,%s,%s,%s,%s,%s" % (
                    data['email_reputation'],
                    data['web_reputation'],
                    data['weighted_reputation_score'],
                    data['month_volume'],
                    data['lastday_volume'],
                    data['talos_blacklisted'])
        else:
            print "talosintelligence.com data for %s [%s] " % (data['address'], data['hostname'])
            print "Email reputation: %s" % data['email_reputation']
            print "Email score: %s" % data['weighted_reputation_score']
            print "Web reputation: %s" % data['web_reputation']
            print "Last month volume: %s\nDay volume: %s" % (data['month_volume'], data['lastday_volume'])
            print "Talos Security Intelligence Blacklist: %s" % data['talos_blacklisted']


    raise SystemExit

if __name__ == "__main__":
    do_main()
