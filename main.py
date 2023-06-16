"""
MASS CASUALTY TRIAGE SIMULATION FOR MERCY-CLASS SHIPS
By: 2ndLt Jessi Lanum

PROBLEM: Mass casualty triage in a Pacific-like environment has not been done in theater since World War II. 
PURPOSE: Support Force Design efforts by demonstrating a framework for mass casualty triage simulations.
OBJECTIVE: Provide quantitative data output and analysis for mass casualty triage situations fielded by Mercy-class ships.

LAST UPDATED: 15 JUN 23
"""

#IMPORTS
"""
Purpose: Import all external packages and libraries we need for this project.
o   OS is to interact with the operating system. We will use it to create folder structure to store our outputs.
    https://docs.python.org/3/library/os.html
o   Numpy is a scientific computing package for math.
    https://numpy.org/
o   Simpy is a discrete event simulation framework.
    https://simpy.readthedocs.io/en/latest/
o   Pandas is a data analysis library.
    https://pandas.pydata.org/
o   Matplotlib is a visualizations library. Specifically, pyplot for 2D graphs in Python.
    https://matplotlib.org/
"""
import os
import numpy
import simpy
import pandas
from matplotlib import pyplot

#FILE STRUCTURE
"""
Purpose: Create the folder structure where we will store our outputs.
"""
#Get Current Working Directory
current_location = os.getcwd()
#All The Folders/Directories We Want To Put Outputs
directories = {
    "outputs",
    "outputs/csv",
    "outputs/graphs"

}
#If That Folder/Directory Doesn't Already Exist, Make It
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

#VARIABLES AND PARAMETERS
"""
Purpose: All the variables and parameters that are needed throughout the program (globally).
"""
class VariablesAndParameters:
    #Sim Details
    warm_up = 1
    number_of_runs = 10
    run_number = 0
    duration_of_simulation_in_minutes = 10
    simulation_time = (duration_of_simulation_in_minutes * 60)
    #A Note On Warm Up Variable:
    #For event simulations, it's important to include some warm-up runs so that the data you glean is as accurate to
    #the real situation as possible. Warmups help eliminate accidental start-up biases. Due to this, data is not collected
    #until after the warmup period has ended.
    
    #A Note On Simulation Duration:
    #This is how long each run will take. Set this accordingly to your scenario. Designed to keep from encountering an
    #accidental "we don't have all day!" type of situation.
    
    #A Note On Simulation Time:
    #Simulation time is technically unitless. This means we pick something and stick to it. For this simulation, seconds
    #have been chosen as it is an appropriate unit of measurement for a combat triage situation. For ease of use, duration
    #entered in minutes will automatically be converted to seconds.
    #Read more here: https://simpy.readthedocs.io/en/latest/topical_guides/environments.html

    #People Involved
    marine_counter = 0
    number_of_red_dedicated_doctors = 281
    number_of_yellow_dedicated_doctors = 260
    number_of_green_dedicated_corpsmen = 239
    number_of_black_dedicated_corpsmen = 239
    #A Note On Marine Counter:
    #We are calculating how many Marines we can handle before resources are swamped or strained. marine_counter keeps track of the number
    #of Marines in the system.

    #A Note On Dedicated Personnel:
    #This can be changed to be more accurate as data is available. Current numbers are gleaned from available Internet sources, and guessing
    #at a best estimate for any data not supplied.
    #https://en.wikipedia.org/wiki/USNS_Mercy
    #https://www.msc.usff.navy.mil/Ships/Mercy/Statistics/

    #Location Occupancy
    main_bds_maximum_occupancy = 92
    holding_area_maximum_occupancy = 280
    auxillary_treatment_area_maximum_occupancy = 370
    other_location_maximum_occupancy = 270
    #A Note On Occupancy:
    #See note on Dedicated Personnel.

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
    #A Note On Durations
    #A lognormal distribution is utilized in this simulation as it provides a normal distribution of a random variable with only positive
    #real numbers. A lognormal sample calculator was used to come up with best guess for duration of care times for each priority color.
    #Lognormal Calculator: https://www.omnicalculator.com/statistics/lognormal-distribution
    #More on lognormal distributions: https://en.wikipedia.org/wiki/Log-normal_distribution 

