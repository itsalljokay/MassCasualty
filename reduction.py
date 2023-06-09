import numpy
import simpy
import pandas

class Variables:
    number_of_runs = 10
    run_number = 0
    simulation_time = 100
    
    number_of_water_pickup_triage_personnel = 20
    number_of_red_dedicated_doctors = 5
    number_of_yellow_dedicated_doctors = 3

class Track:
    data_dictionary = {
        "Initial": [],
        "Red": [],
        "Yellow": [],
        "Red Time": [],
        "Yellow Time": [],
    }
class Marine:
    def __init__(self):
        self.id = Variables.run_number
        self.color = numpy.random.choice(["Red", "Yellow"])

        #DEBUGGING
        print("ID: ", self.id)
        print("Color: ", self.color)

class System:
    def __init__(self):
        self.env = simpy.Environment()
        #Define Our Simulation Resources
        #People
        self.initial_triage_resource_definition = simpy.PriorityResource(self.env, capacity = Variables.number_of_water_pickup_triage_personnel)
        self.red_doctor_resource_definition = simpy.PriorityResource(self.env, capacity = Variables.number_of_red_dedicated_doctors)
        self.yellow_doctor_resource_definition = simpy.PriorityResource(self.env, capacity = Variables.number_of_yellow_dedicated_doctors)

    def marine_generator(self):
        while Variables.run_number < Variables.number_of_runs:
            marine = Marine()
            yield self.env.process(self.triage(marine))
    
    
    def triage(self, marine):
        #Request Initial Triage/Water Pickup
        
        self.initial_request = self.initial_triage_resource_definition.request()
        yield self.initial_request
        self.triage_time = self.env.now
        Track.data_dictionary["Initial"].append(self.triage_time)
        
        if marine.color == "Red":
            red_doctor_request = self.red_doctor_resource_definition.request()
            yield red_doctor_request
            print("You're Red")
            self.time = self.env.now
            Track.data_dictionary["Red"].append(Variables.run_number)
            Track.data_dictionary["Red Time"].append(self.time)

        if marine.color == "Yellow":
            yellow_doctor_request = self.yellow_doctor_resource_definition.request()
            yield yellow_doctor_request
            print("You're Yellow")
            self.time = self.env.now
            Track.data_dictionary["Yellow"].append(Variables.run_number)
            Track.data_dictionary["Yellow Time"].append(self.time)

        Variables.run_number += 1

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
model.env.run(until=Variables.simulation_time)

print(Track.data_dictionary.values())
Conversions.convert_to_dataframe_data()