#IMPORTS
import numpy
import simpy
import pandas

class VariablesAndParameters:
    #Sim Details
    warm_up = 0
    number_of_runs = 10
    run_number = 0
    duration_of_simulation_in_minutes = 5
    simulation_time = (duration_of_simulation_in_minutes * 60)
    #SIMULATION TIME IS IN SECONDS

    #People Involved
    #We are calculating how many Marines we can handle before resources are swamped or strained. Therefore, marine_counter starts and stays at 0.
    marine_counter = 0
    number_of_red_dedicated_doctors = 281
    number_of_yellow_dedicated_doctors = 260
    number_of_green_dedicated_corpsmen = 239
    number_of_black_dedicated_corpsmen = 239

    #Location Occupancy
    main_bds_maximum_occupancy = 92
    holding_area_maximum_occupancy = 280
    auxillary_treatment_area_maximum_occupancy = 370
    other_location_maximum_occupancy = 270

    #How Long It Takes To Do Things
    #Gonna want to mess around with a lognormal calculator and see what some acceptable samples could be.
    red_mean_doctor_main_bds_consultation = 4
    red_stdev_doctor_main_bds_consultation = 1
    yellow_mean_doctor_holding_area_consultation = 3
    yellow_stdev_doctor_holding_area_consultation = 1
    green_mean_corpsman_auxillary_treatment_area_consultation = 2
    green_stdev_corpsman_auxillary_treatment_area_consultation = 1
    black_mean_corpsman_other_location_consultation = 2
    black_stdev_corpsman_other_location_consultation = 1

class Marine:
        def __init__(self):
            self.id = VariablesAndParameters.run_number
            self.color = numpy.random.choice(["Red", "Yellow"])

            #DEBUGGING
            print("ID: ", self.id)
            print("Color: ", self.color)
class Track:
    def data(self):
        marines = []
        time_to_main_battle_dressing_station = []
        time_to_holding_area = []
        time_to_auxillary_treatment_area = []
        time_to_other_location = []
        waiting_for_red_doctor = []
        waiting_for_yellow_doctor = []
        waiting_for_green_corpsman = []
        waiting_for_black_corpsman = []

class System:
    def __init__(self):
        #Initialize Environment
        self.env = simpy.Environment()

        #Define Our Simulation Resources
        #People
        self.red_doctor_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.number_of_red_dedicated_doctors)
        self.yellow_doctor_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.number_of_yellow_dedicated_doctors)
        self.green_corpsman_resource_definition = simpy.Resource(self.env, capacity = VariablesAndParameters.number_of_green_dedicated_corpsmen)
        self.black_corpsman_resource_definition = simpy.Resource(self.env, capacity = VariablesAndParameters.number_of_black_dedicated_corpsmen)

        #Locations
        self.main_bds_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.main_bds_maximum_occupancy)
        self.holding_area_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.holding_area_maximum_occupancy)
        self.auxillary_treatment_area_resource_definition = simpy.Resource(self.env, capacity = VariablesAndParameters.auxillary_treatment_area_maximum_occupancy)
        self.other_location_resource_definition = simpy.Resource(self.env, capacity = VariablesAndParameters.other_location_maximum_occupancy)

        #Locations
        self.main_bds_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.main_bds_maximum_occupancy)

    def marine_generator(self):
        while VariablesAndParameters.run_number < VariablesAndParameters.number_of_runs:
            marine = Marine()
            yield self.env.process(self.triage(marine))
    
    def triage(self, marine):
        if marine.color == "Red":
            red_doctor_request = self.red_doctor_resource_definition.request()
            yield red_doctor_request
            print("You're Red")
            self.time = self.env.now

model = System()
model.env.process(model.marine_generator())
model.env.run(until=VariablesAndParameters.simulation_time)