#MARINE INSTANCE
"""
Purpose: Detail the entity of a Marine for the simulation.
"""
class Marine:
        #Initialization. Will Occur Every Time Simulation Runs.
        def __init__(self):
            self.id = VariablesAndParameters.run_number
            self.color = numpy.random.choice(["Red", "Yellow", "Green", "Black"])
            #A Note On ID and Color:
            #Every Marine in the system recieves a unique ID that corresponds to the simulation run number. Marine 0 is the Marine triaged
            #during simulation 0, Marine 1 is the Marine triaged on simulation 1, etc. Each Marine also recieves a randomized color which
            #corresponds to their triage color code. This color coding corresponds to standard mass casualty triage color coding.
            #More on Mass Casualty Triage Color Code: https://www.ncbi.nlm.nih.gov/books/NBK459369/
            
            #Output
            print("ID: ", self.id)
            print("Color: ", self.color)

#DATA TRACKING
"""
Purpose: Track data as the simulation runs.
"""
class Track:
    #RED DATA
    red_dataframe = pandas.DataFrame({
        "Time To Main Battle Dressing Station": [],
        "Waiting For Red Doctor": [],
        "Time With Red Doctor": []
    })
    red_dataframe.index.name = "Marine ID"

    #YELLOW DATA
    yellow_dataframe = pandas.DataFrame({
        "Time To Holding Area": [],
        "Waiting For Yellow Doctor": [],
        "Time With Yellow Doctor": []
    })
    yellow_dataframe.index.name = "Marine ID"

    #GREEN DATA
    green_dataframe = pandas.DataFrame({
        "Time To Auxillary Holding Area": [],
        "Waiting For Green Corpsman": [],
        "Time With Green Corpsman": []
    })
    green_dataframe.index.name = "Marine ID"

    #BLACK DATA
    black_dataframe = pandas.DataFrame({
        "Time To Other Location": [],
        "Waiting For Black Corpsman": [],
        "Time With Black Corpsman": []
    })
    black_dataframe.index.name = "Marine ID"

    #SIMPLIFIED DATA
    simplified_dataframe = pandas.DataFrame({
        "Triage Color": [],
        "Time To Location": [],
        "Waiting For Care": [],
        "Care Time": []
    })
    simplified_dataframe.index.name = "Marine ID"
    #A Note on Simplified Data:
    #In the Simplified Dataframe every Marine is tracked. You will notice that the specific location or care personnel details are ommitted
    #in favor of the universal "Time to Location", "Waiting For Care", or "Care Time" categories. The data here will be the same as the data
    #logged in the corresponding color dataframe, but makes for easier calculations and visualization of full data later on.

#DATA CALCULATIONS
"""
Purpose: Conduct calculations on collected data.
"""
class Calculations:
    #DATAFRAMES
    #Pull in our tracked data and save it to a new dataframe to keep from overwriting.
    red_averages = Track.red_dataframe
    yellow_averages = Track.yellow_dataframe
    green_averages = Track.green_dataframe
    black_averages = Track.black_dataframe
    all_averages = Track.simplified_dataframe
    overall_averages = Track.simplified_dataframe
    priority_count = pandas.DataFrame()

    def get_data():
        #FIND AVERAGES
        Calculations.red_averages["MEAN"] = Calculations.red_averages.mean(axis=1)
        Calculations.red_averages.loc["MEAN"] = Calculations.red_averages.mean()
        Calculations.red_averages.to_csv("outputs/csv/red_averages_seperate.csv")

        Calculations.yellow_averages["MEAN"] = Calculations.yellow_averages.mean(axis=1)
        Calculations.yellow_averages.loc["MEAN"] = Calculations.yellow_averages.mean()
        Calculations.yellow_averages.to_csv("outputs/csv/yellow_averages_seperate.csv")

        Calculations.green_averages["MEAN"] = Calculations.green_averages.mean(axis=1)
        Calculations.green_averages.loc["MEAN"] = Calculations.green_averages.mean()
        Calculations.green_averages.to_csv("outputs/csv/green_averages_seperate.csv")

        Calculations.black_averages["MEAN"] = Calculations.black_averages.mean(axis=1)
        Calculations.black_averages.loc["MEAN"] = Calculations.black_averages.mean()
        Calculations.black_averages.to_csv("outputs/csv/black_averages_seperate.csv")

        #BY COLOR
        #"The average [TRIAGE COLOR] Marine spends this amount of time..."
        Calculations.all_averages = Calculations.all_averages.groupby("Triage Color").mean()
        Calculations.all_averages.to_csv("outputs/csv/average_by_triage_color.csv")
    
        #REGARDLESS OF COLOR
        #"The average Marine regardless of triage color spends this amount of time..."
        Calculations.overall_averages["MEAN"] = Calculations.overall_averages.mean(axis=1, numeric_only=True)
        Calculations.overall_averages.loc["MEAN"] = Calculations.overall_averages.mean(numeric_only=True)
        Calculations.overall_averages.to_csv("outputs/csv/average_regardless_of_triage_color.csv")

        #PRIORITY COUNTS
        #"There were x number of Red Marines, x number of Yellow Marines, etc..."
        red_priority_total = len(Track.red_dataframe.index)
        yellow_priority_total = len(Track.yellow_dataframe.index)
        green_priority_total = len(Track.green_dataframe.index)
        black_priority_total = len(Track.black_dataframe.index)
        Calculations.priority_count["Colors"] = ["Red", "Yellow", "Green", "Black"]
        Calculations.priority_count["Totals"] = [red_priority_total, yellow_priority_total, green_priority_total, black_priority_total]
        Calculations.priority_count.to_csv("outputs/csv/priority_count.csv")  

        return Calculations.red_averages, Calculations.yellow_averages, Calculations.green_averages, Calculations.black_averages, Calculations.overall_averages, Calculations.priority_count, Calculations.all_averages

