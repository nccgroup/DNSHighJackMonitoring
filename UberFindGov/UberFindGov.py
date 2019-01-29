#
# Ollie Whitehouse, NCC Group
# 

#
# 0.4 - 27/01/2019 - initial version
# 

import dns.resolver  


# generic hello
print("[i] Uber Find Gov")

# this is from http://data.iana.org/TLD/tlds-alpha-by-domain.txt
fileTLDs = '..\..\TLDs.txt'


# ----------------------------------------------
# configure the resolver
# ----------------------------------------------
resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['8.8.8.8']

# ----------------------------------------------
# Now find us those gov domains
# ----------------------------------------------
try:
    with open(fileTLDs) as fTLDs:  
        fPar= open("Output-!DomainsWithNS.txt","w")
        print("[i] Output-!DomainsWithNS.txt opened for writing")

        print("[i] Processing TLDs")

        # interate through each of the domains in TLDs.txt file
        for cnt, line in enumerate(fTLDs):

            try:
                print("[i] Processing TLD - " + str.strip(line))

                # here is where you add the prefix you care about
                domain = "gov." + str.strip(line)

                # look up the name servers for the domain
                answers = resolver.query(domain,'NS')
                myList = ','.join(map(str, answers)) 
            
                print("[i] " + str.strip(domain)+","+ myList)
                fPar.write(domain+"\n")

            except dns.resolver.NXDOMAIN:
                print("[i] No domain - " + domain + " - skipping..")
                continue
            except dns.resolver.NoNameservers:
                print("[i] No name servers found for - " + domain + " - skipping..")
                continue
            except dns.exception.Timeout:
                print("[i] Timeout for - " + domain + " - skipping..")
                continue
            except dns.resolver.NoAnswer:
                print("[i] No answer for - " + domain + " - skipping..")
                continue

        fPar.close()

finally:  
    fTLDs.close()



