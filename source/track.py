#Class representing...
#DATA
#Where we put data as the simulation runs.
class Track:

    #Store Individual IDs of Marines With Each Priority
    #Used during execution for storage of priorities as they are assigned.
    individual_marines_priority_count_dictionary = {
        "Priority 1: Red": [],
        "Priority 2: Yellow": [],
        "Priority 3: Green": [],
        "Priority 4: Black": []
    }

    #Store Number of Each Priority
    #Used at the end to hold calculated values.
    total_priority_count_dictionary = {
        "Priority 1: Red": [],
        "Priority 2: Yellow": [],
        "Priority 3: Green": [],
        "Priority 4: Black": []

    }

    #Store Individual Times at Location in a List
    #Used during execution to store times of Marines at locations as they go through the system.
    individual_times_at_locations_dictionary = {
        "Initial Triage/Water Pickup": [],
        "Main Battle Dressing Station": [],
        "Holding Area": [],
        "Auxillary Treatment Area": [],
        "Other Location": [],
        "Waiting For Red Doctor": [],
        "Waiting For Yellow Doctor": [],
        "Waiting for Green Corpsman": [],
        "Waiting for Black Corpsman": [],
        "With Red Dedicated Doctor": [],
        "With Yellow Dedicated Doctor": [],
        "With Green Dedicated Corpsman": [],
        "With Black Dedicated Corpsman": []
    }

    #Store Average Time At Locations
    #Used at the end for calculations.
    average_times_at_locations_dictionary = {
        "Initial Triage/Water Pickup": [],
        "Main Battle Dressing Station": [],
        "Holding Area": [],
        "Auxillary Treatment Area": [],
        "Other Location": [],
        "Waiting For Red Doctor": [],
        "Waiting For Yellow Doctor": [],
        "Waiting for Green Corpsman": [],
        "Waiting for Black Corpsman": [],
        "With Red Dedicated Doctor": [],
        "With Yellow Dedicated Doctor": [],
        "With Green Dedicated Corpsman": [],
        "With Black Dedicated Corpsman": []
    }