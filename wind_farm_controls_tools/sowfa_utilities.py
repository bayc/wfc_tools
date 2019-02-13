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
import pandas as pd 
import os

#TODO: Maybe can one day remove this but for now has convenient csv opener

#TODO For now a SOWFA case can only be one where the turbine outputs and the averaged flow field have been saved

class SowfaInterface(GenericInterface):
    """
    - handle data averaging
    """

    def __init__(self, case_folder, flow_field_sub_path='array_mean/array.mean0D_UAvg.vtk',):
        
        # Read the flow field
        flow_field = self.read_flow_frame_SOWFA(os.path.join(case_folder,flow_field_sub_path))

        super().__init__(flow_field)

    def read_flow_frame_SOWFA(self, filename):
        """Read flow array output from SOWFA


        input: filename: name of flow array to open

        output:
            df: a pandas table with the columns, x,y,z,u,v,w of all relavent flow info
            origin: the origin of the flow field, for reconstructing turbine coords

        Paul Fleming, 2018 """

        # Read the dimension info from the file
        with open(filename, 'r') as f:
            for i in range(10):
                read_data = f.readline()
                if 'SPACING' in read_data:
                    spacing = tuple([float(d)
                                    for d in read_data.rstrip().split(' ')[1:]])
                if 'DIMENSIONS' in read_data:
                    dimensions = tuple([float(d)
                                        for d in read_data.rstrip().split(' ')[1:]])
                if 'ORIGIN' in read_data:
                    origin = tuple([float(d)
                                    for d in read_data.rstrip().split(' ')[1:]])

        # Set up x, y, z as lists
        if dimensions[0] > 1.0:
            xRange = np.arange(0, dimensions[0]*spacing[0], spacing[0])
        else:
            xRange = np.array([0.0])
        if dimensions[1] > 1.0:
            yRange = np.arange(0, dimensions[1]*spacing[1], spacing[1])
        else:
            yRange = np.array([0.0])
        if dimensions[2] > 1.0:
            zRange = np.arange(0, dimensions[2]*spacing[2], spacing[2])
        else:
            zRange = np.array([0.0])

        pts = np.array([(x, y, z) for z in zRange for y in yRange for x in xRange])

        df = pd.read_csv(filename, skiprows=10, sep='\t',
                        header=None, names=['u', 'v', 'w'])
        x = pts[:, 0]
        y = pts[:, 1]
        z = pts[:, 2]

        flow_field = FlowField(x,y,z,df.u.values,df.v.values,df.w.values,spacing, dimensions,origin)

        return flow_field
