#!/usr/bin/env python

import sys
import csv
import argparse
import dns.resolver
from dns import reversename

"""

Written by J.R. Murray
Deductiv, Inc.

An adapter that takes CSV as input, performs a lookup to the DNS Python
resolution package, then returns the CSV results for DNS entries.

"""

# STDERR printing for python 3
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def dns_lookup(query, record_type = 'A', server = None):
	try:
		record_type = record_type.upper()
		resolver = dns.resolver.Resolver()
		if record_type.lower() == 'ptr':
			try:
				query = reversename.from_address(query)
			except:
				pass
		if server is not None:
			resolver.nameservers = [server]
		resolver.timeout = 2.5
		resolver.lifetime = 2.5
		answer = resolver.resolve(query, record_type)

		answers = []
		if hasattr(answer, 'rrset'):
			for a in answer.rrset:
				b = a.to_text()
				# Dot record is identical to the query
				if b == ".":
					b = query
				if b[-1] == '.':
					b = b[0:-1]
				answers.append(b)
			return answers
		else:
			return ["Error:NoResults"]
		
	except dns.resolver.NoAnswer: 
		sys.stderr.write("No answer: " + str(query) + "\n")
		return ["Error:NoAnswer"]
	except dns.resolver.NXDOMAIN:
		sys.stderr.write("Does not resolve: " + str(query) + "\n")
		return ["Error:NXDOMAIN"]
	except BaseException as e:
		sys.stderr.write("query=" + str(query) + " error=\"" + str(e) + "\"\n")
		return ["Error:"+str(e)]

def main():
	parser = argparse.ArgumentParser(prog='Add-On for DNS Lookup', description='Query DNS records')
	parser.add_argument('-hostname', type=str, dest='hostname', default='',
						help='Hostname or domain to resolve')
	parser.add_argument('-server', type=str, default=None, dest='server',
						help='Server to query')
	parser.add_argument('-type', type=str, dest='record_type', default='a', 
						help='Specify the DNS record type to resolve (e.g. A, PTR, CNAME, MX, NS)')
	parser.add_argument('field_list', nargs='*', type=str, default=['hostname', 'ip'])
	
	try:
		args = parser.parse_args()
	except:
		exit(1)

	in_field = args.field_list[0]
	out_field = args.field_list[1]
	error_field = "dns_error"

	# Use STDIN if the hostname or IP are not passed via CLI
	if in_field in list(args.__dict__.keys()) and args.__dict__[in_field] != '':
		#eprint('Using CLI data')
		data = [ in_field, 
				  args.hostname]
		r = csv.DictReader(data)
		cli = True
	else:
		infile = sys.stdin
		r = csv.DictReader(infile)
		cli = False

	outfile = sys.stdout

	header = r.fieldnames
	required_fields = [in_field, out_field, error_field]
	for required_field in required_fields:
		if not required_field in header:
			header.append(required_field)
	w = csv.DictWriter(outfile, fieldnames=header)
	w.writeheader()

	for result in r:
		#eprint(result[in_field])
		if in_field in list(result.keys()) and result[in_field] is not None and len(result[in_field])>0:
			# Host was provided, add result
			answers = dns_lookup(result[in_field], record_type=args.record_type, server=args.server)
			
			if cli and len(answers) > 1:
				mv_fields = [out_field, error_field]
				for field in mv_fields:
					result[field] = []
				for answer in answers:
					if answer[0:5] == "Error":
						result[error_field].append(answer[6:])
					else:
						result[out_field].append(answer)

				for field in mv_fields:
					if len(result[field]) == 0:
						result[field] = ""
					elif len(result[field]) == 1:
						result[field] = result[field][0]
					elif len(result[field]) > 1:
						result[field] = ';'.join(result[field])
				w.writerow(result)
			else:
				for answer in answers:
					if answer[0:5] == "Error":
						result[error_field] = answer[6:]
					else:
						result[out_field] = answer
					w.writerow(result)
		else:
			w.writerow(result)

main()
