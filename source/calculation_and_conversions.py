
import pandas
from matplotlib import pyplot

# user-defined classes
from track import Track

#Class representing...
#CALCULATIONS
#The putting together the outputs of the gonkulator.
class CalculationsAndConversions:
    def total_priority_counts():
        for key, values in Track.individual_marines_priority_count_dictionary.items():
            Track.total_priority_count_dictionary[key] = len(values)
        print("Total Priority Count Dictionary:")
        print(Track.total_priority_count_dictionary.values())

    def average_times_at_locations():
        for key, values in Track.individual_times_at_locations_dictionary.items():
            if len(values) > 0:
                Track.average_times_at_locations_dictionary[key] = sum(values) / len(values)
            else:
                Track.average_times_at_locations_dictionary[key] = 0
        print("Average Time At Location Dictionary:")
        print(Track.average_times_at_locations_dictionary.values())

    def convert_to_dataframe_individual_marines_priority_count():
        """
        Converting our Dictionaries to Pandas Dataframes
        Here we are converting our dictionaries we used during the simulation to Pandas dataframes for easy output and plotting later.
        Pandas dataframes don't just automatically fill in any empty cells if there isn't any values there like Excel does.
        So, if there are 17 Red priority Marines, and only 4 Yellow Priority Marines, we need to fill in the remaining values
        on the Yellow Priority Marines rows with designated empty values, else the dataframe will freak and not work.
        """
        #INDIVIDUAL MARINES PRIORITY COUNT DICTIONARY
        #Step 1: Find the longest entry.
        max_length_individual_marines_priority_count_dictionary = max(len(values) for values in Track.individual_marines_priority_count_dictionary.values())
        """
        for entry in Track.individual_marines_priority_count_dictionary:
            max_length_individual_marines_priority_count_dictionary = max(len(entry))
        """
        #Step 2: Padd the list with any extra values to make all entries of equal length.
        """
        Here, we are making a new dictionary to include the padded (empty) cells.
        Then for every key and value pair in our unpadded dictionary, we add an empty cell.
        [] * (max_length... - len(values)) says add an empty cell ([]) for however many cells we have between the largest entry in the dictionary 
        and how many we actually have.
        Then we go ahead and add the values plus our new padding into the dictionary.
        """
        padded_individual_marines_priority_count_dictionary = {}
        for key, values in Track.individual_marines_priority_count_dictionary.items():
            padding = [] * (max_length_individual_marines_priority_count_dictionary - len(values))
            padded_values = values + padding
            padded_individual_marines_priority_count_dictionary[key] = padded_values
        #Step 3: Convert to Pandas Dataframe
        individual_marines_priority_count_dataframe = pandas.DataFrame.from_dict(padded_individual_marines_priority_count_dictionary, orient="index")
        print(individual_marines_priority_count_dataframe)
        #Step 4: Output Dataframe as a CSV for future use.
        individual_marines_priority_count_dataframe.to_csv("individual_marines_priority_count.csv")
        return individual_marines_priority_count_dataframe

    def convert_to_dataframe_total_priority_count():
        """
        We don't have to do the padding here. Why? Because all values are the same for every row.
        """
        total_marines_priority_count_dataframe = pandas.DataFrame.from_dict(Track.total_priority_count_dictionary, orient="index")
        print(total_marines_priority_count_dataframe)
        total_marines_priority_count_dataframe.to_csv("total_marines_priority_count.csv")
        return total_marines_priority_count_dataframe

    def convert_to_dataframe_individual_times_at_locations():
        max_length_individual_times_at_locations_dictionary = max(len(values) for values in Track.individual_times_at_locations_dictionary.values())
        
        padded_individual_times_at_locations_dictionary = {}
        for key, values in Track.individual_times_at_locations_dictionary.items():
            padding = [] * (max_length_individual_times_at_locations_dictionary - len(values))
            padded_values = values + padding
            padded_individual_times_at_locations_dictionary[key] = padded_values
        
        individual_times_at_locations_dataframe = pandas.DataFrame.from_dict(padded_individual_times_at_locations_dictionary, orient="index")
        print(individual_times_at_locations_dataframe)
        individual_times_at_locations_dataframe.to_csv("individual_times_at_locations.csv")
        return individual_times_at_locations_dataframe

    def convert_to_dataframe_average_times_at_locations():
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
        value_lengths = [1] * len(Track.average_times_at_locations_dictionary)
        max_length = 1

        if len(set(value_lengths)) == 1 and max_length == 1:
            average_times_at_locations_dataframe = pandas.DataFrame.from_dict(Track.average_times_at_locations_dictionary, orient="index")
            print(average_times_at_locations_dataframe)
            average_times_at_locations_dataframe.to_csv("average_times_at_locations.csv")
        else:
            max_length_average_times_at_locations_dictionary = max_length
    
            padded_average_times_at_locations_dictionary = {}
            for key, value in Track.average_times_at_locations_dictionary.items():
                padded_average_times_at_locations_dictionary[key] = [value]

            average_times_at_locations_dataframe = pandas.DataFrame.from_dict(padded_average_times_at_locations_dictionary, orient="index")
            print(average_times_at_locations_dataframe)
            average_times_at_locations_dataframe.to_csv("average_times_at_locations.csv")

        return average_times_at_locations_dataframe

    def plot_and_save_graph(dataframe, title, plot_type, image_filename):
        if plot_type == "chart":
            dataframe.plot()
        elif plot_type == "histogram":
            dataframe.hist()
        elif plot_type == "pie":
            dataframe.plot(kind="pie", subplots=True, legend=False)
        elif plot_type == "scatter":
            for idx, row in dataframe.iterrows():
                pyplot.scatter([idx] * len(row), row)
        else:
            print("Invalid plot type!")
        
        pyplot.title(title)
        pyplot.savefig(image_filename)