import os, sys, getopt, configparser, datetime
import htmlReportGen
from collections import OrderedDict

possible_params = []            #Possible parameters they could input
parameters = {}                 #Dictionary that holds the parameters:their filters

outputDir, inputDir = '', ''    #Folder where to report, folder where logs are

front_extra = ' data_type="4">' #Needed for parsing xml values, the front tags end
back_extra = '</'               #Needed for parsing xml values, the back tags front

values, count = [], []          #Values holds the lines in the report
                                #Count is how many times an identical line appeared


start_time, end_time = "", ""   #Start and end time frames given by user

#When -h is called or the user doesn't do something right
helpfile="""
               ,   .,---.,---.          |         
,---.,---.,---.|\  ||---'`---.,---.,---.|__/ ,---.
|   ||   ||---'| \ ||        ||   |,---||  \ |---'
`---'|---'`---'`  `'`    `---'`   '`---^`   ``---'
     |

Parses NPS logs and generates useful reports

Usage: python opeNPSnake.py -i "filepath" [options]

Options:
    -h Prints out this help file
    -i Input file/directory (YOU MUST QUOTE THE FILE PATH)
    -o Output directory (Defaults to the current working directory)
    -P Prints list of log parameterss
    -p Select parameters for parsing [-p arg1:filter1,arg2:filter2:filter3,arg3]
    -c Specifies config file (see sample.conf)
    -t Specify the time frame [-t "* * * * *,* * * * *"] Year, Month, Day, Hour, Minute

Note: Fully-Qualifed-User-Names is not spelled correctly in the logs.
     
"""

#Gets the xml values from the logs
#Expects the line of text from the log, the starting <' '> tag and ending </' '> tag
def get_xml_value(line, start_tag, end_tag):
    x = line.find(start_tag)
    if x == -1:                     #Returns N/A if that tag isn't there
        return "N/A"
    x += len(start_tag + front_extra)
    y = line.find(end_tag)
    return line[x:y]

#Parses the files and pulls the desired values
def parseFiles():
    for file in os.listdir(inputDir):
        if file.endswith('.log'):
            print("Parsing data from file: " + file)
            inputFile = open(inputDir + file)
            lines = inputFile.readlines()       #List of lines in the file
            for line in lines:
                #Temp variable to store the values that will be reported
                values_temp = []
                #Boolean for checking if a filter has been broken
                #False = the values get reported
                #True = A filter has been broken
                broken_filter = False
                for param in parameters:
                    #The front <' '> tag
                    start_tag = param
                    #The back </' '> tag
                    end_tag = back_extra + param
                    #temp storage for the values
                    xml_value = get_xml_value(line, start_tag, end_tag)
                    #Checks to see if it gets passed the filter or there is no filter
                    if xml_value in parameters[param] or len(parameters[param]) <= 0:
                        values_temp.append(xml_value)
                    else:
                        broken_filter = True
                if not broken_filter:
                    #Checks to see if this is a duplicate line
                    if values_temp not in values:
                        values.append(values_temp)
                        count.append(1)
                    #Adds one to count if it is
                    else:
                        index = values.index(values_temp)
                        count[index] += 1 
            inputFile.close()

#Parses the files for possible parameter types
def checkFilesForParameters():
    for file in os.listdir(inputDir):
        if file.endswith('.log'):
            inputfile = open(inputDir + file)
            #List that holds all the lines in the file
            lines = inputfile.readlines()
            #temp variable to hold a place in a line so we progress through the line
            lastindex = 0
            for line in lines:
                while lastindex != -1:
                    #Where the last item was
                    lastindex = line.find(back_extra, lastindex)
                    #Next items first <' '>
                    fbracket = int(line.find(back_extra, lastindex)) + 2
                    #Next items second </' '>
                    sbracket = int(line.find('>', lastindex))
                    #Break if there are no more values
                    if sbracket == -1:
                        break
                    param = line[fbracket:sbracket]
                    #No duplicates
                    if param not in possible_params:
                        possible_params.append(param)
                    lastindex+=1
            inputfile.close()
    #These variable break or are specified through another cmdline argument
    for param in ["Timestamp", "User-Name", "Event"]:
        possible_params.remove(param)

