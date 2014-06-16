#!/usr/bin/env python
import datetime, os

#this method expects a two-dimensional list containing the data as lst, and a one-dimensional list containing titles as titlelst
def generate(lst, titlelst, count=[], folder=os.getcwd()+'/'):
    #make the document pretty (inthefuture)
    
    #hideous code to create the html report file with the prefix in the format of year month day hour minute
    report = open(folder + str(datetime.datetime.today()).replace(':','').replace('.','').replace(' ','').replace('-','')[0:14]+'report.html','w')
    #Import js library to make tables sort
    report.write('<head>')
    report.write('<script src="'+ os.getcwd() + '/sorttable.js"></script>')
    report.write('</head>')
    report.write("""
    <style>
h1{
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 30px;
    color: #003399
    background: #fff;
    margin: 45px;
    text-align: left;
}

table
{
	font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
	font-size: 12px;
	background: #fff;
	margin: 45px;
	width: 480px;
	border-collapse: collapse;
	text-align: left;
}
table th
{
	font-size: 14px;
	font-weight: normal;
	color: #039;
	padding: 10px 8px;
	border-bottom: 2px solid #6678b1;
}
table td
{
	border-bottom: 1px solid #ccc;
	color: #669;
	padding: 6px 8px;
}
table tbody tr:hover td
{
	color: #009;
}
 
</style>
<h1>opeNPSnake</h1>
                 """)
    report.write('<table class="sortable">')
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
    print("\n\nOutput to " + folder)
    
    
#for testing purposes
#generate('C:/Users/jeramy.lochner/Downloads/',[[0,1],[2,3]],['cats','dogs'], [10, 12])


    
