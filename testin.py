import random
import operator
import math

class Process(object):
    waitingt = 0
    turnt = 0

    def __init__(self, name, burst, arrivt):
        self.name = name
        self.burst = burst
        self.arrivt = arrivt

    def getBurst(self):
        return self.burst

    def getArrivt(self):
        return  self.arrivt


def waitingt(list):
    i = 1
    j = 0

    while i < len(list):
        list[i].waitingt = 0
        while j < i:
            list[i].waitingt = list[j].burst + list[i - 1].waitingt
            j += 1
        i += 1


def turnt(list):

    for i in list:
        i.turnt = i.burst + i.waitingt

def avwaitingturn(list):

    avwt = 0
    avtt = 0
    for i in list:
        avwt += i.waitingt
        avtt += i.turnt

    avwt /= len(list)
    avtt /= len(list)

    print('\nAverage waiting time: ~ {}\nAverage turnaround time: ~ {}'.format(math.floor(avwt), math.floor(avtt)))

def printlog(list):

    print('\nProcess\t\tBurst Time\tWaiting Time\tTurnaround Time')
    for i in list:
        print('\n   {}\t\t\t{}\t\t\t{}\t\t\t\t{}'.format(i.name, i.burst, i.waitingt, i.turnt))

def fcfs(list):

    # calculating waiting time
    waitingt(list)

    # calculating turnaround time
    turnt(list)

    printlog(list)

    avwaitingturn(list)

def sjf(list):
    list = sortb(list)
    waitingt(list)
    turnt(list)
    printlog(list)
    avwaitingturn(list)

def srtf(list):
    list = sortat(list)
    list = sortb(list)

    waitingt(list)
    turnt(list)
    printlog(list)
    avwaitingturn(list)


def sortb(list):
    list = sorted(list, key=Process.getBurst)

    return list


def sortat(list):
    list = sorted(list, key=Process.getArrivt)

    return list

def create_process():

    print("\n\t**************** STAGING ALGORITHMS ****************")
    print("\t** 1 - FCFS  2 - SJF  3 - SRTF  4 - RR  5 - M.level **")
    print("\t********************** CHOOSE ************************")
    o = int(input())

    n = int(input("How many process you wanna simulate?"))
    list = []

    c = input("Burst: random or manual(R/M)?")

    if c == 'R' or c == 'r':
        # automatic burst and arrival time
        for i in range(n):
            if o == 1 or o == 2:
                b = random.randint(1, 100)
                list.append(Process('P' + str(i+1), b, 0))
            else:
                b = random.randint(1, 100)
                a = random.randint(1, 15)
                list.append(Process('P' + str(i), b, a))
    else:
        # manual burst and arrival time
        for i in range(n):
            b = int(input("P" + str(i+1) + " Burst:"))
            if o == 1 or o == 2:
                t = 0
            else:
                t = int(input("P" + str(i + 1) + " Tempo de Chegada:"))

            proc = Process('P' + str(i+1), b, t)
            list.append(proc)

        print(list[0].burst)

    # menu continuation
    if o == 1:
        fcfs(list)
    if o == 2:
        sjf(list)
    if o == 3:
        srtf(list)


create_process()




