#IMPORTS
from scipy.stats import lognorm

# user-defined classes
from calculation_and_conversions import CalculationsAndConversions
from track import Track
from MassCasualtySystem.Mass_Casualty_System import MassCasualtySystem
from variables_and_parameters import VariablesAndParameters
     
#RUNNING THE SYSTEM
model = MassCasualtySystem()
model.env.process(model.pickup_and_care_procedures())
model.env.run(until=VariablesAndParameters.simulation_time)

#APPLYING CALCULATIONS AND CONVERSIONS AND THEN GRAPHING EVERYTHING
CalculationsAndConversions.total_priority_counts()
CalculationsAndConversions.average_times_at_locations()
"""
Here we're going to create a dictionary with the names of each dataframe as well
the function we wrote earlier to actually create the dataframe. This allows us to not
only convert our tracking dictionaries to dataframes, but also creates an easy way to
pass those dataframes to matplotlib for graphing.
"""
dataframes = {
    "Individual Priority Counts By ID": (CalculationsAndConversions.convert_to_dataframe_individual_marines_priority_count, "chart", "individual_marines_priority_count.png"),
    "Total Priority Counts": (CalculationsAndConversions.convert_to_dataframe_total_priority_count, "bar", "total_priority_count.png"),
    "Individual Times at Locations by ID": (CalculationsAndConversions.convert_to_dataframe_individual_times_at_locations, "scatter", "individual_times_at_locations.png"),
    "Average Times at Locations": (CalculationsAndConversions.convert_to_dataframe_average_times_at_locations, "bar","average_times_at_locations.png")
}

for title, (function, plot_type, image_filename) in dataframes.items():
    print(title)
    dataframe = function()
    # CalculationsAndConversions.plot_and_save_graph(dataframe, title, plot_type, image_filename)