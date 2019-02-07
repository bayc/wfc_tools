class GenericInterface():
    """
    - cutplane
    - calculate_power_profile
    - layout: defined in the floris json format
    - averaging window
    """

    def __init__(self, wind_speed):
        self.wind_speed = wind_speed

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
    
