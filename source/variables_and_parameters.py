#Class representing...
#VARIABLES AND PARAMETERS
#Global variables and a parameters are tweaked here.
class VariablesAndParameters:
    #Sim Details
    warm_up = 3
    number_of_runs = 10
    run_number = 0
    duration_of_simulation_in_minutes = 500
    simulation_time = (duration_of_simulation_in_minutes * 60)
    #SIMULATION TIME IS IN SECONDS

    #People Involved
    #We are calculating how many Marines we can handle before resources are swamped or strained. Therefore, marine_counter starts and stays at 0.
    marine_counter = 0
    number_of_water_pickup_triage_personnel = 10
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
    interarrival_mean = 1
    water_pickup_triage_mean_time = 1.2
    water_pickup_triage_stdev_time = 1
    red_mean_doctor_main_bds_consultation = 4
    red_stdev_doctor_main_bds_consultation = 1
    yellow_mean_doctor_holding_area_consultation = 3
    yellow_stdev_doctor_holding_area_consultation = 1
    green_mean_corpsman_auxillary_treatment_area_consultation = 2
    green_stdev_corpsman_auxillary_treatment_area_consultation = 1
    black_mean_corpsman_other_location_consultation = 2
    black_stdev_corpsman_other_location_consultation = 1

    #INSIGHTS
    #How Long It Takes From Water to Color-Coded Area
    wait_time_of_inital_triage_water_pickup = []
    red_wait_time_between_triage_to_main_bds = []
    yellow_wait_time_between_triage_to_holding_area = []
    green_wait_time_between_triage_to_auxillary_treatment_area = []
    black_wait_time_between_triage_to_other_location = []

    #How Long It Takes Once In Color-Coded To Get A Provider
    red_wait_for_doctor_main_bds = []
    yellow_wait_for_doctor_holding_area = []
    green_wait_for_corpsman_auxillary_treatment_area = []
    black_wait_for_corpsman_other_location = []

    #How Long It Takes In Color-Coded Area For Care
    red_time_in_main_bds = []
    yellow_time_in_holding_area = []
    green_time_in_aux_treatment_area = []
    black_time_in_other_location = []