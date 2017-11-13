import salabim as sim

'''
class AnimateLane(sim.Component):
    def __init__(self, i):
	self.i = i
	sim.Animate.__init__(self,
            rectangle0=(-20, -20, 20, 20), x0=49, y0=100 + 60 * i, fillcolor0='blue', linewidth0=0)

class AnimateCustomer(sim.Component):
    def __init__(self, i):
	self.i = i
	sim.Animate.__init__(self,
            rectangle0=(-10, -10, 10, 10), x0=350 - 30 * i, y0=95, fillcolor0='red', linewidth0=0)

    def visible(self, t):
        return waitingline[self.i] is not None


def do_animation():
    env.animation_parameters()
    
    for i in range(len(lanes)):
        AnimateCashier(i)

    for i in range(1):
	#if lane.ispassive():
	   AnimateWaitSquare(i)
'''


class CustomerGenerator(sim.Component):
    def process(self):
        while True:
            Customer()
            yield self.hold(sim.Exponential(6).sample())


class Customer(sim.Component):
    def process(self):
        self.enter(waitingline)
        for lane in lanes:
            if lane.ispassive():
                lane.activate()
                break  # activate only one lane
        yield self.passivate()


class Lane(sim.Component):
    def process(self):
        while True:
            while len(waitingline) == 0:
                yield self.passivate()
            self.customer = waitingline.pop()
            yield self.hold(sim.Exponential(5).sample())
            self.customer.activate()


env = sim.Environment(trace=False)
CustomerGenerator()
lanes = sim.Queue('lanes')
for i in range(1):
    Lane().enter(lanes)
waitingline = sim.Queue('waitingline')

env.run(till=360)
#waitingline.length.print_histogram(30, 0, 1)
print()
waitingline.print_info()
waitingline.print_statistics()

#waitingline.length.print_histogram(30, 0, 1)
print()
#waitingline.length_of_stay.print_histogram(30, 0, 10)

waitingline.length_of_stay.print_statistics()
waitingline.length.print_statistics()
