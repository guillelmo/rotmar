import sys
import urllib2 


class FetchResponse:
    """Wrapper class for the fetch method (not completely equivalent to the GAE response)"""
    content = ''

def fetch(url,deadline,method='get'):
    response = FetchResponse()
    res = urllib2.urlopen(url)

    response.content = res.read()
    response.status_code = res.code
    response.final_url = res.geturl()
    return response

def main():

    # for arg in sys.argv: 
    #     print arg

    import getopt
    opts, extraparams = getopt.getopt(sys.argv[1:], "r:", ["prefix="])
    
    for k,v in opts:
        if k == '-r':
            #print 'range: '+v
            str_range = str.split(v,",")
            bibs = range(int(str_range[0]), int(str_range[1]))            
        elif k=='--prefix':
            prefix = v

    try:
        prefix
    except NameError:
        prefix = ""

    try:
        bibs
    except NameError:
        print "Bib number range not defined."
        return

    print "Fetching bibs from " + prefix + str(bibs[0]) + " to "+ prefix + str(bibs[len(bibs)-1])

    notfound = open('notfound.txt', 'w')
    found = open('found.txt', 'w')
    
    base_url = "http://evenementen.uitslagen.nl/2012/marathonrotterdam/details.php"
    parameters = { "s":"1", "o": "1", "t": "en"}

    for s in bibs:
        parameters['s'] = prefix + str(s)
        params  = ""

        # print '%(dir)s/%(prefix)s%(bib)04d.html' % {'bib': s,'dir': prefix+ str((s / 1000) * 1000), "prefix": prefix}
        # return

        for k,v in parameters.iteritems():
            if params == '':
                params += "?"+k+"="+v
            else:
                params += "&"+k+"="+v
                
        response = fetch(base_url+params,0)
        if "Not found" in response.content:
            notfound.write(' '+prefix+str(s))
        elif "Net split times" in response.content:
            found.write(' '+prefix+str(s))
            
            f = open('%(dir)s/%(prefix)s%(bib)04d.html' % {'bib': s,'dir': prefix+ str((s / 1000) * 1000), "prefix": prefix}, 'w')
            f.write(response.content)
        else:
            print "Error: not found "+str(parameters['s'])            
            notfound.write(' '+str(parameters['s']))


    notfound.close()
    found.close()

            



if __name__ == "__main__":
    main()


