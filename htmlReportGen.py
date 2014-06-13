#!/usr/bin/env python
import datetime


print(str(datetime.datetime.today()).replace(':','').replace('.','').replace(' ','').replace('-','')[0:14])
report = open(str(datetime.datetime.today()).replace(':','').replace('.','').replace(' ','').replace('-','')[0:14]+'report.html','w')
