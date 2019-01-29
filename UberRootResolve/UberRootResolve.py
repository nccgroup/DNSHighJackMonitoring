#
# Ollie Whitehouse, NCC Group
# 

#
# 0.1 - 23/01/2019 - initial version
# 0.2 - 24/01/2019 - minor bug fixes
# 0.3 - 26/01/2019 - added ASN and various other minor tidying up
# 0.4 - 27/01/2019 - added zipping of results to allow multiruns and other tidying
# 

import dns.resolver  
import ipaddress
import sys
import gzip
import zipfile
import traceback
import datetime
import os
from time import gmtime, strftime

class ASN:
    pass

# generic hello
print("[i] Uber Root Resolver")

# this is from http://data.iana.org/TLD/tlds-alpha-by-domain.txt
fileTLDs = '..\..\myGovs.txt'

# this is from https://iptoasn.com/
filev4ASNS = '..\..\ip2asn-v4.tsv.gz'
filev6ASNS = '..\..\ip2asn-v6.tsv.gz'

# ----------------------------------------------
# configure the resolver
# ----------------------------------------------
resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['8.8.8.8']

# ----------------------------------------------
# IP v4 ASN support
# ----------------------------------------------
print("[i] Loading IPv4 ASN database..")
asnv4List = []
try:
    with gzip.open(filev4ASNS,'rt', encoding="utf8") as fv4ASNS:
        for line in fv4ASNS:
            parts = line.split('\t')
            # print("[d] Line: + " + line)
            # print("[d] First IP Address: " + parts[0])
            # print("[d] Description " + parts[4])

            asn = ASN()
            asn.first_ip = ipaddress.ip_address(parts[0])
            asn.last_ip = ipaddress.ip_address(parts[1])
            asn.number = int(parts[2])
            asn.country = str.strip(parts[3])
            asn.description = str.strip(parts[4])
            asnv4List.append(asn)

            # ** Test case
            #testIP = ipaddress.ip_address("1.0.0.0")            
            #print("[d] Comparing " + str(testIP) + " " + str(asn.first_ip) + " " + str(asn.last_ip))
            #print(asn.first_ip >= testIP)
            #print(asn.last_ip <= testIP)
            #if asn.first_ip <= testIP and asn.last_ip >= testIP:
                #print("we have a match " + str(testIP) + " - " + line)
                #sys.exit()
except:
    print("[!] Fatal - failed to load database")
    raise
    sys.exit()
print("[i] Loaded successfully with a total of " + str(len(asnv4List)) + " items")

# ----------------------------------------------
# IP v6 ASN support
# ----------------------------------------------
print("[i] Loading IPv6 ASN database..")
asnv6List = []
try:
    with gzip.open(filev6ASNS,'rt', encoding="utf8") as fv6ASNS:
        for line in fv6ASNS:
            parts = line.split('\t')
            # print("[d] Line: + " + line)
            # print("[d] First IP Address: " + parts[0])
            # print("[d] Description " + parts[4])

            asn = ASN()
            asn.first_ip = ipaddress.ip_address(parts[0])
            asn.last_ip = ipaddress.ip_address(parts[1])
            asn.number = int(parts[2])
            asn.country = str.strip(parts[3])
            asn.description = str.strip(parts[4])
            asnv6List.append(asn)

except:
    print("[!] Fatal - failed to load database")
    raise
    sys.exit()

print("[i] Loaded successfully with a total of " + str(len(asnv6List)) + " items")

# ** Test case
#print("[t] Searching..")
#testIP = ipaddress.ip_address("1.0.0.0")
#try:
    #if [fndASN for fndASN in asnList if fndASN.first_ip <= testIP and fndASN.last_ip >= testIP]:
    #   print(fndASN.description)
#    my_filter_iter = filter(lambda x: x.first_ip <= testIP and x.last_ip >= testIP , asnList)
#    print(next(my_filter_iter).description)
#except TypeError:
#    pass

#sys.exit()

