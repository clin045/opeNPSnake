import os, sys, getopt, configparser, datetime, argparse
import htmlReportGen, fileParser, helperFunctions

possible_params = []            #Possible parameters they could input
parameters = {}                 #Dictionary that holds the parameters:their filters

outputDir, inputDir = '', ''    #Folder where to report, folder where logs are

values, count = [], []          #Values holds the lines in the report
                                #Count is how many times an identical line appeared


start_time, end_time = "", ""   #Start and end time frames given by user

outputFormat = 'html'

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
    -p Select parameters for parsing [-p arg1:filter1,arg2:filter2:!filter3,arg3] You can exclude results by prepending a filter with !
    -c Specifies config file (see sample.conf)
    -t Specify the time frame [-t "* * * * *,* * * * *"] Year, Month, Day, Hour, Minute. * is a wildcard.
    -H Generates output as a pretty HTML document (default)
    -C Generates output as a CSV file
    -T Generates output as a TSV file
     
"""

#Checks the parameters that the user specified and drops the ones that
#Aren't in the logs
def getParameters(params):
    possible_params = fileParser.checkFilesForParameters(inputDir)
    global parameters
    for p in params:
        if p[0] == " ":
            p = p[1:]
        if p not in parameters and p in possible_params:
            parameters[p] = params[p]
        elif p not in possible_params:
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
    global inputDir,outputDir,outputFormat
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
            inputDir = helperFunctions.getFolderPath(c.get(section,o))
        if o == 'output':
            outputDir = helperFunctions.getFolderPath(c.get(section,o))
        if o == 'timeframe':
            parameters['Timestamp']=''
            arg = c.get(section,o)
            global start_time,end_time
            start_time,end_time=arg.split(',')[0].split(' '),arg.split(',')[1].split(' ')
        if o == 'outputformat':
            arg = c.get(section,o)
            if arg=='H':
                outputFormat=0
            elif arg=='C':
                outputFormat=1
            elif arg=='T':
                outputFormat=2

    getParameters(paramlst)

#Main
#We should probably split this up but whatever
def main():
    global outputFormat
    global filters
    global outputDir, inputDir
    global start_time, end_time

    parser = argparse.ArgumentParser(prog="""
               ,   .,---.,---.          |         
,---.,---.,---.|\  ||---'`---.,---.,---.|__/ ,---.
|   ||   ||---'| \ ||        ||   |,---||  \ |---'
`---'|---'`---'`  `'`    `---'`   '`---^`   ``---'
     |
""",description=helpfile)
    parser.add_argument('--input', '-i', dest='inputDir', required=True, help='The directory where your logs are stored')
    parser.add_argument('--output', '-o', dest='outputDir', help='The directory where the report will be placed')
    parser.add_argument('--showParams', '-P', action='store_true', help='Shows the possible parameters')
    parser.add_argument('--params', '-p', dest='paramlst', help='The parameters and filters used')
    parser.add_argument('--timestamp', '-t', dest='time', help='Time frame of the information you want')
    parser.add_argument('--config', '-c', dest='configFile', help='The location of the configuration file')
    parser.add_argument('--HTML', '-H', action='store_true', help='If you want an HTML report')
    parser.add_argument('--CSV', '-C', action='store_true', help='If you want a CSV report')
    parser.add_argument('--TSV', '-T', action='store_true', help='If you want a TSV report')

    args = parser.parse_args()
    inputDir = helperFunctions.getFolderPath(args.inputDir)
    if args.outputDir:
        outputDir = helperFunctions.getFolderPath(args.outputDir)
    if args.showParams:
        possible_params = fileParser.checkFilesForParameters(inputDir)
        for param in possible_params:
            print(param.replace("-", " "))
    if args.paramlst:
        paramlst = getFilters(args.paramlst)
        getParameters(paramlst)
    if args.time:
        parameters['Timestamp']=''
        start_time,end_time=args.time.split(',')[0].split(' '),args.time.split(',')[1].split(' ')
    if args.configFile:
        loadConf(args.configFile)
    if args.HTML:
        outputFormat='html'
    elif args.CSV:
        outputFormat='csv'
    elif args.TSV:
        outputFormat='tsv'

    getParameters(paramlst)
    if len(parameters) > 0:
        values, count = fileParser.parseFiles(inputDir, parameters)
        #stupid way to check if -t
        if 'Timestamp' in parameters:
            #take out everything except events in specified time range
            tempv=[]
            for v in values:
                date = v[list(parameters.keys()).index("Timestamp")]
                dt = datetime.datetime(int(date.split('/')[2].split(" ")[0]),int(date.split('/')[0]),int(date.split('/')[1]),int(date.split(' ')[1].split(':')[0]),int(date.split(':')[1]))
                if helperFunctions.checkDateinRange(start_time,end_time,dt):
                    tempv.append(v)
            values=tempv
            for v in values:
                v.remove(v[list(parameters.keys()).index("Timestamp")])
            del(parameters['Timestamp'])
            temp = []
            for v in values:
                if v in temp:
                    count[temp.index(v)] += 1
                else:
                    temp.append(v)
                    count.append(1)
            values = temp
                
        #Generating the reports
        
        if outputFormat == 'html':
            #If there wasn't a specified outputDir we just use the default(cwd)
            if outputDir == '':
                htmlReportGen.generate(values, parameters, count)
            else:
                htmlReportGen.generate(values, parameters, count, outputDir)
        else:
            if outputDir == '':
                helperFunctions.genReport(values,parameters,count,repType=outputFormat)
            else:
                helperFunctions.genReport(values, parameters, count, outputDir, outputFormat)

    elif ('-P', '') not in opts and ('-h', '') not in opts:
        print(helpfile)
        print("You did not specify any parameters")
            
if __name__ == '__main__':
    main()