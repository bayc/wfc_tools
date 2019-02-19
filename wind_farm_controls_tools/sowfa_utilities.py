#
# Copyright 2019 NREL
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#

import numpy as np
from .generic_simulation import GenericInterface
from .flow_field import FlowField
from .types import Vec3
import pandas as pd
import os

#TODO: Maybe can one day remove this but for now has convenient csv opener
#TODO For now a SOWFA case can only be one where the turbine outputs and the averaged flow field have been saved


class SowfaInterface(GenericInterface):
    """
    - handle data averaging
    """

    def __init__(self, case_folder,
                 flow_field_sub_path='array_mean/array.mean0D_UAvg.vtk',
                 setup_sub_path='setUp',
                 turbine_array_sub_path='constant/turbineArrayProperties',
                 turbine_sub_path='constant/turbineProperties',
                 controlDict_sub_path='system/controlDict',
                 turbine_output_sub_path='turbineOutput/20000'):

        # Save the case_folder and sub_paths
        self.case_folder = case_folder
        self.setup_sub_path = setup_sub_path
        self.turbine_array_sub_path = turbine_array_sub_path
        self.turbine_sub_path = turbine_sub_path
        self.controlDict_sub_path = controlDict_sub_path
        self.turbine_output_sub_path = turbine_output_sub_path

        # Populate inputs and outputs
        self.import_inputs_and_outputs()

        # Read the flow field
        flow_field = self.read_flow_frame_SOWFA(os.path.join(case_folder, flow_field_sub_path))

        # Re-set turbine positions to flow_field origin
        self.layout_x = self.layout_x - flow_field.origin.x1
        self.layout_y = self.layout_y - flow_field.origin.x2
        #TODO HUB-HEIGHT reset with z??

        super().__init__(flow_field)

    def import_inputs_and_outputs(self):

        # Read in the input files

        # Get control settings from sc input file
        #TODO Assuming not dynamic and only one setting applied for each turbine
        #TODO If not using the super controller sowfa variant, need alternative
        df_SC = read_sc_input(self.case_folder)
        self.yaw_angles = df_SC.yaw.values
        self.pitch_angles = df_SC.pitch.values

        # Get the turbine name and locations
        turbine_array_dict = read_foam_file(os.path.join(self.case_folder, self.turbine_array_sub_path))
        self.turbine_name = turbine_array_dict['turbineType'].replace('"', '')  # TODO Assuming only one type
        self.layout_x, self.layout_y = get_turbine_locations(os.path.join(self.case_folder, self.turbine_array_sub_path))

        # Get the turbine rotor diameter and hub height
        turbine_dict = read_foam_file(os.path.join(self.case_folder, self.turbine_sub_path, self.turbine_name))
        self.D = 2 * turbine_dict['TipRad']
        # print(turbine_dict)

        # Use the setup file and control file to determine the precursor wind speed
        # And the time flow averaging begins (settling time)
        setup_dict = read_foam_file(os.path.join(self.case_folder, self.setup_sub_path))
        controlDict_dict = read_foam_file(os.path.join(self.case_folder, self.controlDict_sub_path))
        start_run_time = controlDict_dict['startTime']
        averagine_start_time = setup_dict['meanStartTime']
        self.settling_time = averagine_start_time - start_run_time
        self.precursor_wind_speed = setup_dict['U0Mag']

        # Get the wind direction
        self.precursor_wind_dir = setup_dict['dir']

        # print(turbine_array_dict['baseLocation'])

        # Read the outputs
        self.turbine_output = read_sowfa_df(os.path.join(self.case_folder, self.turbine_output_sub_path))

        # Remove the settling time
        self.turbine_output = self.turbine_output[self.turbine_output.time > self.settling_time]

        # Get the sim_time
        self.sim_time_length = self.turbine_output.time.max()

    def __str__(self):

        print('---------------------')
        print('Case: %s' % self.case_folder)
        print('==Turbine Info==')
        print('Turbine: %s' % self.turbine_name)
        print('Diameter: %dm' % self.D)
        print('Num Turbines = %d' % len(self.layout_x))
        print('==Control Settings==')
        print('Yaw Angels, ', self.yaw_angles)
        print('Pitch Angels, ', self.pitch_angles)
        print('==Inflow Info==')
        print('U0Mag: %.2fm/s' % self.precursor_wind_speed)
        print('dir: %.1f' % self.precursor_wind_dir)
        print('==Timing Info==')
        print('Settling time: %.1fs' % self.settling_time)
        print('Simulation time: %.1fs' % self.sim_time_length)
        print('---------------------')
        return ' '

    def read_flow_frame_SOWFA(self, filename):
        """Read flow array output from SOWFA


        input: filename: name of flow array to open

        output:
            df: a pandas table with the columns, x,y,z,u,v,w of all relavent flow info
            origin: the origin of the flow field, for reconstructing turbine coords

        Paul Fleming, 2018 """

        # Read the dimension info from the file
        with open(filename, 'r') as f:
            for _ in range(10):
                read_data = f.readline()
                if 'SPACING' in read_data:
                    splitstring = read_data.rstrip().split(' ')
                    spacing = Vec3(float(splitstring[1]), float(splitstring[2]), float(splitstring[3]))
                if 'DIMENSIONS' in read_data:
                    splitstring = read_data.rstrip().split(' ')
                    dimensions = Vec3(int(splitstring[1]), int(splitstring[2]), int(splitstring[3]))
                if 'ORIGIN' in read_data:
                    splitstring = read_data.rstrip().split(' ')
                    origin = Vec3(float(splitstring[1]), float(splitstring[2]), float(splitstring[3]))

        # Set up x, y, z as lists
        if dimensions.x1 > 1.0:
            xRange = np.arange(0, dimensions.x1*spacing.x1, spacing.x1)
        else:
            xRange = np.array([0.0])

        if dimensions.x2 > 1.0:
            yRange = np.arange(0, dimensions.x2*spacing.x2, spacing.x2)
        else:
            yRange = np.array([0.0])

        if dimensions.x3 > 1.0:
            zRange = np.arange(0, dimensions.x3*spacing.x3, spacing.x3)
        else:
            zRange = np.array([0.0])

        pts = np.array([(x, y, z)
                        for z in zRange for y in yRange for x in xRange])

        df = pd.read_csv(filename, skiprows=10, sep='\t',
                         header=None, names=['u', 'v', 'w'])
        x = pts[:, 0]
        y = pts[:, 1]
        z = pts[:, 2]

        return FlowField(x, y, z, df.u.values, df.v.values, df.w.values, spacing, dimensions, origin)


