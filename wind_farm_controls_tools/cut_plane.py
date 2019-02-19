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
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import griddata


class _CutPlane():

    def __init__(self,
                 flow_field,
                 x1='x',
                 x2='y',
                 x3_value=None,
                 resolution=100,
                 x1_center=0.0,
                 x2_center=0.0,
                 D=None,
                 invert_x1=False,
                 crop_x1=None,
                 crop_x2=None):

        # Assign the axis names
        self.x1_name = x1
        self.x2_name = x2
        # TODO: if it will be assumed that x3 is the one of x, y, or z that is x1 and x2,
        #       then we should verify that x1 and x2 are one of x, y, or z
        self.x3_name = [x3 for x3 in ['x', 'y', 'z'] if x3 not in [x1, x2]][0]

        # For convenience convert flow-field to a dataframe
        #TODO this is probable not necessary

        df_flow = pd.DataFrame({'x': flow_field.x,
                                'y': flow_field.y,
                                'z': flow_field.z,
                                'u': flow_field.u,
                                'v': flow_field.v,
                                'w': flow_field.w, })

        # Find the nearest value in 3rd dimension
        #TODO Replace this search stuff with interpolation
        #TODO Also note that this search doesn't use the origin, I think this makes sense for x and y, but if z is not zero, this can get weird
        search_values = np.array(sorted(df_flow[self.x3_name].unique()))
        nearest_idx = (np.abs(search_values-x3_value)).argmin()
        nearest_value = search_values[nearest_idx]
        print('Nearest value to in %s of %.2f is %.2f' %
              (self.x3_name, x3_value, nearest_value))

        # Get a sub-frame of only this 3rd dimension value
        df_sub = df_flow[df_flow[self.x3_name] == nearest_value]

        # Make sure cropping is valid
        if crop_x1:
            if crop_x1[0] < min(df_sub[x1]):
                raise Exception("Invalid x_1 minimum on cropping")
            if crop_x1[1] > max(df_sub[x1]):
                raise Exception("Invalid x_1 maximum on cropping")

        if crop_x2:
            if crop_x2[0] < min(df_sub[x2]):
                raise Exception("Invalid x_2 minimum on cropping")
            if crop_x2[1] > max(df_sub[x2]):
                raise Exception("Invalid x_2 maximum on cropping")

        # Store the relevent values
        self.x1_in = df_sub[x1]
        self.x2_in = df_sub[x2]
        self.u_in = df_sub['u']
        self.v_in = df_sub['v']
        self.w_in = df_sub['w']

        # Save the desired resolution
        self.resolution = resolution

        # Grid the data, if cropping available use that
        if crop_x1:
            self.x1_lin = np.linspace(crop_x1[0], crop_x1[1], self.resolution)
        else:
            self.x1_lin = np.linspace(
                min(self.x1_in), max(self.x1_in), self.resolution)
        if crop_x2:
            self.x2_lin = np.linspace(crop_x2[0], crop_x2[1], self.resolution)
        else:
            self.x2_lin = np.linspace(
                min(self.x2_in), max(self.x2_in), self.resolution)

        # Mesh and interpolate u, v and w
        self.x1_mesh, self.x2_mesh = np.meshgrid(self.x1_lin, self.x2_lin)
        self.u_mesh = griddata(np.column_stack([self.x1_in, self.x2_in]), self.u_in, (
            self.x1_mesh.flatten(), self.x2_mesh.flatten()), method='cubic')
        self.v_mesh = griddata(np.column_stack([self.x1_in, self.x2_in]), self.v_in, (
            self.x1_mesh.flatten(), self.x2_mesh.flatten()), method='cubic')
        self.w_mesh = griddata(np.column_stack([self.x1_in, self.x2_in]), self.w_in, (
            self.x1_mesh.flatten(), self.x2_mesh.flatten()), method='cubic')

        # Save flat vectors
        self.x1_flat = self.x1_mesh.flatten()
        self.x2_flat = self.x2_mesh.flatten()

        # Save u-cubed
        self.u_cubed = self.u_mesh ** 3

        # Save re-centing points for visualization
        self.x1_center = x1_center
        self.x2_center = x2_center

        # If inverting, invert x1, and x1_center
        if invert_x1:
            self.x1_mesh = self.x1_mesh * -1
            self.x1_lin = self.x1_lin * -1
            self.x1_flat = self.x1_flat * -1
            self.x1_center = self.x1_center * -1
            self.v_mesh = self.v_mesh * -1

        # Set the diamater which will be used in visualization
        # Annalysis in D or meters?
        if D == None:
            self.plot_in_D = False
            self.D = 1.
        else:
            self.plot_in_D = True
            self.D = D

    def visualize(self, ax=None, minSpeed=None, maxSpeed=None):
        """ Visualize the scan
        
        Args:
            ax: axes for plotting, if none, create a new one  
            minSpeed, maxSpeed, values used for plotting, if not provide assume to data max min
        """
        if not ax:
            fig, ax = plt.subplots()
        if minSpeed is None:
            minSpeed = self.u_mesh.min()
        if maxSpeed is None:
            maxSpeed = self.u_mesh.max()

        # Reshape UMesh internally
        u_mesh = self.u_mesh.reshape(self.resolution, self.resolution)
        Zm = np.ma.masked_where(np.isnan(u_mesh), u_mesh)

        # Plot the cut-through
        im = ax.pcolormesh((self.x1_lin-self.x1_center)/self.D, (self.x2_lin -
                                                                 self.x2_center)/self.D, Zm, cmap='coolwarm', vmin=minSpeed, vmax=maxSpeed)

        # Make equal axis
        ax.set_aspect('equal')

        return im