#Returns a reformatted folder path
def getFolderPath(path):
    #Replace the \ slashes with / so we don't get unicode errors
    temp = path.replace('\\', '/')
    #Add a / to the end if there isn't one
    if temp[-1:] != "/":
        temp += "/"
    return temp

#Checks the parameters that the user specified and drops the ones that
#Aren't in the logs
def getParameters(params):
    checkFilesForParameters()
    global parameters
    for p in params:
        if p not in parameters and p in possible_params:
            parameters[p] = params[p]
        else:
            print(p + " is not a valid parameter")

#Returns a dictionary {key:value} = {parameter:[filter1, filter2, etc]}            
def getFilters(arg):
    params = arg.split(',')
    paramlst = {}
    for p in params:
        if p[0] == " ":
            p = p[1:]
        filterlst=[]
        try:
            filterlst=p.split(':')[1:]
        except:
            filterlst.append('')

        paramlst[p.split(':')[0].lower().replace(' ', '-').title()]=filterlst
    return paramlst

#loads config file
def loadConf(loc):
    global inputDir,outputDir
    loc = loc.replace('\\', '/')
    c = configparser.ConfigParser()
    c.read(loc)
    section='Config'
    options=c.options(section)
    paramlst = {}
    for o in options:
        if o == 'parameters':
            arg = c.get(section,o)
            paramlst = getFilters(arg)
        if o == 'input':
            inputDir = getFolderPath(c.get(section,o))
        if o == 'output':
            outputDir = getFolderPath(c.get(section,o))
    getParameters(paramlst)

#convert user supplied date to correct format
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

#Main
#We should probably split this up but whatever
def main():
    global filters
    global outputDir, inputDir
    global start_time, end_time
    #get the cmd line options
    #try:
    opts, args = getopt.getopt(sys.argv[1:],'hi:o:Pp:t:c:')
    #except:
    #    print(helpfile)
    #do stuff based on options
    for opt, arg in opts:
        paramlst = {}
        #print help file
        if opt == '-h':
            print(helpfile)
        #get input directory
        elif opt == '-i':
            inputDir = getFolderPath(arg)
        #get output directory
        elif opt == '-o':
            outputDir = getFolderPath(arg)
        #prints out list of parameters
        elif opt == '-P':
            checkFilesForParameters()
            for param in possible_params:
                print(param.replace("-", " "))
        #selects parameters for parsing
        elif opt == '-p':
            paramlst = getFilters(arg)
        #specifies the time frame
        elif opt == '-t':
            times = arg.split(',')
            parameters['Timestamp']=''
            global start_time,end_time
            start_time,end_time=convertDate(times)
            
        #Load parameters/filters from a config file
        elif opt == '-c':
            loadConf(arg)
    #Make sure they specified a -p parameter
    getParameters(paramlst)
    if len(parameters) > 0:
        parseFiles()
        ordParameters = OrderedDict(parameters)
        #stupid way to check if -t
        if 'Timestamp' in ordParameters:
            ordParameters.move_to_end("Timestamp")
            #take out everything except events in specified time range
            for v in values:
                date = v[0]
                print(v)
                dt = datetime.datetime(datetime.datetime(int(date.split('/')[2]),int(date.split('/')[1]),int(date.split('/')[0]),int(time.split(':')[0]),int(time.split(':')[1])))
                print(dt)
        #Generating the reports
        #If there wasn't a specified outputDir we just use the default(cwd)
        if outputDir == '':
            htmlReportGen.generate(values, ordParameters, count)
        else:
            htmlReportGen.generate(values, ordParameters, count, outputDir)

    elif ('-P', '') not in opts:
        print(helpfile)
        print("You did not specify any parameters")
            
if __name__ == '__main__':
    main()
