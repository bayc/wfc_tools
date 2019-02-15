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

## Example 07
## Wake profile
## In this example:
## 1) Load the SOWFA and FLORIS model
## 2) Make the FLORIS to match the SOWFA simulation setup
## 3) Get vertical cut planes at 3 and 5 D
## 3) Compare the wake profiles at 3 and 5 D

import wind_farm_controls_tools as wfct
import matplotlib.pyplot as plt


# Load SOWFA
sowfa_case = wfct.sowfa_utilities.SowfaInterface('sowfa_example')
sowfa_flow_field = sowfa_case._flow_field #TODO Correct?
print(sowfa_case)

# Load FLORIS
#TODO Make match SOWFA (waiting for earlier example to copy from)
floris_interface = wfct.floris_utilities.FlorisInterface("example_input.json")
floris_interface.run_floris()
floris_flow_field = floris_interface.get_flow_field()

# Grab floris turbine cp/ct tables
# TODO for now assume only one turbine, is this how to do this?
for coord, turbine in floris_interface.floris.farm.turbine_map.items():
    floris_ws = turbine.power_thrust_table["wind_speed"]
    floris_ct = turbine.power_thrust_table["thrust"]
    floris_cp = turbine.power_thrust_table["power"]


# Determine the cut planes distances for 3 and 5 D
D = sowfa_case.D

# Get the 3D values
sowfa_cut_3 = wfct.cut_plane.CrossPlane(sowfa_flow_field,3 * D + sowfa_case.layout_x[0],y_center=sowfa_case.layout_y[0], z_center=90,D=D)
x_locs, ws_3 = sowfa_cut_3.get_profile()
x_locs, pow_3 = sowfa_cut_3.get_power_profile(floris_ws,floris_cp,D/2.)

# Get the 7D values
sowfa_cut_5 = wfct.cut_plane.CrossPlane(sowfa_flow_field,5 * D + sowfa_case.layout_x[0],y_center=sowfa_case.layout_y[0], z_center=90,D=D)
x_locs, ws_5 = sowfa_cut_5.get_profile()
x_locs, pow_5 = sowfa_cut_5.get_power_profile(floris_ws,floris_cp,D/2.)

fig, axarr = plt.subplots(2,2,sharex=True)

# Plot the visuals
sowfa_cut_3.visualize(axarr[0,0])
sowfa_cut_5.visualize(axarr[0,1])
axarr[0,0].set_title('3D')
axarr[0,1].set_title('5D')

# Plot the wind-speed profiles
ax = axarr[1,0]
ax.plot(x_locs, ws_3,label='SOWFA 3D')
ax.plot(x_locs, ws_5,label='SOWFA 5D')
ax.grid()
ax.set_ylabel('WindSpeed (m/s)')
ax.set_xlabel('X Location (D)')
ax.legend()

# Plot the power profiles
ax = axarr[1,1]
ax.plot(x_locs, pow_3/1E6,label='SOWFA 3D')
ax.plot(x_locs, pow_5/1E6,label='SOWFA 5D')
ax.grid()
ax.set_ylabel('Power (MW)')
ax.set_xlabel('X Location (D)')
ax.legend()

plt.show()