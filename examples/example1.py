
from wind_farm_controls_tools.floris_utilities import FlorisInterface
from wind_farm_controls_tools.visualization import VisualizationManager


floris_interface_a = FlorisInterface("example_input.json")
floris_interface_a.run_floris()
floris_flow_field_a = floris_interface_a.get_flow_field()

# visualization
vm = VisualizationManager()
vm.plot_x_planes(floris_flow_field_a, [0.5])
vm.show()
