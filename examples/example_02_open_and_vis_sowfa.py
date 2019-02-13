# DOES NOT WORK?
# import wind_farm_controls_tools as wfct #Why doesn't this way work?
# sowfa_case = wfct.sowfa_utilities.SowfaInterface('sowfa_example')

# This seems to work:
#TODO Super ugly though get to an "as" type import
from wind_farm_controls_tools.sowfa_utilities import SowfaInterface
from wind_farm_controls_tools.cut_plane import HorPlane

import matplotlib.pyplot as plt

sowfa_case = SowfaInterface('sowfa_example')

# Show the original horizontal plane
flow_field = sowfa_case._flow_field
hor_plane = HorPlane(flow_field,90)
hor_plane.visualize()

plt.show()