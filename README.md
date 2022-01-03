# Add-On for DNS Lookup - Splunk Add-On by Deductiv 

## Enrich your Splunk searches with DNS query results for any record type from any DNS server.   


### Lookups (Fields)
- dnslookup_a (hostname, ip, dns_error)
- dnslookup_mx (hostname, mx, dns_error)
- dnslookup_reverse (hostname, ip, dns_error)
- dnslookup_ptr (Same as _reverse but here for conventions)
- dnslookup_ns (hostname, ns, dns_error)
- dnslookup_aaaa (hostname, aaaa, dns_error)
- dnslookup_txt (hostname, txt, dns_error)
- dnslookup_cname (hostname, cname, dns_error)
- dnslookup_alias (hostname, alias, dns_error)
- dnslookup_soa (hostname, soa, dns_error)
- dnslookup_srv (hostname, srv, dns_error)

See transforms.conf for details.

### Customization  
Users have the ability to customize the lookups to use their own dns server or another request type. Use the examples in default/transforms.conf to create your own version.