def read_sc_input(case_folder, filename='SC_INPUT.txt', wind_direction=270.):
    """Read the SC input file to get the wind farm control settings


    input: case_folder: name of case folder
            filename: name of the SC file
            wind_direction: wind direction to subtract from to get relative yaw error

    output: df_SC: Data frame of SC settings

    Paul Fleming, 2018 """

    sc_file = os.path.join(case_folder, filename)

    df_SC = pd.read_csv(sc_file, delim_whitespace=True)

    df_SC.columns = ['time', 'turbine', 'yaw', 'pitch']

    df_SC['yaw'] = wind_direction - df_SC.yaw

    df_SC = df_SC.set_index('turbine')

    return df_SC


def read_sowfa_df(folder_name, channels=[]):
    """New function to use pandas to read in files using pandas

    input: folder_name, where to find the outputs of AL
            channels, not really used for now, but could be a list of desired channels to only read
    output:
		df: a pandas table


    Paul Fleming, 2018 based on 
    Pieter Gebraad, 2015"""

    # Get the availble outputs
    outputNames = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]

    # Remove the harder input files for now (undo someday)
    hardFiles = ['Vtangential', 'Cl', 'Cd', 'Vradial', 'x', 'y', 'z', 'alpha', 'axialForce']
    simpleFiles = ['nacYaw', 'rotSpeedFiltered', 'rotSpeed', 'thrust', 'torqueGen', 'powerRotor', 'powerGenerator', 'torqueRotor', 'azimuth', 'pitch']

    # Limit to files
    if len(channels) == 0:
    	outputNames = [o for o in outputNames if o in simpleFiles]
    else:
    	outputNames = channels

    # Get the number of channels
    num_channels = len(outputNames)

    if num_channels == 0:
        raise ValueError('Is %s a data folder?' % folder_name)

    # Now loop through the files
    for c_idx, chan in enumerate(outputNames):

        filename = os.path.join(folder_name, chan)

        # Load the file
        df_inner = pd.read_csv(filename, sep=' ', header=None, skiprows=1)

        # Rename the columns
        df_inner.columns = ['turbine', 'time', 'dt', chan]

        # Drop dt
        df_inner = df_inner[['time', 'turbine', chan]].set_index(['time', 'turbine'])

        # On first run declare the new frame
        if c_idx == 0:
            # Declare the main data frame to return as copy
            df = df_inner.copy(deep=True)

        # On other loops just add the new frame
        else:
            df[chan] = df_inner[chan]

    # Reset the index
    df = df.reset_index()

    # Zero the time
    df['time'] = df.time - df.time.min()

    return df


def read_foam_file(filename):
    '''
    Note that this function only reads scalar and boolean/string inputs from
    an OpenFOAM  input file
    '''
    data = {}

    with open(filename, 'r') as fid:
        raw = fid.readlines()

    count = 0
    bloc_comment_test = False
    for i, line in enumerate(raw):

        if raw[i][0:2] == '/*':
            bloc_comment_test = True

        if bloc_comment_test is False:

            # Check if the string is a comment and skip line
            if raw[i].strip()[0:2] == '//' or raw[i].strip()[0:1] == '#':
                pass

            elif len(raw[i].strip()) == 0:  # Check if the string is empty and skip line
                pass

            else:
                tmp = raw[i].strip().rstrip().split()
                try:
                    data[tmp[0].replace('"', '')] = np.float(tmp[1][:-1])
                except:
                    try:
                        data[tmp[0].replace('"', '')] = tmp[1][:-1]
                    except:
                        next

        if raw[i][0:2] == '\*':
            bloc_comment_test = False

    return data


def get_turbine_locations(turbine_array_file):
    import re

    x = list()
    y = list()

    with open(turbine_array_file, 'r') as f:
        for line in f:
            if 'baseLocation' in line:
                # Extract the coordinates
                data = re.findall(r"[-+]?\d*\.\d+|\d+", line)

                # Append the data
                x.append(float(data[0]))
                y.append(float(data[1]))

    layout_x = np.array(x)
    layout_y = np.array(y)

    return layout_x, layout_y
