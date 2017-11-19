'''
M/M/c queueing simulator

This program will run a simulation of a grocery store's cashering lanes,
and measure the average wait time in the queues and the average lengths of the queues
for different numbers of open cashiering lanes

Copyright (c) 2017 Karen Canas Hernandez, Joshua Clemens, Jacob Denion, Cory Watson, Afton Woodring

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sbm as sim
import random as r
import sys
import os
import csv
from collections import deque
from collections import defaultdict
from decimal import *


class AnimateWaitingClientSquare(sim.Animate):
    def __init__(self, pos):
        # define animation object for the green square of pos'th client in the queue
        self.pos = pos

        sim.Animate.__init__(
            self, rectangle0=(-20,-20,20,20), offsetx0=800-pos*50, offsety0=200,
            fillcolor0='green', linewidth0=0)

    def visible(self, t):
        client = cashiers.requesters()[self.pos]  # this gets the pos'th client in the requesters queue
        return client is not None  # hide if there's no client there


class AnimateWaitingClientText(sim.Animate):
    def __init__(self, pos):
        # define animation object for the sequence_number of pos'th client in the queue
        self.pos = pos

        sim.Animate.__init__(
            self, text='', offsetx0=800-pos*50, offsety0=200, textcolor0='white', anchor='center')

    def text(self, t):
        client = cashiers.requesters()[self.pos]  # this gets the pos'th client in the requesters queue
        if client:  # if there is a client
            return str(client.sequence_number())  # give the sequence_number
        else:
            return ''


class AnimateServicedClientSquare(sim.Animate):
    def __init__(self, index):
        # define animation object for the green/gray square for the index'th cashier
        self.index = index

        sim.Animate.__init__(
            self, rectangle0=(-20,-20,20,20), offsetx0=900, offsety0=200+index*50,
            linewidth0=0)

    def fillcolor(self, t):
        for client in cashiers.claimers():
            if client.cashier_index == self.index:
                return 'green'  # if there's a client as cashier index, make green
        return 'gray'  # if not, gray


class AnimateServicedClientText(sim.Animate):
    def __init__(self, index):
        # define animation object for the sequence_number for the index'th cashier
        self.index = index

        sim.Animate.__init__(
            self, text='', offsetx0=900, offsety0=200+index*50, textcolor0='white', anchor='center')

    def text(self, t):
        for client in cashiers.claimers():
            if client.cashier_index == self.index:
                return str(client.sequence_number())  # if there's a client at cashier index, show sequence_number
        return ''  # else, null string


def do_animation():
    for pos in range(20):  # show at most 20 waiting clients
        AnimateWaitingClientSquare(pos)  # to show a green square for the pos'th client in the waiting queue
        AnimateWaitingClientText(pos)  # to show the sequence number of the pos'th client in the waiting queue

    for index in range(numCashiers):
        AnimateServicedClientSquare(index)  # to show a green/gray square for the client served by cashier index
        AnimateServicedClientText(index)  # to show the sequence number of the client served by cashier index

    sim.Animate(text='cashier', x0=900, y0=200-50, anchor='n')
    sim.Animate(text='<-- Waiting line', x0=900-145, y0=200-50, anchor='n')
    env.animation_parameters(modelname='M/M/c')


class Client(sim.Component):
    def process(self):
        yield self.request(cashiers)
        self.cashier_index=idle_cashier_indexes.popleft()  # makes that cashiers are assigned round robin
        yield self.hold(sim.Exponential(5,r.seed()).sample())
        idle_cashier_indexes.append(self.cashier_index)  # return the cashier to the idle pool


class ClientGenerator(sim.Component):
    def process(self):
        while True:
            yield self.hold(sim.Exponential(6,r.seed()).sample())
            client = Client()


# This function reads the mean queue wait statistics file
# we created during simulation and takes just the averages
# and then places than info into a CSV for further processing
def writeMeanQueueWait():
    out_file = open(MeanQWait, 'w')
    with open(AllQWaitFile, 'r') as in_file:
        for line in in_file:
            if 'mean' in line:
                out_file.write(','.join(line.split()))
                out_file.write('\n')

    in_file.close()
    out_file.close()

# This function reads the mean queue length statistics file
# we created during simulation and takes just the averages
# and then places than info into a CSV file for further processing
def writeMeanQueueLength():
    out_file = open(MeanQLength, 'w')
    with open(AllQLengthFile, 'r') as in_file:
        for line in in_file:
            if 'mean' in line:
                out_file.write(','.join(line.split()))
                out_file.write('\n')

    in_file.close()
    out_file.close()

# This function outputs the average of the collected mean queue waits
# collected in the CSV file created in the functions above
def getMeanQueueWait():

    # create a new list collection to store our CSV data elements
    columns = defaultdict(list)

    # read our CSV and append the elements into our list
    with open(MeanQWait) as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            for (i,v) in enumerate(row):
                columns[i].append(v)

    # calculate the average of our collected means as a
    # Decimal to prevent binary-based float rounding errors
    # and print out that average
    qwMean = (sum(map(Decimal,columns[1])))/len(columns[i])
    print('Average queue wait (in minutes): ' + str(qwMean))

# This function outputs the average of the collected mean queue lengths
# collected in the CSV file created in the functions above
def getMeanQueueLength():

    # create a new list collection to store our CSV data elements
    columns = defaultdict(list)

    # read our CSV and append the elements into our list
    with open(MeanQLength) as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            for (i,v) in enumerate(row):
                columns[i].append(v)

    # calculate the average of our collected means as a
    # Decimal to prevent binary-based float rounding errors
    # and print out that average
    qlMean = (sum(map(Decimal,columns[1])))/len(columns[i])
    print('Average queue length: ' + str(qlMean))

# This function makes a list of all '.txt' files
# in our temp folder and removes them
def cleanupTxtFiles():
    mydir = os.getcwd() + '/temp'
    filelist = [f for f in os.listdir(mydir) if f.endswith(".txt")]
    for f in filelist:
        os.remove(os.path.join(mydir,f))
    print("Txt files deleted.")

# This function makes a list of all '.csv' files
# in our temp folder and removes them
def cleanupCsvFiles():
    mydir = os.getcwd() + '/temp'
    filelist = [f for f in os.listdir(mydir) if f.endswith(".csv")]
    for f in filelist:
        os.remove(os.path.join(mydir,f))
    print("CSV files deleted.")

# The function allows the user to choose which
# data they want to keep and what they would like to delete
def cleanupPrompt():

    print("\nFile cleanup options:\n")

    # option to delete temp folder and all its contents
    # return statement exits function afterwards so other options aren't given
    option1 = raw_input("Would you like to delete the temp folder and all tempory files \n" +
        " created during this simulation? (y/n)\n").lower()
    if(option1 == 'y'):
        cleanupTxtFiles()
        cleanupCsvFiles()
        os.rmdir(os.getcwd() + '/temp')
        return

    # option to delete all txt files
    option2 = raw_input("Would you like to delete TXT files with average queue wait time " +
         "\n and length statistical data from this simulation? (y/n)\n").lower()
    if(option2 == 'y'):
        cleanupTxtFiles()

    # option to delete all csv files
    option3 = raw_input("Would you like to delete CSV files with average queue wait time " +
        "\n and length from this simulation? (y/n)\n").lower()
    if(option3 == 'y'):
        cleanupCsvFiles()


# TODO: Implement visual animation to simulation and add terminal prompts

if __name__ == "__main__":
    # this range is the number of cashiers we are running our tests for
    # 2,11 runs our trials for 2 cashier lanes through 10 cashier lanes
    for numCashiers in range(2,11):

        # create the temp directory inside our current directory
        # to hold txt and csv files created during simulation
        mydir = os.getcwd() + '/temp'
        if not os.path.exists(mydir):
            os.makedirs(mydir)

        # writes our results to different files for each # of cashiering lanes
        AllQWaitFile = 'temp/' + str(numCashiers) + 'clerks-qw.txt'
        AllQLengthFile = 'temp/' + str(numCashiers) + 'clerks-ql.txt'
        MeanQWait = 'temp/' + str(numCashiers) + 'clerks-qw-means.csv'
        MeanQLength = 'temp/' + str(numCashiers) + 'clerks-ql-means.csv'


        # keep track of our normal terminal output and
        # create the files we are writing results to
        orig_out = sys.stdout
        f = open(AllQWaitFile,'w')
        f2 = open(AllQLengthFile,'w')

        # this range is the number of trials/simulations are running
        # change 4191 for a different number of trials
        for i in range(1000):

            # create a new environment to sim
            env = sim.Environment(trace=False)

            cashiers = sim.Resource('cashiers', capacity=numCashiers)
            idle_cashier_indexes= deque(range(numCashiers))  # this is to keep track of which cashiers are idle (only for animation)

            # start our customer generations
            ClientGenerator()

            '''
            cashiers = sim.Queue('cashier')
            for i in range(numCashiers):
                Cashier().enter(cashiers)
            waitingline = sim.Queue('waitingline')
            '''

            do_animation()

            # 1 time unit = 1 minute
            # run simulation for 6 hours, or 360 mins
            env.run(till=360)

            # changes the standard output from the terminal to our different files
            # allows us to write that output to files for further processing
            sys.stdout = f
            cashiers.requesters().length_of_stay.print_statistics()
            sys.stdout = f2
            cashiers.requesters().length_of_stay.print_statistics()

        # change the output back to console and close files
        sys.stdout = orig_out
        f.close()
        f2.close()

        # Write the mean queue waiting times to a new file
        writeMeanQueueWait()

        # Write the mean queue length to a new file
        writeMeanQueueLength()

        # Print the average of the mean queue length and mean queue wait
        print('Lanes open: ' + str(numCashiers))
        getMeanQueueLength()
        getMeanQueueWait()

    # Allow user to clean up files created during the simulation
    # or to keep them for further studying or processing
    cleanupPrompt()
