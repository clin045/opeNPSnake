import datetime
import os
#Returns a reformatted folder path
def getFolderPath(path):
    #Replace the \ slashes with / so we don't get unicode errors
    temp = path.replace('\\', '/')
    #Add a / to the end if there isn't one
    if temp[-1:] != "/":
        temp += "/"
    return temp
#checks if date is in range
#the start and end dates are lists of strings, check should be a datetime object
def checkDateinRange(start, end, check):
    #make a new datetime object with the given parameters, replacing * with the parameters of check
    temp_test_start=[]
    check_list = [check.year, check.month, check.day, check.hour, check.minute]
    for x in range(0, 5):
        if start[x]=='*':
            temp_test_start.append(check_list[x])
        else:
            temp_test_start.append(int(start[x]))
    test_start=datetime.datetime(temp_test_start[0], temp_test_start[1], temp_test_start[2], temp_test_start[3], temp_test_start[4])
    #Do it again with the end date
    temp_test_end=[]
    for x in range(0, 5):
        if end[x]=='*':
            temp_test_end.append(check_list[x])
        else:
            temp_test_end.append(int(end[x]))
    test_end=datetime.datetime(temp_test_end[0], temp_test_end[1], temp_test_end[2], temp_test_end[3], temp_test_end[4])
    if test_start <= check <= test_end:
        return True
    else:
        return False

def genReport(values, parameters, count=[], folder=os.getcwd()+'/', repType='csv'):
    if repType== 'csv':
        differs = ['csv', ',']
    else:
        differs = ['tsv', '\t']
    report = open(folder + str(datetime.datetime.today()).replace(':','').replace(' ','-')[0:15]+'report.'+differs[0],'w')
    for p in parameters:
        report.write(p+differs[1])
    if count != []:
        report.write('# of Events')
    report.write('\n')
    for v in values:
        for i in range(0, len(v)):
            report.write(v[i] + differs[1])
        if count != []:
            report.write(str(count[values.index(v)]))
        report.write('\n')
    print('\n\nOutput to ' + folder)