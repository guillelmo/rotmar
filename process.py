# -*- coding: latin-1 -*-

import re
import sys

def extract(id):

    if "F" in id:
        prefix = "F"       
        id = int(id[1:])
    else:
        prefix = ""
        id = int(id)
        
    folder = prefix + str((id / 1000) * 1000)
    fname = prefix + "%(id)04d.html" % {"id": id}

    # print folder +"/"+fname
    # return

    f = open(folder +"/"+fname, 'r')
    text = f.read()
    #print text
    
    city = re.search("<td>City</td><td>(.*?)</td>", text).group(1)
    cat = re.search("<td>Category</td><td>(.*?)</td>", text).group(1)
    time = re.search("<td>Net time</td><td>(.*?)</td>", text).group(1)
    place = re.search("<td>Overall place</td><td>(.*?)</td></tr>",text,re.DOTALL).group(1)
    cat_place = re.search("<td>Category place</td><td>(.*?)</td></tr>",text,re.DOTALL).group(1)
    times = re.search("<img src=\"graph.php.*?&t=(.*?)\">", text).group(1)
    kmsplits = times.split(",")

    if city.find(',') != -1:
        city = "\""+city+"\""

    res = {"city": city, "cat": cat, "time": time, "place": place, "cat_place": cat_place, "splits": kmsplits}

    for k,v in res.iteritems():       

        if k != "splits":
            res[k] = str.replace(res[k],"\353", 'e')
            res[k] = str.replace(res[k],"&#324;", 'n')
            res[k].strip()
    
    return res
    

def process(data):

    data['time'] = to_seconds(data['time'])
    data['splits'] = proc_time_splits(data['splits'])
    data['place'] = data['place'].split("/")[0].strip()
    data['cat_place'] = data['cat_place'].split("/")[0].strip()    
    return data

def verify_time_splits(data_splits):

    last = None

    for split in data_splits:
        if last == None:
            last = split
        else:
            if last > split:
                print "error: $last > $split "
            


def proc_time_splits(data_splits):

    splits = []
    for lap in data_splits:
        if(lap != ""):
            splits.append(to_seconds(lap))
        else:
            splits.append(0)

    pos = 0
    for lap in splits:
        if lap == 0:
            if pos == 0:
                if splits[pos+1]:
                    splits[pos+1] / 2
            elif pos == 4:
                #half marathon
                if splits[pos-1] != 0 and splits[pos-2]!=0:
                    splits[pos] = ((splits[pos-1]-splits[pos-2]) / 5) + splits[pos-1]
            elif pos == 9:
                if splits[pos-1] != 0 and splits[pos-1]!=0:
                    splits[pos] = 2 * splits[pos-1] - splits[pos-2]
            else:
                if splits[pos-1] != 0 and splits[pos+1]!=0:
                    splits[pos] = (splits[pos-1]+splits[pos+1]) / 2            
        pos+=1

    return splits
    
def csv_record(data):

    res = data['city']+","
    
    for i in range(0,10):
        res +=str(data['splits'][i])+","

    res+=data['cat']+","+data['place']+","+data['cat_place']
    
    return res    
        
def to_seconds(str_time):

    size = len(str_time.split(':'))
    import time
    if size == 2:
        t =  time.strptime(str_time, "%M:%S")
    elif size == 3:
        t =  time.strptime(str_time, "%H:%M:%S")
    else:
        print "size" + str(size)
        print str_time

    return t[3]*3600 + t[4]*60 +t[5]
    
def main():

    import getopt
    opts, extraparams = getopt.getopt(sys.argv[1:], "r:a")

    #By default, the output file will be written from scratch
    write_file = "w"
    
    for k,v in opts:
        if k == '-r':
            str_range = str.split(v,",")

            if 'A' <= str_range[0][0].upper() <= 'Z':
                if str_range[0][0] == str_range[1][0]:
                    prefix = str_range[0][0]
                    str_range[0] = str_range[0][1:]
                    str_range[1] = str_range[1][1:]
                else:
                    print "Range incorrectly defined (Prefix)"
                    return
            else:
                prefix = ""
            
            bibs = range(int(str_range[0]), int(str_range[1]))

        elif k == '-a':
            write_file = "a"

    try:
        bibs
    except NameError:
        print "Bib number range not defined."
        return
    # print prefix

    f = open("found.txt")
    found = f.read().split(" ")
    f.close()
    
    f = open('rotmar.csv', write_file)

    csv_header = "city,km5,km10,km15,km20,hm,km25,km30,km35,km40,time,cat,place,cat_place\n"

    if(write_file == 'w'):
        f.write(csv_header)

    count = 0
    incomplete = 0
    
    for bib in bibs:
        if prefix+str(bib) in found:            
            data = extract(prefix+str(bib))
            proc_data = process(data)

            if 0 in data['splits']:
                incomplete += 1
            else:
                verify_time_splits(data['splits'])
                rec = csv_record(proc_data)
                f.write(rec+"\n")
                count+=1

        if count % 100 == 0:
            print str(count)+" bib numbers analyzed"
            
        # else:
        #     print str(bib)+" not in the found"
        #     print found[1:20]
    print "Total: "+str(count)+" bib numbers correctly parsed."
    #print "Incomplete: "+str(incomplete)+" records were found incomplete"
    


if __name__ == "__main__":
    main()
