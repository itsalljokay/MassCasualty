import numpy
import simpy

number_of_mres = 5
marines_present = 0
marines_total = 10
marine_counter = 0

simulation_time = 10

class Marine:
    def __init__(self):
        self.id = marine_counter
        self.priority_number = numpy.random.choice([1, 2])

        #DEBUGGING
        print("Priority Number: ", self.priority_number)

class System:
    def __init__(self):
        self.env = simpy.Environment()
        #Define Our Simulation Resources
        #People
        self.mre_resource_definition = simpy.PriorityResource(self.env, capacity = number_of_mres)

    def marine_generator(self):
        while marines_present < marines_total:
            marine = Marine()
            yield self.env.process(self.mre_handout(marine))
    
    
    def mre_handout(self, marine):
        mre_request = self.mre_resource_definition.request()
        if marine.priority_number == 1:
            yield mre_request
            print("You Got an MRE")

        if marine.priority_number == 2:
            print("Too bad!")

        marine_counter += 1
    
model = System()
model.env.process(model.marine_generator())
model.env.run(until=simulation_time)