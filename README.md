# DNS High Jack Monitoring

## Overview
Trade craft scripts to aid with detecting DNS high jacking attempts after the disclosures in January 2019

* https://www.us-cert.gov/ncas/alerts/AA19-024A
* https://blog.talosintelligence.com/2018/11/dnspionage-campaign-targets-middle-east.html
* https://www.fireeye.com/blog/threat-research/2019/01/global-dns-hijacking-campaign-dns-record-manipulation-at-scale.html
* https://blog-cert.opmd.fr/dnspionage-focus-on-internal-actions/
* https://www.crowdstrike.com/blog/widespread-dns-hijacking-activity-targets-multiple-sectors/


## The Scripts

### UberRootResolve
This takes the IANA list of TLDs and:
* resolves them for IPv4 and IPv6
* looks up the ASN information for those IPs
* stores the results in two files
** Output-!TLDs.txt - a CSV file with domain and its name servers
** Output-[TLD].txt - a CSV file for the domain with its name servers, their IPv4 and IPv6 addresses and ASNs
* then zips all the findings into a file datetime stamped to allow multiple runs

### UberFindGov
This takes the IANA list of TLDs and:
* looks for those domains which resolve a gov.[TLD]




