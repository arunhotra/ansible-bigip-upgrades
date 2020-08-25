import os
import json
import sys


CLOSING_BRACE = "}"
OPENING_BRACE = "{"
POOL_PREFIX = "ltm pool "
STATUS_PREFIX = 'status.availability-state '


cmdargs = sys.argv


# Parses the pool status obtained from ansible (using tmsh command). The output would be poolname:status

def parsePoolsStatus(inputfile):
    with open(inputfile) as infile:
        readingPool = False
        bracketCounter = 0
        poolName = ''
        poolStatus = ''
        poolObjects = {}
        for lineNum, line in enumerate(infile, 1):
            if POOL_PREFIX in line:
                readingPool = True
                poolName = line.split()[2]
            if readingPool == True:
                if OPENING_BRACE in line:
                    bracketCounter = bracketCounter + 1
                if CLOSING_BRACE in line:
                    bracketCounter = bracketCounter - 1
                if bracketCounter == 1:
                    if STATUS_PREFIX in line:
                        poolStatus = line.split()[1]
                if bracketCounter == 0:
                    poolObjects[poolName] = poolStatus
                    readingPool = False
                    bracketCounter = 0
                    poolFullName = ''
                    poolName = ''
                    poolStatus = ''
                    continue
    return poolObjects


# Formats the ansible data from //n to /n. This is done because ansible changes the tmsh output to a one line string and condenses all the /n's by escaping them.

def formattedOutput(ansibleOutputFileName):
    inputFile = ansibleOutputFileName + '.json'
    with open(inputFile, 'r') as in_json_file:
        data = json.load(in_json_file)
        data_content = data[0]
        data_content.replace('\\n', '\n')
    outputFile = ansibleOutputFileName + '.txt'
    with open(outputFile, 'w') as out_json_file:
        out_json_file.write(data_content)


os.chdir("../TMP")

hostname = cmdargs[1]

print(hostname)

formattedOutput(hostname)

poolStatus = parsePoolsStatus(hostname + '.txt')

statusFile = hostname + '_status.json'


with open(statusFile, 'w') as out_status_file:
    json.dump(poolStatus, out_status_file)
