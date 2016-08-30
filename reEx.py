#Author : Kunchala Anil
#Date : 29 Aug 2016
#Simple Data Parsing

import re

line = "<q>12||Question1||opta||optb||optc||optd</q> <q>34||question2||opta||optb||optc||optd</q>"

pattern = r"\<q\>(.+?)\<\/q\>"

pattern2 = r"(\d+?)\|\|(.+?)\|\|(.+?)\|\|(.+?)\|\|(.+?)\|\|(.+?)$"


for queOpt in re.findall(pattern,line):
    for opt in re.findall(pattern2,queOpt):
        print opt[]
        print "done"
