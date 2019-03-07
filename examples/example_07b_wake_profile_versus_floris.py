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

## Example 07b
## Wake profile
## Take a simple one turbine FLORIS case and compare the profile hypothetical power with
## what FLORIS actually produces

import wind_farm_controls_tools as wfct
import wind_farm_controls_tools.visualization as vis
import matplotlib.pyplot as plt
import numpy as np
from wind_farm_controls_tools.types import Vec3

turbine_1_x = 500.
turbine_1_y = 500.

# # Load FLORIS
floris_interface = wfct.floris_utilities.FlorisInterface("example_input.json")

# Set to one turbine and run
floris_interface.floris.farm.set_turbine_locations([turbine_1_x], [turbine_1_y], calculate_wake=False)
floris_interface.floris.farm.set_yaw_angles(np.radians([0]), calculate_wake=False)
floris_interface.run_floris()

# Get the FLORIS domain bounds and define a resolution
xmin, xmax, ymin, ymax, zmin, zmax = floris_interface.floris.farm.flow_field._get_domain_bounds()
resolution = Vec3(
    1 + (xmax - xmin) / 10,
    1 + (ymax - ymin) / 10,
    1 + (zmax - zmin) / 10
)

floris_flow_field = floris_interface.get_flow_field(resolution=resolution)

# # Check flow
fig, ax = plt.subplots()
hor_plane = wfct.cut_plane.HorPlane(floris_flow_field, 90)
wfct.visualization.visualize_cut_plane(hor_plane,ax=ax)
vis.plot_turbines(ax, floris_interface.floris.farm.layout_x, floris_interface.floris.farm.layout_y, np.degrees(floris_interface.get_yaw_angles()), floris_interface.floris.farm.turbine_map.turbines[0].rotor_diameter)
ax.set_title('FLORIS')


# Grab floris turbine cp/ct tables
# TODO for now assume only one turbine, is this how to do this?
# print(floris_interface.floris.farm.turbines)
for turbine in floris_interface.floris.farm.turbines: # turbine_map.items():
    floris_ws = turbine.power_thrust_table["wind_speed"]
    floris_ct = turbine.power_thrust_table["thrust"]
    floris_cp = turbine.power_thrust_table["power"]


# Use profile method to check power at 1200 m
second_turbine_x = 1200
floris_cross = wfct.cut_plane.CrossPlane(floris_flow_field,second_turbine_x)

# What is the hypothetical power at this point
D = 126.
hypothetical_power = wfct.cut_plane.calculate_power(floris_cross,x1_loc=turbine_1_y,x2_loc=90,R=D/2.,ws_array=floris_ws,cp_array=floris_cp)
print('Hypothetical Power = %.2f MW' % (hypothetical_power/1E6))

## What is the power from FLORIS================


# Add a second turbine
floris_interface.floris.farm.set_turbine_locations([turbine_1_x,second_turbine_x], [turbine_1_y,turbine_1_y], calculate_wake=False)
floris_interface.floris.farm.set_yaw_angles(np.radians([0,0]), calculate_wake=False)
floris_interface.run_floris()

# Visualize the two turbine case
floris_flow_field = floris_interface.get_flow_field(resolution=resolution)
fig, ax = plt.subplots()
hor_plane = wfct.cut_plane.HorPlane(floris_flow_field, 90)
wfct.visualization.visualize_cut_plane(hor_plane,ax=ax)
vis.plot_turbines(ax, floris_interface.floris.farm.layout_x, floris_interface.floris.farm.layout_y, np.degrees(floris_interface.get_yaw_angles()), floris_interface.floris.farm.turbine_map.turbines[0].rotor_diameter)
ax.set_title('FLORIS')

# Grab second turbine power
for turbine in floris_interface.floris.farm.turbines: # turbine_map.items():
    floris_power = turbine.power

print('FLORIS Power = %.2f MW' % (floris_power/1E6))


plt.show()