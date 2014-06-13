#!/usr/bin/env python
import datetime

#hideous code to create the html report file with the prefix in the format of year month day hour minute
report = open(str(datetime.datetime.today()).replace(':','').replace('.','').replace(' ','').replace('-','')[0:14]+'report.html','w')


#this method expects a two-dimensional list containing the data as lst, and a one-dimensional list containing titles as titlelst
def generate(lst,titlelst):
    #make the document pretty (inthefuture)

    report.write('<table border="1">')
    report.write('<tr>\n')
    #writes titles as heading
    for title in titlelst:
        report.write('<th>'+title+'</th>\n')
    report.write('</tr>\n')
    #writes data
    for i in range(0,len(lst)):
        report.write('<tr>\n')
        for j in range(0,len(lst[i])):
            report.write('<td>'+str(lst[i][j])+'</td>\n')
            
        report.write('</tr>\n')
    report.write('</table>')
    
<<<<<<< HEAD
    
#for testing purposes
=======

>>>>>>> origin/master
generate([[0,1],[2,3]],['cats','dogs'])


    
