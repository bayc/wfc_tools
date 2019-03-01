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

import matplotlib.pyplot as plt
import wind_farm_controls_tools as wfct
from wind_farm_controls_tools.types import Vec3

# Initialize and execute FLORIS
floris_interface = wfct.floris_utilities.FlorisInterface("example_input.json")
floris_interface.run_floris()

# Get the FLORIS domain bounds and define a resolution
xmin, xmax, ymin, ymax, zmin, zmax = floris_interface.floris.farm.flow_field._get_domain_bounds()
resolution = Vec3(
    1 + (xmax - xmin) / 10,
    1 + (ymax - ymin) / 10,
    1 + (zmax - zmin) / 10
)

# Initialize the horizontal cut
hor_plane = wfct.cut_plane.HorPlane(
    floris_interface.get_flow_field(resolution=resolution),
    floris_interface.floris.farm.turbines[0].hub_height
)

# Plot and show
fig, ax = plt.subplots()
wfct.visualization.visualize_cut_plane(hor_plane,ax=ax)
plt.show()
