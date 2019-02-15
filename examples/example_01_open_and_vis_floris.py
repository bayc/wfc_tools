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

floris_interface = wfct.floris_utilities.FlorisInterface("example_input.json")
floris_interface.run_floris()
floris_flow_field = floris_interface.get_flow_field()

hor_plane = wfct.cut_plane.HorPlane(floris_flow_field, 90)
hor_plane.visualize()
plt.show()