# ----------------------------------------------
# Now for parsing the TLDs
# ----------------------------------------------
try:
    with open(fileTLDs) as fTLDs:  
        fPar= open("Output-!TLDs.txt","w")
        print("[i] Output-!TLDs.txt opened for writing")

        print("[i] Processing TLDs")

        # interate through each of the domains in TLDs.txt file
        for cnt, line in enumerate(fTLDs):
            
            try:
                print("[i] Processing TLD - " + str.strip(line))
                domain = str.strip(line)

                # look up the name servers for the domain
                answers = resolver.query(domain,'NS')
                myList = ','.join(map(str, answers)) 
            
                #print("[i] " + str.strip(domain)+","+ myList)
                fPar.write(domain+","+ myList + "\n")
            
                # iterate through each of the nameservers getting their IPv4 and IPv6 address
                f= open("Output-"+domain+".txt","w")

                for server in answers:

                    print("[i] Processing Server " + server.target.to_text(True))

                    # ----------------------------------------------
                    # IPv4
                    # ----------------------------------------------
                    try:
                        IPv4Results = list()
                    
                        # Get the A record for the name server
                        answersA = resolver.query(server.target.to_text(True),'A')

                        for AAddress in answersA:
                            try:
                                # Get the ASN information for the IP address of the name server
                                serverIP = ipaddress.ip_address(AAddress)
                            
                                # this is filth
                                my_filter_iter = filter(lambda x: x.first_ip <= serverIP and x.last_ip >= serverIP, asnv4List)
                                asnFound = next(my_filter_iter)
                                if(asnFound.number==0):
                                    asnFound = next(my_filter_iter)
                                #print("[d] Result of filter " + str(asnFound.number) + " - " + asnFound.description)
                            
                                # append to the list
                                IPv4Results.append(AAddress)
                                IPv4Results.append(str(asnFound.number))
                                IPv4Results.append(asnFound.description)
                                IPv4Results.append(asnFound.country)
                            except:
                                traceback.print_exc()
                                IPv4Results.append(AAddress)
                                IPv4Results.append("no_as_numebr")
                                IPv4Results.append("no_as_description")
                                IPv4Results.append("no_as_country_code")
                                pass
                    
                        # Output
                        #myList = ','.join(map(str, answersA)) 
                        myList = ",".join(map(str,IPv4Results))
                        #print(server.target.to_text(True)+","+ myList)
                        f.write(server.target.to_text(True)+","+ myList+"\n")
                    except (KeyboardInterrupt, SystemExit):
                        sys.exit()
                    except:
                        #traceback.print_exc()
                        continue

                    # ----------------------------------------------
                    # IPv6
                    # ----------------------------------------------
                    try:
                        IPv6Results = list()
                        # Get the A record for the name server
                        answersAAAA = resolver.query(server.target.to_text(True),'AAAA')

                        for AAAAAddress in answersAAAA:
                            try:
                                # Get the ASN information for the IP address of the name server
                                serverIP = ipaddress.ip_address(AAAAAddress)
                            
                                # this is filth
                                my_filter_iter = filter(lambda x: x.first_ip <= serverIP and x.last_ip >= serverIP, asnv6List)
                                asnFound = next(my_filter_iter)
                                #print("[d] Result of filter " + str(asnFound.number) + " - " + asnFound.description)
                                if(asnFound.number==0):
                                    asnFound = next(my_filter_iter)
                                #print("[d] Result of filter " + str(asnFound.number) + " - " + asnFound.description)
                            
                                # append to the list
                                IPv6Results.append(AAAAAddress)
                                IPv6Results.append(str(asnFound.number))
                                IPv6Results.append(asnFound.description)
                                IPv6Results.append(asnFound.country)

                            except:
                                #traceback.print_exc()
                                IPv6Results.append(AAAAAddress)
                                IPv6Results.append("no_as_numebr")
                                IPv6Results.append("no_as_description")
                                IPv6Results.append("no_as_country_code")
                                pass
                    
                        # Output
                        #myList = ','.join(map(str, answersA)) 
                        myList = ",".join(map(str,IPv6Results))
                        #print(server.target.to_text(True)+","+ myList)
                        f.write(server.target.to_text(True)+","+ myList+"\n")

                    except (KeyboardInterrupt, SystemExit):
                        sys.exit()
                    except:
                        #traceback.print_exc()
                        continue

                f.close()
            except dns.resolver.NXDOMAIN:
                print("[i] No name servers found for - " + str.strip(line) + " - skipping..")
                continue
        
        fPar.close()

finally:  
    fTLDs.close()

    # 
    # zip the results
    # 
    strNow = strftime("%Y%m%d%H%M%S")
    print("[i] zipping results to " + str(strNow ) + ".zip")

    lstTXTFiles = []
    for file in os.listdir(".\\"):
        if file.endswith(".txt") and file.startswith("Output-"):
            lstTXTFiles.append(os.path.join(".\\", file))

    #with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
    with zipfile.ZipFile(str(strNow )+".zip", 'w', zipfile.ZIP_DEFLATED) as zip:
        for file in lstTXTFiles:
            zip.write(file)