#Mass Casualty Triage Model Aboard A Mercy Class Ship
import numpy
import simpy
import pandas

class VariablesAndParameters:
    number_of_runs = 10
    run_number = 0
    simulation_time = 500
    
    #People Involved
    number_of_red_dedicated_doctors = 5
    number_of_yellow_dedicated_doctors = 3
    number_of_green_dedicated_corpsmen = 239
    number_of_black_dedicated_corpsmen = 239

    #Location Occupancy
    main_bds_maximum_occupancy = 92
    holding_area_maximum_occupancy = 280
    auxillary_treatment_area_maximum_occupancy = 370
    other_location_maximum_occupancy = 270

    #How Long It Takes To Do Things
    red_mean_doctor_main_bds_consultation = 4
    red_stdev_doctor_main_bds_consultation = 1
    yellow_mean_doctor_holding_area_consultation = 3
    yellow_stdev_doctor_holding_area_consultation = 1
    green_mean_corpsman_auxillary_treatment_area_consultation = 2
    green_stdev_corpsman_auxillary_treatment_area_consultation = 1
    black_mean_corpsman_other_location_consultation = 2
    black_stdev_corpsman_other_location_consultation = 1

class Track:
    triage_colors_dictionary = {
        "Red": [],
        "Yellow": [],
        "Green": [],
        "Black": []
    }
    total_triage_colors_dictionary = {
        "Red": [],
        "Yellow": [],
        "Green": [],
        "Black": []
    }
    triage_times_dictionary = {
        "Time To Main Battle Dressing Station": [],
        "Time To Holding Area": [],
        "Time To Auxillary Treatment Area": [],
        "Time To Other Location": [],
        "Waiting For Red Doctor": [],
        "Waiting For Yellow Doctor": [],
        "Waiting For Green Corpsman": [],
        "Waiting For Black Corpsman": [],
        "With Red Dedicated Doctor": [],
        "With Yellow Dedicated Doctor": [],
        "With Green Dedicated Corpsman": [],
        "With Black Dedicated Corpsman": []
    }
    average_triage_times_dictionary = {
        "Time To Main Battle Dressing Station": [],
        "Time To Holding Area": [],
        "Time To Auxillary Treatment Area": [],
        "Time To Other Location": [],
        "Waiting For Red Doctor": [],
        "Waiting For Yellow Doctor": [],
        "Waiting For Green Corpsman": [],
        "Waiting For Black Corpsman": [],
        "With Red Dedicated Doctor": [],
        "With Yellow Dedicated Doctor": [],
        "With Green Dedicated Corpsman": [],
        "With Black Dedicated Corpsman": []
    }
class Marine:
    def __init__(self):
        self.id = VariablesAndParameters.run_number
        self.color = numpy.random.choice(["Red", "Yellow", "Green", "Black"])

        #DEBUGGING
        print("ID: ", self.id)
        print("Color: ", self.color)

