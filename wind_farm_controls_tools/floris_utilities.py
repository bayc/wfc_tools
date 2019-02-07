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

import pandas as pd
import numpy as np
from .generic_simulation import GenericInterface
from floris.floris import Floris
from .flow_field import FlowField

# Performance Analysis Uncertainty Library And FLow EstiMation plottING: PAUL A FLEMING


class FlorisInterface(GenericInterface):
    """
    The interface from FLORIS to the wfc tools
    """

    def __init__(self, input_file):
        self.input_file = input_file
        self.floris = Floris(input_file=input_file)
        
        super().__init__(self)

    def run_floris(self):
        self.floris.farm.flow_field.calculate_wake()

    def get_flow_field(self, resolution=None):
        """
        df: a pandas table with the columns, x,y,z,u,v,w of all relevant flow info
            origin: the origin of the flow field, for reconstructing turbine coords
        Paul Fleming, 2018
        """

        flow_field = self.floris.farm.flow_field
        if resolution is not None:
            # TODO: flow_field.redo_resolution()
            pass
        x = flow_field.x.flatten()
        y = flow_field.y.flatten()
        z = flow_field.z.flatten()
        u = flow_field.u_field.flatten()
        if hasattr(flow_field, 'v'):
            v = flow_field.v.flatten()
            w = flow_field.w.flatten()
        return FlowField(x, y, z, u, v, w)
