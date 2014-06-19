#!/usr/bin/env python
import datetime, os

#this method expects a two-dimensional list containing the data as lst, and a one-dimensional list containing titles as titlelst
def generate(lst, titlelst, count=[], folder=os.getcwd()+'/'):

    
    #hideous code to create the html report file with the prefix in the format of year month day hour minute
    report = open(folder + str(datetime.datetime.today()).replace(':','').replace(' ','-')[0:15]+'report.html','w')
    template = open(os.getcwd()+'/template.html', 'r')
    #Import js library to make tables sort

    for line in template:
        line= line.strip()
        if (line[:1] != '%'):
            report.write(line)
        if line == '%SORTTABLE%':
            report.write('<script src="'+ os.getcwd() + '/sorttable.js"></script>')
        elif line == '%CODELIST%':
            report.write('<a href="'+ os.getcwd() + '/reasoncodes.html" target="_blank">Reason Codes</a>')
        elif line == '%TITLES%':
            for title in titlelst:
                report.write('<th>'+title+'</th>\n')
        elif line == '%AMOUNT%':
            if count != []:
                report.write('<th># of Events</th>\n')
        elif line == '%VALUES%':
            #writes data
            for i in range(0,len(lst)):
                report.write('<tr>\n')
                for j in range(0,len(lst[i])):
                    report.write('<td>'+str(lst[i][j])+'</td>\n')
                if count != []:
                    report.write('<td>'+str(count[i])+'</td>\n')

    report.close()
    template.close()
    print("\n\nOutput to " + folder)
    
    
#for testing purposes
#generate('C:/Users/jeramy.lochner/Downloads/',[[0,1],[2,3]],['cats','dogs'], [10, 12])


    
