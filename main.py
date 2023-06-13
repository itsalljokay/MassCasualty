#IMPORTS
import numpy
import simpy
import pandas

class VariablesAndParameters:
    #Sim Details
    warm_up = 0
    number_of_runs = 10
    run_number = 0
    duration_of_simulation_in_minutes = 10
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
            self.color = numpy.random.choice(["Red", "Yellow", "Green", "Black"])

            #DEBUGGING
            print("ID: ", self.id)
            print("Color: ", self.color)
class Track:
    #RED DATA
    red_dataframe = pandas.DataFrame({
        "Time To Main BDS": [],
        "Waiting For Red Doctor": [],
        "With Red Doctor": []
    })
    red_dataframe.index.name = "Marine ID"

    #YELLOW DATA
    yellow_dataframe = pandas.DataFrame({
        "Time To Holding Area": [],
        "Waiting For Yellow Doctor": [],
        "With Yellow Doctor": []
    })
    yellow_dataframe.index.name = "Marine ID"

    #GREEN DATA
    green_dataframe = pandas.DataFrame({
        "Time To Auxillary Treatment Area": [],
        "Waiting For Green Corpsman": [],
        "With Green Corpsman": []
    })
    green_dataframe.index.name = "Marine ID"

    #BLACK DATA
    black_dataframe = pandas.DataFrame({
        "Time To Other Location": [],
        "Waiting For Black Corpsman": [],
        "With Black Corpsman": []
    })
    black_dataframe.index.name = "Marine ID"

