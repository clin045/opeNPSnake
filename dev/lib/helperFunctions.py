#Returns a reformatted folder path
def getFolderPath(path):
    #Replace the \ slashes with / so we don't get unicode errors
    temp = path.replace('\\', '/')
    #Add a / to the end if there isn't one
    if temp[-1:] != "/":
        temp += "/"
    return temp

def convertDate(times):
    time_start_split = times[0].split(' ')
    time_start_parsed=[]
    for s in time_start_split:
        if s == '*':
            s = 1
        else:
            s = int(s)
        time_start_parsed.append(s)
    temp_start = datetime.datetime(time_start_parsed[0], time_start_parsed[1], time_start_parsed[2], time_start_parsed[3], time_start_parsed[4])
    time_end_split = times[1].split(' ')
    time_end_parsed=[]
    for s in time_end_split:
        if s == '*':
            s = 1
        else:
            s = int(s)
        time_end_parsed.append(s)
    temp_end = datetime.datetime(time_end_parsed[0], time_end_parsed[1], time_end_parsed[2], time_end_parsed[3], time_end_parsed[4])
    return temp_start,temp_end