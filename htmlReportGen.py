#!/usr/bin/env python
import datetime

#this method expects a two-dimensional list containing the data as lst, and a one-dimensional list containing titles as titlelst
def generate(folder, lst, titlelst, count=[]):
    #make the document pretty (inthefuture)
    #hideous code to create the html report file with the prefix in the format of year month day hour minute
    report = open(folder + str(datetime.datetime.today()).replace(':','').replace('.','').replace(' ','').replace('-','')[0:14]+'report.html','w')
    report.write('<table border="1">')
    report.write('<tr>\n')
    #writes titles as heading
    for title in titlelst:
        report.write('<th>'+title+'</th>\n')
    if count != []:
        report.write('<th>Amount</th>\n')
    report.write('</tr>\n')
    #writes data
    for i in range(0,len(lst)):
        report.write('<tr>\n')
        for j in range(0,len(lst[i])):
            report.write('<td>'+str(lst[i][j])+'</td>\n')
        if count != []:
            report.write('<td>'+str(count[i])+'</td>\n')
        report.write('</tr>\n')
    report.write('</table>')
    report.close()
    
    
#for testing purposes
#generate('C:/Users/jeramy.lochner/Downloads/',[[0,1],[2,3]],['cats','dogs'], [10, 12])


    
