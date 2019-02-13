
import matplotlib.pyplot as plt
from wind_farm_controls_tools.floris_utilities import FlorisInterface
from wind_farm_controls_tools.cut_plane import HorPlane
# from wind_farm_controls_tools.visualization import VisualizationManager


floris_interface_a = FlorisInterface("example_input.json")
floris_interface_a.run_floris()
floris_flow_field_a = floris_interface_a.get_flow_field()

# NOTE THIS DOESN"T WORK BECAUSE FORMATTING OF FLOWFIELD IS NOT LIKE VTK IN FLORIS
hor_plane = HorPlane(floris_flow_field_a,90)
hor_plane.visualize()

plt.show()

# # visualization (old way)
# vm = VisualizationManager()
# vm.plot_x_planes(floris_flow_field_a, [0.5])
# vm.show()
