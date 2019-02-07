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

class GenericInterface():
    """
    - cutplane
    - calculate_power_profile
    - layout: defined in the floris json format
    - averaging window
    """

    def __init__(self):
        # private variables
        self._flow_field = None
        # self.wind_speed = wind_speed

    # def flowfield(self):
    #     """
    #     flowfield should be in this format:
    #     DataFrame: {
    #         u: np.array()
    #         v: np.array()
    #         w: np.array()
    #     }
    #     """
    #     return
    