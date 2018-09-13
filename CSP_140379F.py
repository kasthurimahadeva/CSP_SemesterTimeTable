import csv
import sys, getopt

def readCSVFile(fileName):
    
    with open(fileName) as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')

        datas = []
        for data in readCSV:
            for i in range(len(data)):
                if(data[i] == ""):
                    data = data[ : i]
                    break
            datas.append(data)
    
    return datas

def writeCSVFile(fileName):
    dataStr = ""
    for row in assignments:
        rowStr = ""
        for column in row:
            rowStr += column + ','
        else:
            rowStr = rowStr[:-1]
        dataStr += rowStr + '\n'
    else:
        dataStr = dataStr[:-1]
    with open(fileName, 'w') as csvfile:
        csvfile.write(dataStr)


def forwardChecking(pendingSubs, availableSlots, currentSlot):
    copyOfPendingSubs = list(pendingSubs)
    copyOfAvailableSlots = dict(availableSlots)
    copyOfPendingSubs.pop(0)
    if(len(copyOfPendingSubs) == 0):
        return True
    noOfPendingSubs = len(copyOfPendingSubs)
    category = categories[(noOfSubs - noOfPendingSubs) - 1]
    categoryDetails = categories[(noOfSubs - noOfPendingSubs) : ]
    slotsDetails = slots[(noOfSubs - noOfPendingSubs) : ]

    if(category == "c"):
        del copyOfAvailableSlots[currentSlot]
    else:
        x = len(rooms)
        y = len(copyOfAvailableSlots[currentSlot])
        r = rooms[(x - y) : ]
        r.pop(0)
        copyOfAvailableSlots[currentSlot] = r

    for i in range(noOfPendingSubs):
        result = False
        if(categoryDetails[i] == "c"):
            for slot in slotsDetails[i]:
                if((slot in copyOfAvailableSlots) and (len(copyOfAvailableSlots[slot]) == len(rooms))):
                    result = True
                    break
        else:
            for slot in slotsDetails[i]:
                if(slot in copyOfAvailableSlots):
                    result = True
                    break
        if(result):
            continue
        else:
            return False
    if(result):
        return True


def backTracking():
    return False


def assigningTimeSlots():
    assignedTimeSlots = {}
    pendingSubs = subs[:]
    assignedSubs = []
    availableSlots = timeSlots

    for i in range(noOfSubs):
        result = False
        if(categories[i] == "c"):
            for slot in slots[i]:
                if((slot in availableSlots) and (len(availableSlots[slot]) == len(rooms))):
                    if(forwardChecking(pendingSubs, availableSlots, slot)):
                        assignments[i] = [subs[i], slot, rooms[0]]
                        assignedSubs.append(pendingSubs.pop(0))
                        assignedTimeSlots[slot] = rooms
                        del availableSlots[slot]
                        result = True
                        # print(subs[i] , " is assigned")
                        break
            if(result):
                continue
            else:
                backTracking()
        else:
            for slot in slots[i]:
                if(slot in availableSlots):
                    if(forwardChecking(pendingSubs, availableSlots, slot)):
                        x = len(rooms)
                        y = len(availableSlots[slot])
                        r = rooms[(x - y) : ]
                        assignments[i] = [subs[i], slot, availableSlots[slot][0]]
                        assignedTimeSlots[slot] = [availableSlots[slot][0]]
                        assignedSubs.append(pendingSubs.pop(0))
                        if(len(r) > 1):
                            r.pop(0)
                            availableSlots[slot] = r
                        else:
                            del availableSlots[slot]
                        result = True
                        # print(subs[i], " is assigned")
                        break
            if(result):
                continue
            else:
                backTracking()
            
    if(len(pendingSubs) == 0):
        return True
    else:
        return False

subs = []
slots = []
categories = []

assignments = []
timeSlots = {}
prioritySubs = {}
priorityOrder = {}
rooms = []
noOfSubs = 0


inputfile = sys.argv[1]
outputfile = sys.argv[2]

inputData = readCSVFile(inputfile)
rooms = inputData.pop()
noOfSubs = len(inputData)

for i in range(noOfSubs):
    priority = 0
    if(inputData[i][1] == "c"):
        priority += 1
    priority += len(inputData[i][2:])
    prioritySubs[inputData[i][0]] = priority
    priorityOrder[i] = priority


subs = sorted(prioritySubs, key = prioritySubs.__getitem__)
order = sorted(priorityOrder, key = priorityOrder.__getitem__)

for j in order:
    categories.append(inputData[j][1])
    slots.append(inputData[j][2:])
    assignments.append([inputData[j][0], "", ""])


for i in slots:
    for j in i:
        timeSlots[j] = rooms

if(assigningTimeSlots()):
    writeCSVFile(outputfile)
    for data in assignments:
        print data[0], " | ", data[1], " | ", data[2]
    print("Solution found!")
else:
    print("Solution cannot found")              
