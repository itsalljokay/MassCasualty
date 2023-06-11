import numpy
import simpy
from simpy import Monitor
import pandas

class VariablesAndParameters:
    number_of_runs = 5
    run_number = 0
    simulation_time = 100
    
    number_of_red_dedicated_doctors = 5
    number_of_yellow_dedicated_doctors = 3

    #Location Occupancy
    main_bds_maximum_occupancy = 92


class Track:
    #List of every Marine we generate by their unique ID (run_number).
    marines = []
    monitors = {}
class Marine:
    def __init__(self):
        self.id = VariablesAndParameters.run_number
        self.color = numpy.random.choice(["Red"])
        Track.marines[self.id]

        #DEBUGGING
        print("ID: ", self.id)
        print("Color: ", self.color)

class System:
    def __init__(self):
        #Initialize Environment
        self.env = simpy.Environment()
        #Create a Monitor For The Marine
        Track.monitors[self.id] = simpy.Monitor(self.env)
        #Define Our Simulation Resources
        #People
        self.red_doctor_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.number_of_red_dedicated_doctors)
        self.yellow_doctor_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.number_of_yellow_dedicated_doctors)

        #Locations
        self.main_bds_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.main_bds_maximum_occupancy)

    def marine_generator(self):
        while VariablesAndParameters.run_number < VariablesAndParameters.number_of_runs:
            marine = Marine()
            yield self.env.process(self.triage(marine))
    
    def triage(self, marine):

        if marine.color == "Red":
            #RED
            #LOCATION
            #Start Red Location Timer
            red_main_bds_location_timer_start = self.env.now
            print("Red Location Start Time: ", red_main_bds_location_timer_start)
            #Request Main BDS Location
            main_bds_request = self.main_bds_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield main_bds_request
            #Calculate Red Location Elapsed Time
            red_main_bds_location_elapsed_time = (self.env.now - red_main_bds_location_timer_start)
            print("Red Location Elapsed Time: ", red_main_bds_location_elapsed_time)
            #Add To Data
            Track.monitors[marine.id].observe(red_main_bds_location_elapsed_time)

            #Give The Resource Back To The System For Another Marine To Use
            self.main_bds_resource_definition.release(main_bds_request)

        VariablesAndParameters.run_number += 1

model = System()
model.env.process(model.marine_generator())
model.env.run(until=VariablesAndParameters.simulation_time)

for marine in Track.marines:
    print(f"Collected data for Marine {marine.id}:")
    print(Track.monitors[marine.id])
    print()