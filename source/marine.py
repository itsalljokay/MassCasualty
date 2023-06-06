
import numpy

# user-defined classes
from variables_and_parameters import VariablesAndParameters
from track import Track

#Class representing...
#A MARINE
class InstanceOfMarine:
    #ID and Time In System
    def __init__(self):
        self.time_in_system_start = 0
        self.id = VariablesAndParameters.marine_counter
        #DEBUGGING
        print("ID: ", self.id)
        print("Start Time In System: ", self.time_in_system_start)

        #Give Them Priority Number and Color
        self.set_priority()
        self.set_triage_color()

        VariablesAndParameters.marine_counter += 1

        #DEBUGGING
        print("Marine Counter: ", VariablesAndParameters.marine_counter)

    #Priority Number To Correspond With Color
    def set_priority(self):
        self.set_priority_number = numpy.random.choice([1, 2, 3, 4])

        #DEBUGGING
        print("Priority Number: ", self.set_priority_number)

    #Priority Color That Corresponds To Priority Number
    def set_triage_color(self):
        if self.set_priority_number == 1:
            self.triage_color = "Red"
            #Add To Data
            if VariablesAndParameters.run_number > VariablesAndParameters.warm_up:
                Track.individual_marines_priority_count_dictionary["Priority 1: Red"].append(self.id)
            
        if self.set_priority_number == 2:
            self.triage_color = "Yellow"
            #Add To Data
            if VariablesAndParameters.run_number > VariablesAndParameters.warm_up:
                Track.individual_marines_priority_count_dictionary["Priority 2: Yellow"].append(self.id)
            
        if self.set_priority_number == 3:
            self.triage_color = "Green"
            #Add To Data
            if VariablesAndParameters.run_number > VariablesAndParameters.warm_up:
                Track.individual_marines_priority_count_dictionary["Priority 3: Green"].append(self.id)
            
        if self.set_priority_number == 4:
            self.triage_color = "Black"
            #Add To Data
            if VariablesAndParameters.run_number > VariablesAndParameters.warm_up:
                Track.individual_marines_priority_count_dictionary["Priority 4: Black"].append(self.id)
                
        #DEBUGGING
        print("Triage Color: ", self.triage_color)