class System:
    def __init__(self):
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

    def marine_generator(self):
        while VariablesAndParameters.run_number < VariablesAndParameters.number_of_runs:
            marine = Marine()
            yield self.env.process(self.triage(marine))
    
    
    def triage(self, marine):

        if marine.color == "Red":
            #TRACK TRIAGE COLOR
            Track.triage_colors_dictionary["Red"].append(VariablesAndParameters.run_number)

            #MOVE TO MAIN BDS
            #Start Red Location Timer
            red_main_bds_location_timer_start = self.env.now
            print("Red Location Start Time: ", red_main_bds_location_timer_start)
            #Request Main BDS Location
            main_bds_request = self.main_bds_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield main_bds_request
            #End Red Location Timer
            red_main_bds_location_timer_end = self.env.now
            print("Red Location End Time: ", red_main_bds_location_timer_end)
            #Calculate Red Location Elapsed Time
            red_main_bds_location_elapsed_time = (red_main_bds_location_timer_end - red_main_bds_location_timer_start)
            print("Red Location Elapsed Time: ", red_main_bds_location_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["Time To Main Battle Dressing Station"].append(float(red_main_bds_location_elapsed_time))

            #WAIT FOR RED DOCTOR
            #Start Red Doctor Wait Timer
            red_doctor_wait_timer_start = self.env.now
            print("Red Doc Wait Time Start: ", red_doctor_wait_timer_start)
            #Request Red Doctor
            red_doctor_request = self.red_doctor_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield red_doctor_request
            #End Red Doctor Wait Timer
            red_doctor_wait_timer_end = self.env.now
            print("Red Doc Wait End Time: ", red_doctor_wait_timer_end)
            #Calculate Red Doctor Wait Time
            red_doctor_wait_elapsed_time = (red_doctor_wait_timer_end - red_doctor_wait_timer_start)
            print("Red Doc Elapsed Time: ", red_doctor_wait_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["Waiting For Red Doctor"].append(float(red_doctor_wait_elapsed_time))
            #Give The Resource Back To The System For Another Marine To Use
            self.red_doctor_resource_definition.release(red_doctor_request)

            #CARE
            #Start Care Timer
            red_doctor_care_timer_start = self.env.now
            print("Red Care Start Time: ", red_doctor_care_timer_start)
            #Calculate How Long Care Will Take
            red_care_time = numpy.random.lognormal(VariablesAndParameters.red_mean_doctor_main_bds_consultation, VariablesAndParameters.red_stdev_doctor_main_bds_consultation)
            print("Red Care Calculated Time: ", red_care_time) 
            #Wait That Amount of Care Time
            yield self.env.timeout(red_care_time)
            #Stop Care Timer
            red_doctor_care_timer_end = self.env.now
            print("Red Care Timer End: ", red_doctor_care_timer_end)
            #Calculate Red Care Time
            red_doctor_care_elapsed_time = (red_doctor_care_timer_end - red_doctor_care_timer_start)
            print("Red Care Elapsed Time: ", red_doctor_care_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["With Red Dedicated Doctor"].append(float(red_doctor_care_elapsed_time))
            

        if marine.color == "Yellow":
            #TRACK TRIAGE COLOR
            Track.triage_colors_dictionary["Yellow"].append(VariablesAndParameters.run_number)

            #MOVE TO HOLDING AREA
            #Start Yellow Location Timer
            yellow_holding_area_location_timer_start = self.env.now
            print("Yellow Location Start Time: ", yellow_holding_area_location_timer_start)
            #Request Holding Area Location
            holding_area_request = self.holding_area_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield holding_area_request
            #End Yellow Location Timer
            yellow_holding_area_location_timer_end = self.env.now
            print("Yellow Location End Time: ", yellow_holding_area_location_timer_end)
            #Calculate Yellow Location Elapsed Time
            yellow_holding_area_location_elapsed_time = (yellow_holding_area_location_timer_end - yellow_holding_area_location_timer_start)
            print("Yellow Location Elapsed Time: ", yellow_holding_area_location_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["Time To Holding Area"].append(float(yellow_holding_area_location_elapsed_time))

            #WAIT FOR YELLOW DOCTOR
            #Start Yellow Doctor Wait Timer
            yellow_doctor_wait_timer_start = self.env.now
            print("Yellow Doc Wait Time Start: ", yellow_doctor_wait_timer_start)
            #Request Yellow Doctor
            yellow_doctor_request = self.yellow_doctor_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield yellow_doctor_request
            #End Yellow Doctor Wait Timer
            yellow_doctor_wait_timer_end = self.env.now
            print("Yellow Doc Wait End Time: ", yellow_doctor_wait_timer_end)
            #Calculate Yellow Doctor Wait Time
            yellow_doctor_wait_elapsed_time = (yellow_doctor_wait_timer_end - yellow_doctor_wait_timer_start)
            print("Yellow Doc Elapsed Time: ", yellow_doctor_wait_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["Waiting For Yellow Doctor"].append(float(yellow_doctor_wait_elapsed_time))
            #Give The Resource Back To The System For Another Marine To Use
            self.yellow_doctor_resource_definition.release(yellow_doctor_request)

            #CARE
            #Start Care Timer
            yellow_doctor_care_timer_start = self.env.now
            print("Yellow Care Start Time: ", yellow_doctor_care_timer_start)
            #Calculate How Long Care Will Take
            yellow_care_time = numpy.random.lognormal(VariablesAndParameters.yellow_mean_doctor_holding_area_consultation, VariablesAndParameters.yellow_stdev_doctor_holding_area_consultation)
            print("Yellow Care Calculated Time: ", yellow_care_time) 
            #Wait That Amount of Care Time
            yield self.env.timeout(yellow_care_time)
            #Stop Care Timer
            yellow_doctor_care_timer_end = self.env.now
            print("Yellow Care Timer End: ", yellow_doctor_care_timer_end)
            #Calculate Yellow Care Time
            yellow_doctor_care_elapsed_time = (yellow_doctor_care_timer_end - yellow_doctor_care_timer_start)
            print("Yellow Care Elapsed Time: ", yellow_doctor_care_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["With Yellow Dedicated Doctor"].append(float(yellow_doctor_care_elapsed_time))

        if marine.color == "Green":
            #TRACK TRIAGE COLOR
            Track.triage_colors_dictionary["Green"].append(VariablesAndParameters.run_number)

            #MOVE TO AUXILLARY TREATMENT AREA
            #Start Green Location Timer
            green_auxillary_treatment_area_location_timer_start = self.env.now
            print("Green Location Start Time: ", green_auxillary_treatment_area_location_timer_start)
            #Request Holding Area Location
            auxillary_treatment_area_request = self.holding_area_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield auxillary_treatment_area_request
            #End Green Location Timer
            green_auxillary_treatment_area_location_timer_end = self.env.now
            print("Green Location End Time: ", green_auxillary_treatment_area_location_timer_end)
            #Calculate Green Location Elapsed Time
            green_auxillary_treatment_area_location_elapsed_time = (green_auxillary_treatment_area_location_timer_end - green_auxillary_treatment_area_location_timer_start)
            print("Green Location Elapsed Time: ", green_auxillary_treatment_area_location_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["Time To Auxillary Treatment Area"].append(float(green_auxillary_treatment_area_location_elapsed_time))

            #WAIT FOR GREEN CORPSMAN
            #Start Green Corpsman Wait Timer
            green_corpsman_wait_timer_start = self.env.now
            print("Green Corpsman Wait Time Start: ", green_corpsman_wait_timer_start)
            #Request Green Corpsman
            green_corpsman_request = self.green_corpsman_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield green_corpsman_request
            #End Green Corpsman Wait Timer
            green_corpsman_wait_timer_end = self.env.now
            print("Green Corpsman Wait End Time: ", green_corpsman_wait_timer_end)
            #Calculate Green Corpsman Wait Time
            green_corpsman_wait_elapsed_time = (green_corpsman_wait_timer_end - green_corpsman_wait_timer_start)
            print("Green Corpsman Elapsed Time: ", green_corpsman_wait_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["Waiting For Green Corpsman"].append(float(green_corpsman_wait_elapsed_time))
            #Give The Resource Back To The System For Another Marine To Use
            self.green_corpsman_resource_definition.release(green_corpsman_request)

            #CARE
            #Start Care Timer
            green_corpsman_care_timer_start = self.env.now
            print("Green Care Start Time: ", green_corpsman_care_timer_start)
            #Calculate How Long Care Will Take
            green_care_time = numpy.random.lognormal(VariablesAndParameters.green_mean_corpsman_auxillary_treatment_area_consultation, VariablesAndParameters.green_stdev_corpsman_auxillary_treatment_area_consultation)
            print("Green Care Calculated Time: ", green_care_time) 
            #Wait That Amount of Care Time
            yield self.env.timeout(green_care_time)
            #Stop Care Timer
            green_corpsman_care_timer_end = self.env.now
            print("Green Care Timer End: ", green_corpsman_care_timer_end)
            #Calculate Green Care Time
            green_corpsman_care_elapsed_time = (green_corpsman_care_timer_end - green_corpsman_care_timer_start)
            print("Green Care Elapsed Time: ", green_corpsman_care_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["With Green Dedicated Corpsman"].append(float(green_corpsman_care_elapsed_time))

        if marine.color == "Black":
            #TRACK TRIAGE COLOR
            Track.triage_colors_dictionary["Black"].append(VariablesAndParameters.run_number)

            #MOVE TO OTHER LOCATION
            #Start Black Location Timer
            black_other_location_timer_start = self.env.now
            print("Black Location Start Time: ", black_other_location_timer_start)
            #Request Other Location
            other_location_request = self.other_location_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield other_location_request
            #End Black Location Timer
            black_other_location_timer_end = self.env.now
            print("Black Location End Time: ", black_other_location_timer_end)
            #Calculate Black Location Elapsed Time
            black_other_location_elapsed_time = (black_other_location_timer_end - black_other_location_timer_start)
            print("Black Location Elapsed Time: ", black_other_location_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["Time To Other Location"].append(float(black_other_location_elapsed_time))

            #WAIT FOR BLACK CORPSMAN
            #Start Black Corpsman Wait Timer
            black_corpsman_wait_timer_start = self.env.now
            print("Black Corpsman Wait Time Start: ", black_corpsman_wait_timer_start)
            #Request Black Corpsman
            black_corpsman_request = self.black_corpsman_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield black_corpsman_request
            #End Black Corpsman Wait Timer
            black_corpsman_wait_timer_end = self.env.now
            print("Black Corpsman Wait End Time: ", black_corpsman_wait_timer_end)
            #Calculate Black Corpsman Wait Time
            black_corpsman_wait_elapsed_time = (black_corpsman_wait_timer_end - black_corpsman_wait_timer_start)
            print("Black Corpsman Elapsed Time: ", black_corpsman_wait_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["Waiting For Black Corpsman"].append(float(black_corpsman_wait_elapsed_time))
            #Give The Resource Back To The System For Another Marine To Use
            self.black_corpsman_resource_definition.release(black_corpsman_request)

            #CARE
            #Start Care Timer
            black_corpsman_care_timer_start = self.env.now
            print("Black Care Start Time: ", black_corpsman_care_timer_start)
            #Calculate How Long Care Will Take
            black_care_time = numpy.random.lognormal(VariablesAndParameters.black_mean_corpsman_other_location_consultation, VariablesAndParameters.black_stdev_corpsman_other_location_consultation)
            print("Black Care Calculated Time: ", black_care_time) 
            #Wait That Amount of Care Time
            yield self.env.timeout(black_care_time)
            #Stop Care Timer
            black_corpsman_care_timer_end = self.env.now
            print("Black Care Timer End: ", black_corpsman_care_timer_end)
            #Calculate Black Care Time
            black_corpsman_care_elapsed_time = (black_corpsman_care_timer_end - black_corpsman_care_timer_start)
            print("Black Care Elapsed Time: ", black_corpsman_care_elapsed_time)
            #Add To Data
            Track.triage_times_dictionary["With Black Dedicated Corpsman"].append(float(black_corpsman_care_elapsed_time))
        
        VariablesAndParameters.run_number += 1

class Calculations:
    def total_priority_counts():
        for key, values in Track.triage_colors_dictionary.items():
            Track.total_triage_colors_dictionary[key] = len(values)
        print("Total Triage Colors Dictionary:")
        print(Track.total_triage_colors_dictionary.values())

    def average_times_at_locations():
        for key, values in Track.triage_times_dictionary.items():
            if len(values) > 0:
                Track.average_triage_times_dictionary[key] = sum(values) / len(values)
            else:
                Track.average_triage_times_dictionary[key] = 0
        print("Average Triage Times Dictionary:")
        print(Track.average_triage_times_dictionary.values())

class Conversions:
    def convert_to_dataframe_triage_colors():
        max_length_triage_colors_dictionary = max(len(values) for values in Track.triage_colors_dictionary.values())
        
        padded_triage_colors_dictionary = {}
        for key, values in Track.triage_colors_dictionary.items():
            padding = [""] * (max_length_triage_colors_dictionary - len(values))
            padded_values = values + padding
            padded_triage_colors_dictionary[key] = padded_values
        
        triage_colors_dataframe = pandas.DataFrame.from_dict(padded_triage_colors_dictionary, orient="index")
        print(triage_colors_dataframe)

    def convert_to_dataframe_total_triage_colors():
        """
        We don't have to do the padding here. Why? Because all values are the same for every row.
        """
        total_triage_colors_dataframe = pandas.DataFrame.from_dict(Track.total_triage_colors_dictionary, orient="index")
        print(total_triage_colors_dataframe)
        total_triage_colors_dataframe.to_csv("outputs/total_triage_colors.csv")
        return total_triage_colors_dataframe
    
    def convert_to_dataframe_triage_times():
            max_length_triage_times_dictionary = max(len(values) for values in Track.triage_times_dictionary.values())
            
            padded_triage_times_dictionary = {}
            for key, values in Track.triage_times_dictionary.items():
                padding = [""] * (max_length_triage_times_dictionary - len(values))
                padded_values = values + padding
                padded_triage_times_dictionary[key] = padded_values
            
            triage_times_dataframe = pandas.DataFrame.from_dict(padded_triage_times_dictionary, orient="index")
            print(triage_times_dataframe)

    def convert_to_dataframe_average_triage_times():
        """
        This one is a little different because sometimes when you run the simulation, you could end up with a marine at
        every location, in which case checking for max_length will error out because all values are the same, OR...
        You could not end up with a Marine at every location, and you needed to padd the cell.
        To check this, we first assume we don't need any padding, and calcualte the length of the first key's values to
        serve as our first checking point. From there, if another entry has a different length, then we realize we need
        to padd, and switch our is_padding_needed variable to Yes, or True. Then we break out of this loop to return to
        the other stuff we needed to do, instead of wasting our time and checking all the other lengths, when we already
        know we're gonna need to pad.
        """
        value_lengths = [1] * len(Track.average_triage_times_dictionary)
        max_length = 1

        if len(set(value_lengths)) == 1 and max_length == 1:
            average_triage_times_dataframe = pandas.DataFrame.from_dict(Track.average_triage_times_dictionary, orient="index")
            print(average_triage_times_dataframe)
            average_triage_times_dataframe.to_csv("outputs/average_triage_times.csv")
        else:
            padded_average_triage_times_dictionary = {}
            for key, value in Track.average_triage_times_dictionary.items():
                padded_average_triage_times_dictionary[key] = [value]

            average_triage_times_dataframe = pandas.DataFrame.from_dict(padded_average_triage_times_dictionary, orient="index")
            print(average_triage_times_dataframe)
            average_triage_times_dataframe.to_csv("outputs/average_triage_times.csv")

        return average_triage_times_dataframe

model = System()
model.env.process(model.marine_generator())
model.env.run(until=VariablesAndParameters.simulation_time)

print(Track.triage_colors_dictionary.values())
print(Track.triage_times_dictionary.values())
Calculations.total_priority_counts()
Calculations.average_times_at_locations()
Conversions.convert_to_dataframe_triage_colors()
Conversions.convert_to_dataframe_total_triage_colors()
Conversions.convert_to_dataframe_triage_times()
Conversions.convert_to_dataframe_average_triage_times()