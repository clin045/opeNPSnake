#get file input                             -
#get what parameters they want              -
#find data
#store in list
#generate report

#test_folder = C:\Users\jeramy.lochner\Desktop\NPSLogFile



import os, sys, getopt
import htmlReportGen

parameters = []         #Parameters input by users
possible_params = []    #Possible parameters they could input
folder = ""             #Folder where logs are located
filters = []

front_extra = ' data_type="4">'
back_extra = '</'

values, count = [], []

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
    -o Output directory
    -P Prints list of log parameterss
    -p Specifies parameters you want to grab [-p arg1,arg2,arg3]
    -c TODO Specifies config file

Note: Fully-Qualifed-User-Names is not spelled correctly in the logs.
     
"""


def get_xml_value(line, start_tag, end_tag):
    x = line.find(start_tag)
    if x == -1:
        return "N/A"
    x += len(start_tag + front_extra)
    y = line.find(end_tag)
    return line[x:y]


def parseFiles():
    for file in os.listdir(folder):
        if file.endswith('.log'):
            print("Parsing data from file: " + file)
            inputfile = open(folder + file)
            lines = inputfile.readlines()
            for line in lines:
                params_temp = []
                broken_filter = False
                for param in parameters:
                    start_tag = param
                    end_tag = back_extra + param
                    xml_value = get_xml_value(line, start_tag, end_tag)
                    index = parameters.index(param)
                    if xml_value == filters[index] or filters[index] == "":
                        params_temp.append(xml_value)
                    else:
                        broken_filter = True
                if not broken_filter:
                    if params_temp not in values:
                        values.append(params_temp)
                        count.append(1)
                    else:
                        index = values.index(params_temp)
                        count[index] += 1 
            inputfile.close()
                    
def checkFilesForParameters():
    for file in os.listdir(folder):
        if file.endswith('.log'):
            inputfile = open(folder + file)
            lines = inputfile.readlines()
            lastindex = 0
            for line in lines:
                while lastindex != -1:
                    lastindex = line.find(back_extra, lastindex)
                    fbracket = int(line.find(back_extra, lastindex)) + 2
                    sbracket = int(line.find('>', lastindex))
                    if sbracket == -1:
                        break
                    param = line[fbracket:sbracket]
                    if param not in possible_params:
                        possible_params.append(param)
                    lastindex+=1
            inputfile.close()
    for param in ["Timestamp", "User-Name", "Event"]:
        possible_params.remove(param)
    
    
def getFolderPath(path):
    global folder
    temp = path.replace('\\', '/')
    if temp[-1:] != "/":
        temp += "/"
    folder = temp
    

def getParameters(params):
    checkFilesForParameters()
    for p in params:
        p = p.lower().replace(' ','-').title()
        if p not in parameters and p in possible_params:
            parameters.append(p)
        elif p not in possible_params:
            print(p + " isn't a valid parameter")
    
def main():
    global filters
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hi:o:Pp:')
    except:
        print(helpfile)
    for opt, arg in opts:
        if opt == '-h':
            print(helpfile)
        elif opt == '-i':
            getFolderPath(arg)
        #TODO set output dir
        elif opt == '-P':
            checkFilesForParameters()
            print()
            for param in possible_params:
                print(param.replace("-", " "))
        elif opt == '-p':
            params = []
            params = arg.split(',')
            paramlst = []
            filterlst = []
            for p in params:
                paramlst.append(p.split(':')[0])
                try:
                    filterlst.append(p.split(':')[1])
                except:
                    filterlst.append('')
            filters = filterlst
            getParameters(paramlst)
            parseFiles()
            htmlReportGen.generate(folder, values, parameters, count)

            
if __name__ == '__main__':
    main()