#GRAPHING DATA
"""
Purpose: Design and print graphs of our collected and calculated data.
"""
class Graph:
    #Graph for Priority Totals
    def priority_totals_graph():
        #Set Graph Details
        priority_count = Calculations.priority_count
        fig, ax = pyplot.subplots()
        x_labels = ["Red", "Yellow", "Green", "Black"]
        values = priority_count["Totals"].values.tolist()
        bar_colors = ["red", "yellow", "green", "blue"]
        filename = "priority_counts.png"

        #Set Design Options
        bars = ax.bar(x_labels, values, color=bar_colors)
        ax.set_ylabel("Number of Marines")
        ax.set_title("Priority Counts")
        
        #Annotate Each Bar With Its Value
        for bar in bars:
            height = bar.get_height()
            height = bar.get_height()
            x = bar.get_x()
            width = bar.get_width()
            ax.annotate(height,
                        xy=(x + width / 2, height / 2),  # Position annotation in the middle of the bar body
                        xytext=(0, 0),  # No offset for text position
                        textcoords="offset points",
                        ha='center', va='center')

        #Save Graph
        pyplot.savefig("outputs/graphs/"+filename)

    #Graph for Experience By Individual Marine (Every Color Present)
    def experience_by_individual_marine_graph():
        #Set Graph Details
        filename = "experience_by_individual.png"
        fig, ax1 = pyplot.subplots()
        ax2 = ax1.twinx()
        time_categories = ["Time To Location", "Waiting For Care", "Care Time"]
        y_positions = numpy.arange(len(time_categories))
        annotated_positions = set()
        color_mapping = {
            "Red": "red",
            "Yellow": "yellow",
            "Green": "green",
            "Black": "black"
        }

        #Specifying Graph Design
        for row in Track.simplified_dataframe.iterrows():
            triage_color = row[1]["Triage Color"]
            time_values = [row[1][category] for category in time_categories]
            
            #Check For NaN Values In triage_color Or time_values
            if pandas.isna(triage_color) or any(pandas.isna(time_values)):
                continue  #Skip if value is NaN
            
            #Plot The Dots
            ax1.plot(time_categories, time_values, marker="o", color=color_mapping.get(triage_color, "black"))
            
            #Connect The Dots With Lines
            ax1.plot(time_categories, time_values, color=color_mapping.get(triage_color, "black"))
            
            #Add Value Annotation For Each Dot Except Last One (Care Time)
            for i in range(len(time_categories) - 1):
                x_pos = time_categories[i]
                y_pos = time_values[i]
                value = f"{y_pos:.2f}"
                
                #Check If Position Is Already Annotated
                if (x_pos, y_pos) in annotated_positions:
                    continue
                #Annotate
                ax1.annotate(value, (x_pos, y_pos), textcoords="offset points", xytext=(0, 10), ha="center")
                annotated_positions.add((x_pos, y_pos))
                #A Note On Value Annotations:
                #This can be adjusted if the graph gets overcrowded. During intial testing Care Time quickly became over saturated with values.
        
        #Set More Graph Details
        ax1.set_xlabel("Triage Color")
        ax1.set_ylabel("Time (Minutes)")
        ax2.set_ylabel("Time (Minutes)")
        ax1.set_title("Experience By Individual Marine")
        ax1.set_xticks(y_positions)
        ax1.set_xticklabels(time_categories)

        #Set The Desired Number of Intervals And Interval Size For Y-Axis
        num_intervals = 10
        interval_size = 5

        #Set Y-Axis Ticks And Labels For Both Left And Right Y-Axes
        y_ticks = numpy.arange(0, num_intervals * interval_size + interval_size, interval_size)
        ax1.set_yticks(y_ticks)
        ax2.set_yticks(y_ticks)
        ax1.set_yticklabels(y_ticks)
        ax2.set_yticklabels(y_ticks)
        
        #Save Graph
        pyplot.savefig("outputs/graphs/"+filename)

    #Graph For Average Experience By Triage Color
    def average_experience_by_triage_color():
        #Set Graph Details
        filename = "average_experience_by_triage_color.png"
        fig, ax1 = pyplot.subplots()
        ax2 = ax1.twinx()
        time_categories = ["Time To Location", "Waiting For Care", "Care Time"]
        y_positions = numpy.arange(len(time_categories))
        annotated_positions = set()
        color_mapping = {
            "Red": "red",
            "Yellow": "yellow",
            "Green": "green",
            "Black": "black"
        }

        #Specifying Graph Design
        for triage_color, row in Calculations.all_averages.iterrows():
            time_values = row[time_categories]
            
            #Check For NaN Values In time_values
            if any(pandas.isna(time_values)):
                continue  #Skip if value is NaN
            
            #Plot The Dots
            ax1.plot(time_categories, time_values, marker="o", color=color_mapping.get(triage_color, "black"))
            
            #Connect The Dots With Lines
            ax1.plot(time_categories, time_values, color=color_mapping.get(triage_color, "black"))
            
            #Add Value Annotation For Each Dot Except Last One (Care Time)
            for i in range(len(time_categories) - 1):
                x_pos = time_categories[i]
                y_pos = time_values[i]
                value = f"{y_pos:.2f}"
                
                #Check If Position Is Already Annotated
                if (x_pos, y_pos) in annotated_positions:
                    continue
                #Annotate
                ax1.annotate(value, (x_pos, y_pos), textcoords="offset points", xytext=(0, 10), ha="center")
                annotated_positions.add((x_pos, y_pos))

        #Set More Graph Details
        ax1.set_xlabel("Triage Color")
        ax1.set_ylabel("Time (Minutes)")
        ax2.set_ylabel("Time (Minutes)")
        ax1.set_title("Average Marine Experience by Triage Color")
        ax1.set_xticks(y_positions)
        ax1.set_xticklabels(time_categories)

        #Set The Desired Number of Intervals And Interval Size For Y-Axis
        num_intervals = 10
        interval_size = 5

        #Set Y-Axis Ticks And Labels For Both Left And Right Y-Axes
        y_ticks = numpy.arange(0, num_intervals * interval_size + interval_size, interval_size)
        ax1.set_yticks(y_ticks)
        ax2.set_yticks(y_ticks)
        ax1.set_yticklabels(y_ticks)
        ax2.set_yticklabels(y_ticks)
        
        #Save Graph
        pyplot.savefig("outputs/graphs/"+filename)

    #Graph For Average Experience Regardless of Triage Color
    def average_experience_regardless_of_color():
        #Set Graph Details
        filename = "average_experience_regardless_of_color.png"
        fig, ax1 = pyplot.subplots()
        ax2 = ax1.twinx()
        time_categories = ["Time To Location", "Waiting For Care", "Care Time"]
        y_positions = numpy.arange(len(time_categories))
        overall_average = Calculations.overall_averages.loc["MEAN", time_categories]

        #Plot Data
        ax1.plot(time_categories, overall_average, marker="o", color="black")
        ax1.plot(time_categories, overall_average, color="black")

        #Set More Graph Details
        ax1.set_xlabel("Average Marine Regardless of Triage Color")
        ax1.set_ylabel("Time (Minutes)")
        ax2.set_ylabel("Time (Minutes)")
        ax1.set_title("Average Marine Experience Regardless of Triage Color")
        ax1.set_xticks(y_positions)
        ax1.set_xticklabels(time_categories)

        #Set The Desired Number of Intervals And Interval Size For Y-Axis
        num_intervals = 10
        interval_size = 5

        #Set Y-Axis Ticks And Labels For Both Left And Right Y-Axes
        y_ticks = numpy.arange(0, num_intervals * interval_size + interval_size, interval_size)
        ax1.set_yticks(y_ticks)
        ax2.set_yticks(y_ticks)
        ax1.set_yticklabels(y_ticks)
        ax2.set_yticklabels(y_ticks)

        #Add Value Annotations For Each Dot
        for i in range(len(time_categories)):
            x_pos = time_categories[i]
            y_pos = overall_average[i]
            value = f"{y_pos:.2f}"
            ax1.annotate(value, (x_pos, y_pos), textcoords="offset points", xytext=(0, 10), ha="center")

        #Save Graph
        pyplot.savefig("outputs/graphs/"+filename)