class Calculations:
    def get_data():
        all_data = pandas.concat([
            Track.red_dataframe,
            Track.yellow_dataframe,
            Track.green_dataframe,
            Track.black_dataframe
        ], axis=1)

        priority_count = pandas.DataFrame()
        
        all_data.sort_values(by="Marine ID", inplace = True)
        all_data["MEAN"] = all_data.mean(axis=1)
        all_data.loc['MEAN'] = all_data.mean()
        all_data.fillna("", axis="columns", inplace= True)

        print("DEBUGGING:")
        red_priority_total = len(Track.red_dataframe.index)
        yellow_priority_total = len(Track.yellow_dataframe.index)
        green_priority_total = len(Track.green_dataframe.index)
        black_priority_total = len(Track.black_dataframe.index)

        priority_count["Colors"] = ["Red", "Yellow", "Green", "Black"]
        priority_count["Totals"] = [red_priority_total, yellow_priority_total, green_priority_total, black_priority_total]

        return priority_count, all_data
    
    
     
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

    def marine_generator(self):
        while VariablesAndParameters.run_number < VariablesAndParameters.number_of_runs:
            marine = Marine()
            yield self.env.process(self.triage(marine))
    
    def triage(self, marine):
        if marine.color == "Red":
            #MOVE TO MAIN BDS
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
            #Give The Resource Back To The System For Another Marine To Use
            self.main_bds_resource_definition.release(main_bds_request)
            
            #WAIT FOR CARE
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
            
            #ADD TO DATA
            Track.red_dataframe.loc[marine.id] = [red_main_bds_location_elapsed_time, red_doctor_wait_elapsed_time, red_doctor_care_elapsed_time]
        
        if marine.color == "Yellow":
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
            #Give The Resource Back To The System For Another Marine To Use
            self.holding_area_resource_definition.release(holding_area_request)
            
            #WAIT FOR CARE
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

            #ADD TO DATA
            Track.yellow_dataframe.loc[marine.id] = [yellow_holding_area_location_elapsed_time, yellow_doctor_wait_elapsed_time, yellow_doctor_care_elapsed_time]

        if marine.color == "Green":
            #MOVE TO AUXILLARY TREATMENT AREA
            #Start Green Location Timer
            green_aux_treatment_location_timer_start = self.env.now
            print("Green Location Start Time: ", green_aux_treatment_location_timer_start)
            #Request Auxillary Treatment Area Location
            auxillary_treatment_request = self.auxillary_treatment_area_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield auxillary_treatment_request
            #End Green Location Timer
            green_aux_treatment_location_timer_end = self.env.now
            print("Green Location End Time: ", green_aux_treatment_location_timer_end)
            #Calculate Green Location Elapsed Time
            green_aux_treatment_location_elapsed_time = (green_aux_treatment_location_timer_end - green_aux_treatment_location_timer_start)
            print("Green Location Elapsed Time: ", green_aux_treatment_location_elapsed_time)
            #Give The Resource Back To The System For Another Marine To Use
            self.auxillary_treatment_area_resource_definition.release(auxillary_treatment_request)
            
            #WAIT FOR CARE
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

            #ADD TO DATA
            Track.green_dataframe.loc[marine.id] = [green_aux_treatment_location_elapsed_time, green_corpsman_wait_elapsed_time, green_corpsman_care_elapsed_time]
        
        if marine.color == "Black":
            #MOVE TO OTHER LOCATION
            #Start Black Location Timer
            black_other_location_timer_start = self.env.now
            print("Black Location Start Time: ", black_other_location_timer_start)
            #Request Other Location
            other_loc_request = self.other_location_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield other_loc_request
            #End Green Location Timer
            black_other_location_timer_end = self.env.now
            print("Black Location End Time: ", black_other_location_timer_end)
            #Calculate Black Location Elapsed Time
            black_other_location_elapsed_time = (black_other_location_timer_end - black_other_location_timer_start)
            print("Black Location Elapsed Time: ", black_other_location_elapsed_time)
            #Give The Resource Back To The System For Another Marine To Use
            self.other_location_resource_definition.release(other_loc_request)     
            
            #WAIT FOR CARE
            #Start Black Doctor Wait Timer
            black_corpsman_wait_timer_start = self.env.now
            print("Black Corpsman Wait Time Start: ", black_corpsman_wait_timer_start)
            #Request Black Doctor
            black_corpsman_request = self.black_corpsman_resource_definition.request()
            #Wait Until Request Can Be Fulfilled
            yield black_corpsman_request
            #End Black Corpsman Wait Timer
            black_corpsman_wait_timer_end = self.env.now
            print("Black Corpsman Wait End Time: ", black_corpsman_wait_timer_end)
            #Calculate Black Corpsman Wait Time
            black_corpsman_wait_elapsed_time = (black_corpsman_wait_timer_end - black_corpsman_wait_timer_start)
            print("Black Corpsman Elapsed Time: ", black_corpsman_wait_elapsed_time)
            #Give The Resource Back To The System For Another Marine To Use
            self.black_corpsman_resource_definition.release(black_corpsman_request)
            
            #CARE
            #Start Care Timer
            black_corpsman_care_timer_start = self.env.now
            print("Black Care Start Time: ", black_corpsman_care_timer_start)
            #Calculate How Long Care Will Take
            black_care_time = numpy.random.lognormal(VariablesAndParameters.black_mean_corpsman_other_location_consultation, VariablesAndParameters.black_stdev_corpsman_other_location_consultation)
            print("Black Care Calculated Time: ", black_care_time) 
            #Uncommenting will cause system to crash.
            yield self.env.timeout(black_care_time)
            #Stop Care Timer
            black_corpsman_care_timer_end = self.env.now
            print("Black Care Timer End: ", black_corpsman_care_timer_end)
            #Calculate Black Care Time
            black_corpsman_care_elapsed_time = (black_corpsman_care_timer_end - black_corpsman_care_timer_start)
            print("Black Care Elapsed Time: ", black_corpsman_care_elapsed_time)

            #ADD TO DATA
            Track.black_dataframe.loc[marine.id] = [black_other_location_elapsed_time, black_corpsman_wait_elapsed_time, black_corpsman_care_elapsed_time]

        VariablesAndParameters.run_number += 1

model = System()
model.env.process(model.marine_generator())
model.env.run(until=VariablesAndParameters.simulation_time)

print("RED DATAFRAME")
print(Track.red_dataframe)
print("YELLOW DATAFRAME")
print(Track.yellow_dataframe)
print("GREEN DATAFRAME")
print(Track.green_dataframe)
print("BLACK DATAFRAME")
print(Track.black_dataframe)
print("ALL DATA")
print(Calculations.get_data())
