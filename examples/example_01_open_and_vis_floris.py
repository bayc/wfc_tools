
import matplotlib.pyplot as plt
from wind_farm_controls_tools.floris_utilities import FlorisInterface
from wind_farm_controls_tools.cut_plane import HorPlane

floris_interface = FlorisInterface("example_input.json")
floris_interface.run_floris()
floris_flow_field = floris_interface.get_flow_field()

# NOTE THIS DOESN"T WORK BECAUSE FORMATTING OF FLOWFIELD IS NOT LIKE VTK IN FLORIS
hor_plane = HorPlane(floris_flow_field, 90)
hor_plane.visualize()
plt.show()

# from wind_farm_controls_tools.visualization import VisualizationManager
# # visualization (old way)
# vm = VisualizationManager()
# vm.plot_x_planes(floris_flow_field_a, [0.5])
# vm.show()
