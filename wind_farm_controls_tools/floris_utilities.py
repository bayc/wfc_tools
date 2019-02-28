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
from floris import Floris
from .flow_field import FlowField
from .types import Vec3

class FlorisInterface(GenericInterface):
    """
    The interface from FLORIS to the wfc tools
    """

    def __init__(self, input_file):
        self.input_file = input_file
        self.floris = Floris(input_file=input_file)
        flow_field = self.get_flow_field()

        super().__init__(flow_field)

    def run_floris(self):
        self.floris.calculate_wake()

    def get_flow_field(self, resolution=None):
        flow_field = self.floris.farm.flow_field
        if resolution is not None:
            # TODO: flow_field.redo_resolution()
            pass

        order = "f"
        x = flow_field.x.flatten(order=order)
        y = flow_field.y.flatten(order=order)
        z = flow_field.z.flatten(order=order)

        u = flow_field.u.flatten(order=order)
        v = flow_field.v.flatten(order=order)
        w = flow_field.w.flatten(order=order)

        # Determine spacing, dimensions and origin
        unique_x = np.sort(np.unique(x))
        unique_y = np.sort(np.unique(y))
        unique_z = np.sort(np.unique(z))
        spacing = Vec3(
            unique_x[1] - unique_x[0],
            unique_y[1] - unique_y[0],
            unique_z[1] - unique_z[0]
        )
        dimensions = Vec3(len(unique_x), len(unique_y), len(unique_z))
        origin = Vec3(0.0, 0.0, 0.0)
        return FlowField(x, y, z, u, v, w, spacing=spacing, dimensions=dimensions, origin=origin)

    def get_yaw_angles(self):
        yaw_angles = [np.degrees(turbine.yaw_angle) for turbine in self.floris.farm.turbine_map.turbines]
        return yaw_angles
