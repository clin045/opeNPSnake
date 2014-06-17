import os, sys, getopt, configparser, datetime
import htmlReportGen, fileParser

possible_params = []            #Possible parameters they could input
parameters = {}                 #Dictionary that holds the parameters:their filters

outputDir, inputDir = '', ''    #Folder where to report, folder where logs are

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
    possible_params = fileParser.checkFilesForParameters(inputDir)
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
    print(paramlst)
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
            possible_params = fileParser.checkFilesForParameters(inputDir)
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
        values, count = fileParser.parseFiles(inputDir, parameters)
        #stupid way to check if -t
        if 'Timestamp' in parameters:
            #take out everything except events in specified time range
            for v in values:
                print(v)
                date = v[list(parameters.keys()).index("Timestamp")]
                dt = datetime.datetime(int(date.split('/')[2].split(" ")[0]),int(date.split('/')[0]),int(date.split('/')[1]),int(date.split(' ')[1].split(':')[0]),int(date.split(':')[1]))
        #Generating the reports
        #If there wasn't a specified outputDir we just use the default(cwd)
        if outputDir == '':
            htmlReportGen.generate(values, parameters, count)
        else:
            htmlReportGen.generate(values, parameters, count, outputDir)

    elif ('-P', '') not in opts:
        print(helpfile)
        print("You did not specify any parameters")
            
if __name__ == '__main__':
    main()
