"""
Copyright 2018 NREL

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import os
import numpy as np
import pandas as pd
from floris.coordinate import Coordinate


class FlowField():
    #TODO handle none case, maybe defaul values apply like 0 origin and auto determine spacing and dimensions
    def __init__(self, x, y, z, u, v, w, spacing=None, dimensions=None, origin=None):
        """
        x, y, z, u, v, w are numpy arrays
        """
        self.x = x
        self.y = y
        self.z = z
        self.u = u
        self.v = v
        self.w = w

        self.spacing = spacing
        self.dimensions = dimensions
        self.origin = origin

    def save_as_vtk(self, filename):

        # Open the file
        with open(filename, 'w') as out:

            # Write the header
            out.write('# vtk DataFile Version 3.0\n')
            out.write('array.mean0D\n')
            out.write('ASCII\n')
            out.write('DATASET STRUCTURED_POINTS\n')
            out.write('DIMENSIONS %d %d %d\n' % self.dimensions)
            out.write('ORIGIN %.3f %.3f %.3f \n' % self.origin)
            out.write('SPACING %d %d %d\n' % self.spacing)
            out.write('POINT_DATA %d\n' % np.product(self.dimensions))
            out.write('FIELD attributes 1\n')
            out.write('UAvg 3 %d float\n' % np.product(self.dimensions))

            # Put out the data
            for u, v, w in zip(self.u, self.v, self.w):
                out.write('%f\t%f\t%f\n' % (u, v, w))

    @staticmethod
    def crop(ff, x_bnds, y_bnds, z_bnds):
        """
        Return a croped version of the flow field
        """

        map_values = (ff.x > x_bnds[0]) & (ff.x < x_bnds[1]) & (ff.y > y_bnds[0]) & (
            ff.y < y_bnds[1]) & (ff.z > z_bnds[0]) & (ff.z < z_bnds[1])

        x = ff.x[map_values]
        y = ff.y[map_values]
        z = ff.z[map_values]

        #  Work out new dimensions
        dimensions = (len(np.unique(x)), len(np.unique(y)), len(np.unique(z)))

        # Work out origin
        origin = (
            ff.origin[0]+np.min(x),
            ff.origin[1]+np.min(y),
            ff.origin[2]+np.min(z),
        )

        return FlowField(
            x-np.min(x),
            y-np.min(y),
            z-np.min(z),
            ff.u[map_values],
            ff.v[map_values],
            ff.w[map_values],
            spacing=ff.spacing,  # doesn't change
            dimensions=dimensions,
            origin=origin
        )