#SIMULATION SYSTEM
"""
Purpose: Detailing the triage process.
"""
class System:
    #Initialization. Will Occur Every Time Simulation Runs.
    def __init__(self):
        #Initialize Environment
        self.env = simpy.Environment()

        #Define Our Simulation Resources
        #People
        self.red_doctor_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.number_of_red_dedicated_doctors)
        self.yellow_doctor_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.number_of_yellow_dedicated_doctors)
        self.green_corpsman_resource_definition = simpy.Resource(self.env, capacity = VariablesAndParameters.number_of_green_dedicated_corpsmen)
        self.black_corpsman_resource_definition = simpy.Resource(self.env, capacity = VariablesAndParameters.number_of_black_dedicated_corpsmen)
        #A Note On PriorityResource vs. Resource
        #Red and Yellow care personnel are marked as Priority as Red and Yellow triage colored Marines take priority.

        #Locations
        self.main_bds_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.main_bds_maximum_occupancy)
        self.holding_area_resource_definition = simpy.PriorityResource(self.env, capacity = VariablesAndParameters.holding_area_maximum_occupancy)
        self.auxillary_treatment_area_resource_definition = simpy.Resource(self.env, capacity = VariablesAndParameters.auxillary_treatment_area_maximum_occupancy)
        self.other_location_resource_definition = simpy.Resource(self.env, capacity = VariablesAndParameters.other_location_maximum_occupancy)

    #Creates A Marine And Starts Triage Process
    def marine_generator(self):
        while VariablesAndParameters.run_number < VariablesAndParameters.number_of_runs:
            marine = Marine()
            yield self.env.process(self.triage(marine))
    
    #Triage Process
    def triage(self, marine):
        #RED TRIAGE PROCESS
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
            if VariablesAndParameters.run_number > VariablesAndParameters.warm_up:
                Track.red_dataframe.loc[marine.id] = [red_main_bds_location_elapsed_time, red_doctor_wait_elapsed_time, red_doctor_care_elapsed_time]
                Track.simplified_dataframe.loc[marine.id] = [marine.color, red_main_bds_location_elapsed_time, red_doctor_wait_elapsed_time, red_doctor_care_elapsed_time]
        
        #YELLOW TRIAGE PROCESS
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
            if VariablesAndParameters.run_number > VariablesAndParameters.warm_up:
                Track.yellow_dataframe.loc[marine.id] = [yellow_holding_area_location_elapsed_time, yellow_doctor_wait_elapsed_time, yellow_doctor_care_elapsed_time]
                Track.simplified_dataframe.loc[marine.id] = [marine.color, yellow_holding_area_location_elapsed_time, yellow_doctor_wait_elapsed_time, yellow_doctor_care_elapsed_time]

        #GREEN TRIAGE PROCESS
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
            if VariablesAndParameters.run_number > VariablesAndParameters.warm_up:
                Track.green_dataframe.loc[marine.id] = [green_aux_treatment_location_elapsed_time, green_corpsman_wait_elapsed_time, green_corpsman_care_elapsed_time]
                Track.simplified_dataframe.loc[marine.id] = [marine.color, green_aux_treatment_location_elapsed_time, green_corpsman_wait_elapsed_time, green_corpsman_care_elapsed_time]

        #BLACK
        #TRIAGE PROCESS
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
            if VariablesAndParameters.run_number > VariablesAndParameters.warm_up:
                Track.black_dataframe.loc[marine.id] = [black_other_location_elapsed_time, black_corpsman_wait_elapsed_time, black_corpsman_care_elapsed_time]
                Track.simplified_dataframe.loc[marine.id] = [marine.color, black_other_location_elapsed_time, black_corpsman_wait_elapsed_time, black_corpsman_care_elapsed_time]

        VariablesAndParameters.run_number += 1

#RUNNING THE MODEL
model = System()
model.env.process(model.marine_generator())
model.env.run(until=VariablesAndParameters.simulation_time)

#OUTPUTTING DATA
print("RED DATAFRAME")
print(Track.red_dataframe)
print("YELLOW DATAFRAME")
print(Track.yellow_dataframe)
print("GREEN DATAFRAME")
print(Track.green_dataframe)
print("BLACK DATAFRAME")
print(Track.black_dataframe)
print("ALL DATA")
print(Track.simplified_dataframe)

#OUTPUTTING CALCULATED DATA
print(Calculations.get_data())

#OUTPUTTING GRAPHS
Graph.priority_totals_graph()
Graph.experience_by_individual_marine_graph()
Graph.average_experience_by_triage_color()
Graph.average_experience_regardless_of_color()