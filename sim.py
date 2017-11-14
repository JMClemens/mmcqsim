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
from collections import defaultdict
from decimal import *

class AnimateCustomer(sim.Animate):
    pass

class AnimateCashier(sim.Animate):
    pass

class AnimateCustomerVisit(sim.Animate):
    pass

def do_animation():
    pass

# This class generates customers
class CustomerGenerator(sim.Component):
    def process(self):
        while True:

            # creates a new customer
            Customer()

            #print("Peek\n")
            #print(env.peek())

            # waits to generate the next customer based on
            # an expontentially distributed interrarrival time
            yield self.hold(sim.Exponential(6,r.seed()).sample())

# This class defines our customer behavior
class Customer(sim.Component):
    def process(self):

        # has the customer enter our waiting line queue
        self.enter(waitingline)

        # the customer checks each cashier to see if one is available for service
        for cashier in cashiers:
            if cashier.ispassive():
                cashier.activate()
                break  # activate only one clerk

        # if no cashiers are available for service, then the customer must wait
        yield self.passivate()

# This class defines our cashier behavior
class Cashier(sim.Component):
    def setup(self):
        self._schedET = 0
        self._currcname = ''

    def process(self):
        while True:

            # if there is nobody in their waiting line, they continue to wait
            while len(waitingline) == 0:
                yield self.passivate()
            
            # otherwise, they remove a customer from the queue
            self.customer = waitingline.pop()

            # and then they 'hold' the customer, or make them wait 
            # based on an exponentially distributed service time
            yield self.hold(sim.Exponential(5,r.seed()).sample())
            
            self.customer.activate()

            self._currcname = self.customer.name()
            print("\nCustomer name: " + self._currcname + '\n')

            self._schedET = env.peek()
            print("\nCustomer end time: " + str(self._schedET))
            
            '''
            print("Peek\n")
            print(env.peek())
			'''

	def getEndCustomerName(self):
		return string(self._currcname).rsplit('.',1)[1]

    def getScheduledEndTime(self):
    	return float(self._schedET)

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


# TODO: Add visual animation to simulation

if __name__ == "__main__":

    # this range is the number of cashiers we are running our tests for
    # 2,11 runs our trials for 2 cashier lanes through 10 cashier lanes
    for numCashiers in range(2,3):


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
        # change for a different number of trials
        for i in range(5): # TODO: change back to 4191 from 5

            # create a new environment to sim
            env = sim.Environment(trace=True)


            # start our customer generations
            CustomerGenerator()

            # put our cashiers into their own queue
            cashiers = sim.Queue('cashier')
            for i in range(numCashiers):
                Cashier().enter(cashiers)

            # simulate the waiting line for the customers
            waitingline = sim.Queue('waitingline')

            # 1 time unit = 1 minute
            # run simulation for 6 hours, or 360 mins
            env.run(till=360)


            # changes the standard output from the terminal to our different files
            # allows us to write that output to files for further processing
            sys.stdout = f
            waitingline.length_of_stay.print_statistics()
            sys.stdout = f2
            waitingline.length.print_statistics()

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