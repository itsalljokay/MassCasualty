#Mass Casualty Triage Model Aboard A Mercy Class Ship
import numpy
import simpy
from simpy import Monitor
import pandas

class VariablesAndParameters:
    number_of_runs = 10
    run_number = 0
    simulation_time = 500
    
    number_of_water_pickup_triage_personnel = 20
    number_of_red_dedicated_doctors = 5
    number_of_yellow_dedicated_doctors = 3
    number_of_green_dedicated_corpsmen = 239
    number_of_black_dedicated_corpsmen = 239

    #Location Occupancy
    main_bds_maximum_occupancy = 92
    holding_area_maximum_occupancy = 280
    auxillary_treatment_area_maximum_occupancy = 370
    other_location_maximum_occupancy = 270

    water_pickup_triage_mean_time = 1.2
    water_pickup_triage_stdev_time = 1

class Track:
    data_dictionary = {
        "Initial Triage": [],
        "Red": [],
        "Yellow": [],
        "Red Time": [],
        "Yellow Time": [],
    }
class Marine:
    def __init__(self):
        self.id = VariablesAndParameters.run_number
        self.color = numpy.random.choice(["Red", "Yellow"])

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
            Track.data_dictionary["Red"].append(VariablesAndParameters.run_number)
            Track.data_dictionary["Red Time"].append(self.time)

        if marine.color == "Yellow":
            yellow_doctor_request = self.yellow_doctor_resource_definition.request()
            yield yellow_doctor_request
            print("You're Yellow")
            self.time = self.env.now
            Track.data_dictionary["Yellow"].append(VariablesAndParameters.run_number)
            Track.data_dictionary["Yellow Time"].append(self.time)

        VariablesAndParameters.run_number += 1

class Conversions:
     def convert_to_dataframe_data():
        max_length_data_dictionary = max(len(values) for values in Track.data_dictionary.values())
        
        padded_data_dictionary = {}
        for key, values in Track.data_dictionary.items():
            padding = [""] * (max_length_data_dictionary - len(values))
            padded_values = values + padding
            padded_data_dictionary[key] = padded_values
        
        data_dataframe = pandas.DataFrame.from_dict(padded_data_dictionary, orient="index")
        print(data_dataframe)


model = System()
model.env.process(model.marine_generator())
model.env.run(until=VariablesAndParameters.simulation_time)

print(Track.data_dictionary.values())
Conversions.convert_to_dataframe_data()