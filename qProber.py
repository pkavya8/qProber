import urllib2
import base64
import json
import sys
import os
import re

host=""
specT=0.0
cov=0
accountKey=""
v="Root"
coverage={}
spec={}
categories={}
categories['Root']=['Computers', 'Health', 'Sports']
categories['Computers']=['Hardware', 'Programming']
categories['Health']=['Fitness', 'Diseases']
categories['Sports']=['Basketball', 'Soccer']
coverage["Root"]=0
coverage["Health"]=0
coverage["Computers"]=0
coverage["Sports"]=0
coverage["Hardware"]=0
coverage["Programming"]=0
coverage["Diseases"]=0
coverage["Fitness"]=0
coverage["Soccer"]=0
coverage["Basketball"]=0
spec["Root"]=1
spec["Health"]=0
spec["Computers"]=0
spec["Sports"]=0
spec["Hardware"]=0
spec["Programming"]=0
spec["Diseases"]=0
spec["Fitness"]=0
spec["Soccer"]=0
spec["Basketball"]=0
urllist={}
urllist["Root"]=[]
urllist["Computers"]=[]
urllist["Sports"]=[]
urllist["Health"]=[]
docFreq={}

def bing(query,level):
    global urllist
    #print "bing"
    bingUrl = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query=%27site%3a'+host+'%20'+query.replace(' ', '%20')+'%27&$top=4&$format=json'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    result=json.loads(content) 
    for i in result['d']['results'][0]['Web']:
        for level1 in urllist: 
            if i['Url'] not in urllist[level1]:
                z=1
            else:
                z=0
        if z==1:   
            urllist[level].append(i['Url'])
    return result['d']['results'][0]['WebTotal']
    
def contentSummary(v):
    global docFreq
    a=v.split("/")
    if len(a)>1:
        urllist[a[0]]=urllist[a[0]]+urllist[a[1]]
    #print urllist["Root"]
    #print urllist["Sports"]
    for level in a:
        if level not in categories:
            break
        else:
            print "Creating content summary for: "+level
            getDocFreq(level)
            for key in sorted(docFreq):
                fn="/Users/kavyapremkumar/Documents/ADB Project 2/"+level+"-"+host+".txt"
                f1=open(fn,'a+')
                f1.write(key+"#"+str(docFreq[key])+"\n")
                f1.close()
    
       
def getDocFreq(level):
        global docFreq 
        docFreq={}  
        g=0
        print len(urllist[level])
        for url in urllist[level]: 
            print url 
            g=g+1 
            print g
            if url.endswith('.pdf') or url.endswith('.ppt'):
                continue
            else:
                print "Getting page: "+url
                f=os.popen('lynx --dump '+url)   
                l=f.readlines()
                ctnt=''
                for i in range(0,len(l)):
                    a=l[i].strip()
                    #print a
                    x=a.split()
                    if len(x)>=1 and x[0]=="References":
                        break
                    else:
                        ctnt=ctnt+' '+l[i].strip()
                ctnt=re.sub("[^a-zA-Z ]"," ",ctnt).lower()
                for i in ctnt.split():
                    if i not in docFreq:
                        docFreq[i]=1
                    else:
                        docFreq[i]+=1
                
    
def getSpec(level,total):
    #print "getSpec"
    for i in categories[level]:
        spec[i]=spec[level]*(float(coverage[i])/float(total))
    for items in categories[level]:
        print "Specificity for category "+items+ " is", spec[items]
    #print spec
    comparison(level)
  

def getCoverage(filename,level):
    total=0
    #print "getCov"
    with open(filename) as f:
        line=f.readlines()
        for i in range(0,len(line)):
            str1=line[i].split()
            str2=line[i].split()
            str2.pop(0)
            queryWords=" ".join(str2)
            #time.sleep(2)
            webTotal = int(bing(queryWords,level))
            coverage[str1[0]]=coverage[str1[0]]+webTotal
        for i in categories[level]:
            total=total+coverage[i]        
    for items in categories[level]:
        print "Coverage for category "+items+ " is", coverage[items]
    getSpec(level,total)

            
            
  
def main():
    global accountKey,specT,cov,host
    accountKey= sys.argv[1] 
    specT=sys.argv[2]
    cov=sys.argv[3]  
    host=sys.argv[4]      
    print "Classifying..."
    f='/Users/kavyapremkumar/Documents/ADB Project 2/root.txt'
    getCoverage(f,"Root")
    print "Classification: "
    print v
    print "Extracting topic content summaries... "
    contentSummary(v)
    
def comparison(value):
    global v
    c=0
    for i in categories[value]:
       if(float(spec[i]) > float(specT) and float(coverage[i]) > float(cov)):
           v=v+"/"+i
           #print value+" ---> " +i
           c=c+1
           if i in ["Fitness","Hardware","Programming","Diseases","Soccer","Basketball"]:
               if c==len(categories[value]):
                    print "v:"+v
                    return
                    
               else:
                    continue  
           s="/Users/kavyapremkumar/Documents/ADB Project 2/"+i+".txt"
           getCoverage(s,i)
    if c==0:
        print v
        return


main()        
        
            






    
 



