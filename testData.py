#Author : Kunchala Anil, Tanniru Surendra
#Email : anilkunchalaece
#date : Aug 27 2016
#import csv
import urllib2, urllib #used tos end post Request
import re #used to parse the Received Data

class TestData(object):
    def __init__(self):
        #f = open('anatomy_questions.csv','rt')
        #reader = csv.reader(f)
        self.keys = []
        self.queDict = {}
        self.optADict = {}
        self.optBDict = {}
        self.optCDict = {}
        self.optDDict = {}
        self.keyDict = {}
        self.key = 1;
                
        self.mydata=[('ID',102),('two',2)]    #The first is the var name the second is the value
        self.mydata=urllib.urlencode(self.mydata)
        self.path='http://www.newpythonscripts.16mb.com/new5.php'    #the url you want to POST to
        self.req=urllib2.Request(self.path, self.mydata)
        self.req.add_header("Content-type", "application/x-www-form-urlencoded")
        self.page=urllib2.urlopen(self.req).read()

        """
The Received Data is in the Form
<q> Uid||Question1||optA||optB||optC||optD <\q><q>Uid2||Question2||optA||optB||optC||optD<\q> .. and so on

First get the List of Question&Options
Then Cut the String in the list into Uid,Question,optA,optB,optC,optD


on 29 aug the Modification included is the Key Assigned to the Each question is Different to the Uid came from Post Request
The Automatically Added Key and Uid is added to the keyDict where key is the Question key in Exam and value is the Uid of the
Original Question

"""
        self.getQue = r"\<q\>(.+?)\<\/q\>" #re pattern used to split the received data into List Questions

        self.cutQue = r"(\d+?)\|\|(.+?)\|\|(.+?)\|\|(.+?)\|\|(.+?)\|\|(.+?)$" #re pattern used to Each question in list into Question and Options

        for queOpt in re.findall(self.getQue,self.page):
            for opt in re.findall(self.cutQue,queOpt):
                self.keys.append(self.key)
                self.keyDict[str(self.key)] = opt[0]
                self.queDict[str(self.key)] = opt[1]
                self.optADict[str(self.key)] = opt[2]
                self.optBDict[str(self.key)] = opt[3]
                self.optCDict[str(self.key)] = opt[4]
                self.optDDict[str(self.key)] = opt[5]
                self.key = self.key + 1
                

        """
This is used for CSV Reader
        for row in reader:
            key = row[0]
            self.keys.append(key)
            self.queDict[str(key)] = row[1]
            self.optADict[str(key)] = row[2]
            self.optBDict[str(key)] = row[3]
            self.optCDict[str(key)] = row[4]
            self.optDDict[str(key)] = row[5]
        f.close()
        """
if __name__ == "__main__":
    data = TestData()
    print "no of Questions"
    print len(data.keys)
    
