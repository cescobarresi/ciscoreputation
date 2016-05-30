#! /usr/bin/env python
# encoding: utf-8
# filetype: python
"""
ciscoreputation
Get the email reputation for a hostname or IP address from senderbase.org

Usage:
    ciscoreputation <query> [options]
    ciscoreputation reputation <query> [options]
    ciscoreputation volumes <query> [options]
    ciscoreputation alldata <query> [options]
    ciscoreputation --help

Commands:
    reputation      Get the reputation for the given <query>
    volumes         Get the volume for last month and current day for the given <query>

Arguments:
    query    May be an <query> of domain name.

Options:
    --tos                  Accept SenderBase Term of Service
    --values               Output only the requested value, useful when using in another script
    --version              Print version.
    -h --help              Show this screen.

Note: Cisco requires not to exceed 1000 queries per calendar day per IP or subnet.
"""
from __about__ import __version__
from docopt import docopt

import requests, re
from bs4 import BeautifulSoup

def get_authhash_searchby(search_string):
    """
    Get the authHash code from senderbase, if necessary accept the TOS, and the search_by type.

    :param ip: the ip address
    return: authHash, search_by
    """
    # Get web page
    r = requests.get('http://www.senderbase.org/lookup/?search_string=%s' % search_string)

    if r.status_code != 200:
        return None, r.status_code

    soup = BeautifulSoup(r.text, 'html.parser')

    # Need to accept TOS?
    if soup.find("input", id="tos_accepted", class_="button"):
        tos_accepted = soup.find("input", id="tos_accepted", class_="button").attrs['value']
        r = requests.post('http://www.senderbase.org/' + soup.find_all("form", method="POST")[0].attrs['action'],
                data={'tos_accepted':tos_accepted})

    soup = BeautifulSoup(r.text, 'html.parser')

    # Can't find any result
    if soup.find("div", class_="text_warning", text=re.compile("we can't find any results")):
        return None, "can't find any results for search '%s'" % search_string

    # Get authHash
    auth_hash = soup.find("script", string=re.compile("var authHash"))
    auth_hash = re.search("authHash *= *'([^ ']+)", auth_hash.text).group(1)

    # Get search_by
    search_by = soup.find("script", string=re.compile("loadTabIP\(\)"))
    search_by = re.search("searchBy: '([^ ']+)", search_by.text).group(1)
    return auth_hash, search_by

def get_tabdata(search_string, search_by, auth_hash):
    """
    Download tabbed data from senderbase.org for the given IP

    Return tabbed data text
    """
    # get query type

    r = requests.get('http://www.senderbase.org/lookup/export/',
            params = {
                "search_by":search_by,
                "search_string":search_string,
                "order":'lastmonth desc',
                "fields":'["ip","hostname","lastday","lastmonth","email_score_name"]',
                "export_type":"plaintext_unix",
                "auth":auth_hash})
    if r.status_code != 200:
        return r.status_code

    return r.text

def parse_tabdata(search_string, search_by, data):
    """
    Parse tabbed data from senderbase.org for the given search_string

    return: dict with values.
    """
    # Extract values
    values = []
    for line in data.splitlines():
        if line[0] == "#":
            # skip comments
            continue
        values = line.split("\t")
        # search the line with the requested IP when searching by IP.
        if search_by == 'ip' and values[0].split(" ")[0] == search_string:
            break
        elif search_by != 'ip':
            break

    if len(values) < 5:
        return None

    data = {
        'address':values[0].split(" ")[0],
        'hostname':values[1],
        'lastday_volume':values[2],
        'month_volume':values[3],
        'email_reputation':values[4],
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

    # get authHash and search_by
    auth_hash, search_by = get_authhash_searchby(arguments['<query>'])
    if not auth_hash:
        if arguments['--values']:
            print "unknown"
        else:
            print "Reputation: unknown\n Got status code: %s" % search_by
        raise SystemExit

    if not arguments['--values']:
        print " got authHash:", auth_hash
        print " got search_by:", search_by

    # Get tab separated data
    data = get_tabdata(arguments['<query>'], search_by, auth_hash)
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

    # Output tabbed data as is
    if arguments['alldata']:
        if arguments['--values']:
            data = data.splitlines()
            print "\n".join(data[3:])
        else:
            print data
        raise SystemExit

    # Parse tabbed data
    data = parse_tabdata(arguments['<query>'], search_by, data)

    # Output volumes
    if arguments['volumes']:
        if arguments['--values']:
            print "%s,%s" % (data['month_volume'], data['lastday_volume'])
        else:
            print "senderbase.org data for %s [%s]" % (data['address'], data['hostname'])
            print "Last month volume: %s\nDay volume: %s" % (data['month_volume'], data['lastday_volume'])
    # Output reputation
    elif arguments['reputation']:
        if arguments['--values']:
            print data['email_reputation']
        else:
            print "senderbase.org data for %s [%s]" % (data['address'], data['hostname'])
            print "Email reputation: %s" % data['email_reputation']
    # Ouput all
    else:
        if arguments['--values']:
            print "%s,%s,%s" % (data['email_reputation'],data['month_volume'], data['lastday_volume'])
        else:
            print "senderbase.org data for %s [%s]" % (data['address'], data['hostname'])
            print "Email reputation: %s" % data['email_reputation']
            print "Last month volume: %s\nDay volume: %s" % (data['month_volume'], data['lastday_volume'])


    raise SystemExit

if __name__ == "__main__":
    do_main()
