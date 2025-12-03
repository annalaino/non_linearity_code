import random
import os
import pandas as pd
import pickle
import numpy as np
#from queue import Queue
from datetime import datetime as dt
from datetime import timedelta as time_delta
import scipy.stats as stats


#global bod, cod, c_bod, c_cod, bodi, codi
global output_df, base_concentrations, start_dt, dfi
global base_report_path,  set_random_inputs ,monte_carlo_sim

# simulation information
number_of_monte_carlo = 7
CommInt = 0.08
StopTime = 60.0
#Bodlt = 25
#Bodut = 50 
#Bodp = 0.7
#Codut = 250
#Codlt = 125
#Codp = 0.75
#bodi = ["BOD infl composite"]
#codi = ["COD infl composite"] 
#bod = ["BOD effl composite"]
#cod = ["COD effl composite"]
#c_bod = ["c_bod"]
#c_cod = ["c_cod"]

# functions
def profile_variables():
    """
    Returns a dictionary containing the variables that profiles will be obtained for
    """
    print("profile variables start")
    profile_variables = {
        'snh1': 'Ammonia influent',
        'snh31':'Ammonia effluent',
        'abod132': 'BOD influent composite',
        'bod1': 'BOD influent instantaneous',
        'bod31': 'BOD effluent instantaneous',
        'cod1': 'COD influent instantaneous',
        'cod31': 'COD effluent instantaneous',
        'acod132': 'COD influent composite',
        'abod124': 'BOD effluent composite',
        'acod124': 'COD effluent composite',
        'asnh132': 'Ammonia influent composite',
        'asnh124':'Ammonia effluent composite',
    }    
    print("profile variables end")
    return profile_variables

#def single_observation_variables():
    """
    Returns a dictionary of variables to be collected only once at the end of the simulation
    """
#    single_variables = {
#        'codconclimitfinaleff': 'Effluent COD Constraint',
#        'codtimeviolatedfinaleff': 'Total Time Violating COD Constraint',
#        'codptimeviolatedfinaleff': 'Percent of Time Violating COD Constraint',
#        'bodconclimitfinaleff': 'Effluent BOD Constraint',
#        'bodtimeviolatedfinaleff': 'Total Time Violating BOD Constraint',
#        'bodptimeviolatedfinaleff': 'Percent of Time Violating BOD Constraint',
#        'rainEvents': 'Number of rain events experienced'}
#    print("single_variables")
#    return single_variables   

        
def build_profile_df():
    """
    Builds an empty dataframe where results of the GPS-X simulation are stored
    """
    print("build_profile start")
    df = pd.DataFrame()
    variables = profile_variables()
    
    for var in variables:
        df[var] = None

    print("build_profile end")
    return df

#def build_single_observation_df():
    """
    Builds an empty dataframe where end of simulation results of the GPS-X simulation are stored
    """
#    df = pd.DataFrame()
#    for var in single_observation_variables():
#        df[var] = None
#        print("single_obs")
#    return df


def collect_outputs(df, index_type):
    """
    Gets the value of simulation outputs to be observed in the GPS-X simulation

    df (dataframe): Dataframe where observed values will be stored
    index_type (str): datetime -> use a datetime index
                      monte_carlo -> use current monte carlo iteration as an index
    data_frame (dataframe): Dataframe containing the simulation variables
    """
    print("collect output start")
    results = []

    for variable in df.columns:
        
        simulation_value = get_simulation_value(variable)
        results.append(simulation_value)

    if index_type == 'datetime':
        df.loc[get_sim_dt(), :] = results
    elif index_type == 'monte_carlo':
        df.loc[monte_carlo_sim, :] = results
    else:  # if not one of the specified index types, have an incrementing index
        df.loc[len(df.index), :] = results
    print("collect output end")

def get_simulation_value(variable):
    """
    Gets the current value of a parameter in the GPS-X simulation
    """
    print("get simulation value start")
    if '(' in variable:
        cryptic, index = variable.split('(')
        print(f"variable: {variable}, index: {index}, cryptic: {cryptic}")
        print(f"value before index shift: {gpsx.getValue(cryptic)}")
        index = int(index[:-1])
        value = gpsx.getValueAtIndex(cryptic, index)
        print(f"value after index shift: {value}")
    else:
        
        value = gpsx.getValue(variable)
        print(f"variable non split: [{variable}= {value}]")
    print("get simulation value end")
    return value


def set_default_sim_parameters():
    """
    Sets the default GPS-X simulation parameters
    """
    print("set_default_sim_parameters start")
    gpsx.resetSim()
    gpsx.resetAllValues()
    gpsx.setCint(CommInt)
    gpsx.setTstop(StopTime)
    gpsx.setSteady(True)
    #gpsx.setValue('truckNumber', 0)
    #gpsx.setValue('rainEvents', 0)
    print("set_default_sim_parameters end")

