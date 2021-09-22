#!/usr/bin/env python

import csv
import sys
import threading
import dns.resolver
from dns import reversename

""" 

Written by J.R. Murray
Deductiv, Inc.

An adapter that takes CSV as input, performs a lookup to the DNS Python
resolution package, then returns the CSV results for DNS entries.

"""

def mxlookup(hostname):
    try:
	resolver = dns.resolver.Resolver()
	resolver.timeout = 2.5
	resolver.lifetime = 2.5
        answer = resolver.query(hostname, 'MX')

        # Define a new array
        answers = []

        # Get the preferred host
        #for rdata in answer:
        #    print 'Host ', rdata.exchange, 'has preference', rdata.preference
        
        # Parse the results
        if hasattr(answer, 'rrset'):
            for a in answer.rrset:
                #print a
                record_text = str(a)[3:-1]
                answers.append(record_text)
            return answers
        else:
            sys.stderr.write("No results in answer: " + hostname + "\n")
    except dns.resolver.NoAnswer: 
        sys.stderr.write("No answer: " + hostname + "\n")
        return []
    except dns.resolver.NXDOMAIN:
        sys.stderr.write("Does not resolve: " + hostname + "\n")
        return []
    except BaseException, e:
	sys.stderr.write("hostname=" + hostname + " error=\"" + str(e) + "\"\n")
        return []


class parser(threading.Thread):
    output_lock = threading.Lock()

    def __init__ (self, data_input):
        threading.Thread.__init__(self)
        self.data_input = data_input

    def run(self):
        for elem in self.data_input:
            #time.sleep(1)
            with self.output_lock:
                print elem + 'Finished'


def main():
    if len(sys.argv) != 3:
        print "Args: " + str(len(sys.argv))
        print "Usage: python external_lookup_mx.py [input field] [output field]"
        sys.exit(1)

    hostfield = sys.argv[1]
    ipfield = sys.argv[2]

    infile = sys.stdin
    outfile = sys.stdout

    r = csv.DictReader(infile)
    header = r.fieldnames

    w = csv.DictWriter(outfile, fieldnames=r.fieldnames)
    w.writeheader()

    for result in r:
        if result[hostfield]:
            # Host was provided, add result
            ips = mxlookup(result[hostfield])
            for ip in ips:
                result[ipfield] = ip
                w.writerow(result)
main()
