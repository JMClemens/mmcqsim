import salabim as sim

class AnimateCashier(sim.Animate):
    def __init__(self, i):
        self.i = i
        sim.Animate.__init__(self,
            rectangle0=(-20, -20, 20, 20), x0=49, y0=100 + 60 * i, fillcolor0='blue', linewidth0=0)


class AnimateWaitSquare(sim.Animate):
    def __init__(self, i):
        self.i = i
        sim.Animate.__init__(self,
            rectangle0=(-10, -10, 10, 10), x0=350 - 30 * i, y0=95, fillcolor0='red', linewidth0=0)

    def visible(self, t):
        return q[self.i] is not None


class AnimateWaitSquare2(sim.Animate):
    def __init__(self, i):
        self.i = i
        sim.Animate.__init__(self,
            rectangle0=(-10, -10, 10, 10), x0=350 - 30 * i, y0=135, fillcolor0='red', linewidth0=0)

    def visible(self, t):
        return q2[self.i] is not None


def do_animation():
    env.animation_parameters()
    
    for i in range(2):
        AnimateCashier(i)
    for i in range(10):
	AnimateWaitSquare(i)
	AnimateWaitSquare2(i)
    show_length = sim.Animate(text='', x0=370, y0=100, textcolor0='black', anchor='w')
    show_length.text = lambda t: 'Length= ' + str(len(q))
    show_length = sim.Animate(text='', x0=370, y0=135, textcolor0='black', anchor='w')
    show_length.text = lambda t: 'Length= ' + str(len(q))

class Person(sim.Component):
    def process(self):
        self.enter(q)
        yield self.hold(sim.Exponential(5).sample())
        self.leave(q)


class Person2(sim.Component):
    def process(self):
        self.enter(q2)
        yield self.hold(sim.Exponential(5).sample())
        self.leave(q2)

env = sim.Environment(trace=True)

q = sim.Queue('q')
for i in range(15):
    Person(name='{:02d}'.format(i), at=i)

q2 = sim.Queue('q2')
for j in range(15):
    Person2(name='{:02d}'.format(j), at=j)
do_animation()

env.run()