def set_start_dt(start_dt):
    """
    Sets the simulation start time values in GPS-X
    """
    print("set_start_dt start")
    gpsx.setValueAtIndex('ztime', 1, start_dt.year)
    gpsx.setValueAtIndex('ztime', 2, start_dt.month)
    gpsx.setValueAtIndex('ztime', 3, start_dt.day)
    gpsx.setValueAtIndex('ztime', 4, start_dt.hour)
    gpsx.setValueAtIndex('ztime', 5, start_dt.minute)
    gpsx.setValueAtIndex('ztime', 6, start_dt.second)
    print("set_start_dt end")

def get_sim_dt():
    """
    Returns the current datetime for the simulation
    """
    print("get_sim_dt start")
    if gpsx.getValue('t') != 0:
        year = int(gpsx.getValue('iyear'))
        month = int(gpsx.getValue('imonth'))
        day = int(gpsx.getValue('iday'))
        hour = int(gpsx.getValue('ihour'))
        minute = int(gpsx.getValue('iminute'))
        second = int(gpsx.getValue('isec'))

        current_time = dt(year, month, day, hour, minute, second)
    else:
        current_time = start_dt
    
    print("get_sim_dt end")

    return current_time



def get_elapsed_time():
    """
    Returns the elapsed simulation time in seconds
    """
    print("get_elapsed_time start")
    elapsed_seconds = gpsx.getValue('t')
    print("get_elapsed_time end")

    return elapsed_seconds

def start():
    global dfi
    try:
        
        file_path = "C:/Users/Anna Stefania Laino/OneDrive - Newcastle University/NEW WORK- OMAR/CSTR/hybrid aeration n1 - mech aeration/composite sample/cstr - gpsx/Inlet - N-D 2021.xls"

        dfi = pd.read_excel(file_path, header=0)

        dfi = dfi.drop(dfi.columns[0], axis=1)
        
        print(f"dfi_col_dropped: {dfi}")
        print("read excel end")

        print("start")

    except Exception as e:
        print(e)

def set_random_inputs():
    print("set_random_inputs start")
    columns_to_fit = dfi.columns[:]

    chosen_shift = 1.9 # shift the mean of the %
    alp = np.log(1 + chosen_shift)
    shifted_data_df = pd.DataFrame()
    for column in columns_to_fit:
        data = dfi[column].values

        data_numeric = pd.to_numeric(data, errors='coerce')
        data_numeric = data_numeric[~np.isnan(data_numeric)]

        if len(data_numeric) == 0:
            print(f"Column '{column}' contains no valid numeric data. Skipping.")
            continue

        log_data = np.log(data_numeric)
        mean_log = np.mean(log_data)
        std_log = np.std(log_data)

        original_dist = stats.lognorm(s=std_log, scale=np.exp(mean_log))
        shifted_mean_log = mean_log + alp
        shifted_dist = stats.lognorm(s=std_log, scale=np.exp(shifted_mean_log))

        num_samples = len(data_numeric)
        shifted_samples = shifted_dist.rvs(size=num_samples)
        shifted_data_df[column] = shifted_samples

        for index, value in enumerate(shifted_samples):
            value_to_set = value
            gpsx.setValue(column, value_to_set) 

    print("set_random_inputs end")



# cint() function executed at every communication interval
def cint():
    try:
        set_random_inputs()
        df = build_profile_df()  # Define and initialize df
        collect_outputs(output_df, 'datetime')
            

    except Exception as e:
        print(f"An error occurred: {e}")


# eor() function executed once at the end of simulation
# finished set True is required to terminate the runSim() function

def eor():
    global finished

    print(f"output_df: {output_df}")
    with open(os.path.join(report_path, 'profile_run_{}.pkl'.format(monte_carlo_sim)), 'wb') as f:
        f.write(pickle.dumps(output_df))
    
    finished = True

    try:
        pass
    except Exception as e:
        print(e)
        base_path = os.getcwd()


report_path = os.path.join(os.getcwd(), 'base_results')  # path where pickled files will be stored

for monte_carlo_sim in range(1, number_of_monte_carlo + 1):
    print("Sim: ", monte_carlo_sim)
    output_df = build_profile_df()  # Start a fresh collection of profiles
    #sludge_trucks = Queue() # Create a new sludge truck queue
    rain_events = {}  # Create a new rain event tracking dictionary
    
    set_default_sim_parameters()
    start_dt = dt.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    set_start_dt(start_dt)
    runSim()



