import numpy
import simpy
import pandas

class Variables:
    number_of_mres = 5
    marines_present = 0
    marines_total = 10
    marine_counter = 0

    simulation_time = 10

class Track:
    data_dictionary = {
        "MRE": [],
        "No MRE": [],
        "MRE Status": [],
        "No MRE Status": [],
    }
class Marine:
    def __init__(self):
        self.id = Variables.marine_counter
        self.color = numpy.random.choice(["Red", "Blue"])

        #DEBUGGING
        print("ID: ", self.id)
        print("Color: ", self.color)

class System:
    def __init__(self):
        self.env = simpy.Environment()
        #Define Our Simulation Resources
        #People
        self.mre_resource_definition = simpy.PriorityResource(self.env, capacity = Variables.number_of_mres)

    def marine_generator(self):
        while Variables.marines_present < Variables.marines_total:
            marine = Marine()
            yield self.env.process(self.mre_handout(marine))
    
    
    def mre_handout(self, marine):
        mre_request = self.mre_resource_definition.request()
        if marine.color == "Red":
            yield mre_request
            print("You Got an MRE")
            self.mre_status = self.env.now
            Track.data_dictionary["MRE"].append(Variables.marine_counter)
            Track.data_dictionary["MRE Status"].append(self.mre_status)

        if marine.color == "Blue":
            print("Too bad!")
            self.mre_status = self.env.now
            Track.data_dictionary["No MRE"].append(Variables.marine_counter)
            Track.data_dictionary["No MRE Status"].append(self.mre_status)

        Variables.marine_counter += 1

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