# Copyright 2017 NREL

# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from .types import Vec3
import matplotlib.pyplot as plt
import numpy as np

def plot_turbines(ax, layout_x, layout_y, yaw_angles, D):

    for x, y, yaw in zip(layout_x,layout_y,yaw_angles):
        R = D/2.
        x_0 = x + np.sin(np.deg2rad(yaw)) * R
        x_1 = x - np.sin(np.deg2rad(yaw)) * R
        y_0 = y - np.cos(np.deg2rad(yaw)) * R
        y_1 = y + np.cos(np.deg2rad(yaw)) * R
        ax.plot([x_0,x_1],[y_0,y_1],color='k')


class VisualizationManager():
    """
    The VisualizationManager handles all of the lower level visualization instantiation
    and data management. Currently, it produces 2D matplotlib plots for a given plane
    of data.

    IT IS IMPORTANT to note that this class should be treated as a singleton. That is,
    only one instance of this class should exist.
    """

    def __init__(self):
        self.figure_count = 0

    # General plotting functions

    def _set_texts(self, plot_title, horizontal_axis_title, vertical_axis_title):
        fontsize = 15
        plt.title(plot_title, fontsize=fontsize)
        plt.xlabel(horizontal_axis_title, fontsize=fontsize)
        plt.ylabel(vertical_axis_title, fontsize=fontsize)

    def _set_colorbar(self, label):
        cb = plt.colorbar()
        cb.set_label(label)
        cb.ax.tick_params(labelsize=15)

    def _set_axis(self):
        plt.axis('equal')
        plt.tick_params(which='both', labelsize=15)

    def _new_figure(self):
        plt.figure()
        self.figure_count += 1

    def _new_filled_contour(self, mesh1, mesh2, data):
        self._new_figure()
        vmax = np.amax(data)
        plt.contourf(mesh1, mesh2, data, 50,
                     cmap='viridis', vmin=0, vmax=vmax)

    def _plot_constant_plane(self,
                             mesh1,
                             mesh2,
                             data,
                             title,
                             xlabel,
                             ylabel,
                             colorbar=True,
                             colorbar_label=''):
        self._new_filled_contour(mesh1, mesh2, data)
        self._set_texts(title, xlabel, ylabel)
        if colorbar:
            self._set_colorbar(colorbar_label)
        self._set_axis()

    # FLORIS-specific data manipulation and plotting
    def _add_turbine_marker(self, turbine, coords, wind_direction):
        a = Vec3(coords.x, coords.y - turbine.rotor_radius)
        b = Vec3(coords.x, coords.y + turbine.rotor_radius)
        a.rotate_z(turbine.yaw_angle - wind_direction, coords.as_tuple())
        b.rotate_z(turbine.yaw_angle - wind_direction, coords.as_tuple())
        plt.plot([a.xprime, b.xprime], [a.yprime, b.yprime], 'k', linewidth=1)

    # def _plot_constant_z(self, xmesh, ymesh, data, **kwargs):
    #     self._plot_constant_plane(
    #         xmesh, ymesh, data, 'z plane', 'x (m)', 'y (m)', colorbar_label='Flow speed (m/s)', **kwargs)

    # def _plot_constant_y(self, xmesh, zmesh, data, **kwargs):
    #     self._plot_constant_plane(
    #         xmesh, zmesh, data, 'y plane', 'x (m)', 'z (m)', colorbar_label='Flow speed (m/s)', **kwargs)

    def _plot_constant_x(self, ymesh, zmesh, data, **kwargs):
        self._plot_constant_plane(
            ymesh, zmesh, data, 'x plane', 'y (m)', 'z (m)', colorbar_label='Flow speed (m/s)', **kwargs)

    # def _add_z_plane(self, percent_height=0.5, **kwargs):
    #     plane = int(self.flow_field.grid_resolution.z * percent_height)
    #     self._plot_constant_z(
    #         self.flow_field.x[:, :, plane],
    #         self.flow_field.y[:, :, plane],
    #         self.flow_field.u_field[:, :, plane],
    #         **kwargs)
    #     for coord, turbine in self.flow_field.turbine_map.items():
    #         self._add_turbine_marker(
    #             turbine, coord, self.flow_field.wind_direction)

    # def _add_y_plane(self, percent_height=0.5, **kwargs):
    #     plane = int(self.flow_field.grid_resolution.y * percent_height)
    #     self._plot_constant_y(
    #         self.flow_field.x[:, plane, :],
    #         self.flow_field.z[:, plane, :],
    #         self.flow_field.u_field[:, plane, :],
    #         **kwargs)

    def _add_x_plane(self, flow_field, percent_height=0.5, **kwargs):
        plane = int(flow_field.grid_resolution.x * percent_height)
        self._plot_constant_x(
            flow_field.y[plane, :, :],
            flow_field.z[plane, :, :],
            flow_field.u[plane, :, :],
            **kwargs)

    # def plot_z_planes(self, planes, **kwargs):
    #     for p in planes:
    #         self._add_z_plane(p, **kwargs)

    # def plot_y_planes(self, planes, **kwargs):
    #     for p in planes:
    #         self._add_y_plane(p, **kwargs)

    def plot_x_planes(self, flow_field, planes, **kwargs):
        """
        flow_field: FlowField
            An instance of a FlowField with all necessary data

        planes: [0.1,0.2]
            a list of plane locations to plot
        """
        for p in planes:
            self._add_x_plane(flow_field, p, **kwargs)

    def show(self):
        plt.show()

    # def _map_coordinate_to_index(self, coord):
    #     xi = max(0, int(self.grid_resolution.x * (coord.x - self.xmin - 1) \
    #         / (self.xmax - self.xmin)))
    #     yi = max(0, int(self.grid_resolution.y * (coord.y - self.ymin - 1) \
    #         / (self.ymax - self.ymin)))
    #     zi = max(0, int(self.grid_resolution.z * (coord.z - self.zmin - 1) \
    #         / (self.zmax - self.zmin)))
    #     return xi, yi, zi

    # def _field_value_at_coord(self, target_coord, field):
    #     xi, yi, zi = self._map_coordinate_to_index(target_coord)
    #     return field[xi, yi, zi]
