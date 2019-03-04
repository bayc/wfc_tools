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

""""
# EXAMPLE 4
# In this example, open a SOWFA case including all meta-data
# Open a FLORIS case
# Adjust FLORIS parameters to match the SOWFA case
# Plot the two flows with turbine positions indicated
"""

import wind_farm_controls_tools as wfct
import wind_farm_controls_tools.visualization as vis
import wind_farm_controls_tools.cut_plane as cp
from wind_farm_controls_tools.types import Vec3
import matplotlib.pyplot as plt
import numpy as np


# Load the SOWFA case in
sowfa_case = wfct.sowfa_utilities.SowfaInterface('sowfa_example')

# Plot the SOWFA flow and turbines using the input information
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5,8.5))
sowfa_flow_field = sowfa_case.flow_field
hor_plane = wfct.cut_plane.HorPlane(sowfa_case.flow_field, 90)
wfct.visualization.visualize_cut_plane(hor_plane,ax=ax2)
vis.plot_turbines(ax2, sowfa_case.layout_x, sowfa_case.layout_y, sowfa_case.yaw_angles, sowfa_case.D)
ax2.set_title('SOWFA')
# ax2.set_xlabel('x location [m]')
ax2.set_ylabel('y location [m]')

# Load the FLORIS case in
floris_interface = wfct.floris_utilities.FlorisInterface("example_input.json")

# Define a resolution
#TODO Match SOWFA's resolution
# Get the FLORIS domain bounds and define a resolution
xmin, xmax, ymin, ymax, zmin, zmax = floris_interface.floris.farm.flow_field._get_domain_bounds()
resolution = Vec3(
    1 + (xmax - xmin) / 10,
    1 + (ymax - ymin) / 10,
    1 + (zmax - zmin) / 10
)

# Generate and get a flow from original FLORIS file
floris_interface.run_floris()
floris_flow_field_orig = floris_interface.get_flow_field(resolution=resolution)

# Plot the original FLORIS flow and turbines using the input information
hor_plane_orig = cp.HorPlane(floris_flow_field_orig, 90)
wfct.visualization.visualize_cut_plane(hor_plane_orig,ax=ax1)
vis.plot_turbines(ax1, floris_interface.floris.farm.layout_x, floris_interface.floris.farm.layout_y, np.degrees(floris_interface.get_yaw_angles()), floris_interface.floris.farm.turbine_map.turbines[0].rotor_diameter)
ax1.set_title('FLORIS - Original')
ax1.set_ylabel('y location [m]')

# Set the relevant FLORIS parameters to equal the SOWFA case
floris_interface.floris.farm.set_wind_speed(sowfa_case.precursor_wind_speed, calculate_wake=False)
floris_interface.floris.farm.set_wind_direction(sowfa_case.precursor_wind_dir, calculate_wake=False)
floris_interface.floris.farm.set_turbine_locations(sowfa_case.layout_x, sowfa_case.layout_y, calculate_wake=False)
floris_interface.floris.farm.set_yaw_angles(np.radians(sowfa_case.yaw_angles), calculate_wake=False)

# Generate and get a flow from original FLORIS file
floris_interface.run_floris()
floris_flow_field_matched = floris_interface.get_flow_field(resolution=resolution)

# Trim the flow to match SOWFA
sowfa_domain_limits = [[np.min(sowfa_flow_field.x), np.max(sowfa_flow_field.x)],
                       [np.min(sowfa_flow_field.y), np.max(sowfa_flow_field.y)], 
                       [np.min(sowfa_flow_field.z), np.max(sowfa_flow_field.z)]]
floris_flow_field_matched = floris_flow_field_matched.crop(floris_flow_field_matched, sowfa_domain_limits[0], sowfa_domain_limits[1], sowfa_domain_limits[2] )

# Plot the FLORIS flow and turbines using the input information
hor_plane_matched = cp.HorPlane(floris_flow_field_matched, 90)
wfct.visualization.visualize_cut_plane(hor_plane_matched,ax=ax3)
vis.plot_turbines(ax3, floris_interface.floris.farm.layout_x, floris_interface.floris.farm.layout_y, np.degrees(floris_interface.get_yaw_angles()), floris_interface.floris.farm.turbine_map.turbines[0].rotor_diameter)
ax3.set_title('FLORIS - Matched')
ax3.set_xlabel('x location [m]')
ax3.set_ylabel('y location [m]')

plt.show()