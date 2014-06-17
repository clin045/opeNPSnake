import datetime

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
    if start[0]=='*':
        temp_test_start.append(check.year)
    else:
        temp_test_start.append(int(start[0]))
    if start[1]=='*':
        temp_test_start.append(check.month)
    else:
        temp_test_start.append(int(start[1]))
    if start[2]=='*':
        temp_test_start.append(check.day)
    else:
        temp_test_start.append(int(start[2]))
    if start[3]=='*':
        temp_test_start.append(check.hour)
    else:
        temp_test_start.append(int(start[3]))
    if start[4]=='*':
        temp_test_start.append(check.minute)
    else:
        temp_test_start.append(int(start[4]))
    test_start=datetime.datetime(temp_test_start[0], temp_test_start[1], temp_test_start[2], temp_test_start[3], temp_test_start[4])
    #Do it again with the end date
    temp_test_end=[]
    if end[0]=='*':
        temp_test_end.append(check.year)
    else:
        temp_test_end.append(int(end[0]))
    if end[1]=='*':
        temp_test_end.append(check.month)
    else:
        temp_test_end.append(int(end[1]))
    if end[2]=='*':
        temp_test_end.append(check.day)
    else:
        temp_test_end.append(int(end[2]))
    if end[3]=='*':
        temp_test_end.append(check.hour)
    else:
        temp_test_end.append(int(end[3]))
    if end[4]=='*':
        temp_test_end.append(check.minute)
    else:
        temp_test_end.append(int(end[4]))
    test_end=datetime.datetime(temp_test_end[0], temp_test_end[1], temp_test_end[2], temp_test_end[3], temp_test_end[4])
    if test_start <= check <= test_end:
        return True
    else:
        return False