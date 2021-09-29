# Add-On for DNS Lookup - Splunk Add-On by Deductiv 

## Enrich your Splunk searches with DNS query results for any record type from any DNS server.   


### Lookups  
- dnslookup
- dnslookup_mx
- dnslookup_reverse
- dnslookup_ptr (Same as _reverse but here for conventions)
- dnslookup_ns
- dnslookup_aaaa
- dnslookup_txt
- dnslookup_cname
- dnslookup_alias
- dnslookup_soa
- dnslookup_srv

See transforms.conf for details.

### Customization  
Users have the ability to customize the lookups to use their own dns server or another request type. Use the examples in default/transforms.conf to create your own version.