# Define horizontal subclass
class HorPlane(_CutPlane):

    def __init__(self, flow_field, z_value, resolution=100, x1_center=0.0, x2_center=0.0, D=None):

        # Set up call super
        super().__init__(flow_field, x1='x', x2='y', x3_value=z_value, resolution=resolution,
                         x1_center=x1_center, x2_center=x2_center, D=D, invert_x1=False)

# Define cross plane subclass


class CrossPlane(_CutPlane):

    def __init__(self, flow_field, x_value, y_center, z_center, D, resolution=100, crop_y=None, crop_z=None, invert_x1=True):

        # Set up call super
        super().__init__(flow_field, x1='y', x2='z', x3_value=x_value, resolution=resolution,
                         x1_center=y_center, x2_center=z_center, D=D, invert_x1=invert_x1, crop_x1=crop_y, crop_x2=crop_z)

    def calculate_wind_speed(self, x1_loc, x2_loc, R):

        # Make a distance column
        distance = np.sqrt((self.x1_flat - x1_loc)**2 +
                           (self.x2_flat - x2_loc)**2)

        # Return the mean wind speed
        return np.cbrt(np.mean(self.u_cubed[distance < R]))

    def get_profile(self, resolution=100, x1_locs=None):
        if x1_locs is None:
            x1_locs = np.linspace(
                min(self.x1_flat), max(self.x1_flat), resolution)
        v_array = np.array([self.calculate_wind_speed(
            x1_loc, self.x2_center, self.D/2.) for x1_loc in x1_locs])
        return ((x1_locs - self.x1_center)/self.D, v_array)

    def get_power_profile(self, ws_array, cp_array, rotor_radius, air_density=1.225, resolution=100, x1_locs=None):

        # Get the wind speed profile
        x1_locs, v_array = self.get_profile(resolution=resolution, x1_locs=x1_locs)

        # Get Cp
        cp_array = np.interp(v_array,ws_array,cp_array)

        # Return power array
        return x1_locs, 0.5 * air_density * (np.pi * rotor_radius**2) * cp_array * v_array**3

