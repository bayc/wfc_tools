# THIS IS THE CODE PAUL USED TO DOWNSAMPLE THE LARGE SOWFA FLOW FIELD
# IT DOESN"T ACTUALLY WORK SINCE I WONT COMMIT THE LARGE (68MB FILE)

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


flow_field_2 = flow_field.crop([0,1000],[300,700],[0,170])

hor_plane = HorPlane(flow_field_2,90)
hor_plane.visualize()


# Write out the new flow field
flow_field_2.save_as_vtk('sowfa_example/array_mean/array.mean_UAvg.vtk')

#Open this new file and plot
sowfa_case_2 = SowfaInterface('sowfa_example',flow_field_sub_path='array_mean/array.mean_UAvg.vtk')
flow_field = sowfa_case_2._flow_field

hor_plane = HorPlane(flow_field,90)
hor_plane.visualize()

plt.show()