# -*- coding: latin-1 -*-

import re

def extract(id):

    if "F" in id:
        prefix = "F"       
        id = int(id[1:])
    else:
        prefix = ""
        id = int(id)
        
    folder = prefix + str((id / 1000) * 1000)
    fname = prefix + "%(id)04d.html" % {"id": id}

    print folder +"/"+fname
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

    res = {"city": city, "cat": cat, "time": time, "place": place, "cat_place": cat_place, "splits": kmsplits}

    for k,v in res.iteritems():       

        if k != "splits":
            res[k] = str.replace(res[k],"\353", 'e')
            res[k].strip()
    
    return res
    

def process(data):

    splits = []
    for lap in data['splits']:
        if(lap != ""):
            splits.append(to_seconds(lap))
        else:
            splits.append(0)

    switch = {0}
    pos = 0
    for lap in splits:
        if lap == 0:
            if pos == 0:
                splits[pos] / 2
            elif pos == 4:
                #half marathon
                splits[pos] = ((splits[pos-1]-splits[pos-2]) / 5) + splits[pos-1]
            elif pos == 9:
                splits[pos] = 2 * splits[pos-1] - splits[pos-2]
            else:
                splits[pos] = (splits[pos-1]+splits[pos+1]) / 2            
        pos+=1
    

    data['time'] = to_seconds(data['time'])
    data['splits'] = splits
    data['place'] = data['place'].split("/")[0].strip()
    data['cat_place'] = data['cat_place'].split("/")[0].strip()    
    return data

    
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

    f = open("found.txt")
    found = f.read().split(" ")

    f = open('rotmar.csv', 'w')

    csv_header = "city,km5,km10,km15,km20,hm,km25,km30,km35,km40,time,cat,place,cat_place\n"

    f.write(csv_header)
    # return
    for bib in range(1,8500):
        if str(bib) in found: 
            data = extract(str(bib))
            proc_data = process(data)
            rec = csv_record(proc_data)
            f.write(rec+"\n")
        else:
            print str(bib)+" not in "
            print found[1:20]
    
    


if __name__ == "__main__":
    main()
