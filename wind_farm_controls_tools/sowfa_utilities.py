from generic_simulation import GenericInterface

class SowfaData(GenericInterface):
    """
    - handle data averaging
    """

     def __init__(self, wind_speed):
        
        #
        # figure out the wind speed somehow
        #

        #
        # figure out the TI
        #

        super.__init__(wind_speed)


        def read_flow_frame_SOWFA(filename):
    """Read flow array output from SOWFA


    input: filename: name of flow array to open

    output:
		df: a pandas table with the columns, x,y,z,u,v,w of all relavent flow info
        origin: the origin of the flow field, for reconstructing turbine coords

    Paul Fleming, 2018 """

    # Read the dimension info from the file
    with open(filename, 'r') as f:
        for i in range(10):
            read_data = f.readline()
            if 'SPACING' in read_data:
                spacing = tuple([float(d)
                                 for d in read_data.rstrip().split(' ')[1:]])
            if 'DIMENSIONS' in read_data:
                dimensions = tuple([float(d)
                                    for d in read_data.rstrip().split(' ')[1:]])
            if 'ORIGIN' in read_data:
                origin = tuple([float(d)
                                for d in read_data.rstrip().split(' ')[1:]])

    # Set up x, y, z as lists
    if dimensions[0] > 1.0:
        xRange = np.arange(0, dimensions[0]*spacing[0], spacing[0])
    else:
        xRange = np.array([0.0])
    if dimensions[1] > 1.0:
        yRange = np.arange(0, dimensions[1]*spacing[1], spacing[1])
    else:
        yRange = np.array([0.0])
    if dimensions[2] > 1.0:
        zRange = np.arange(0, dimensions[2]*spacing[2], spacing[2])
    else:
        zRange = np.array([0.0])

    pts = np.array([(x, y, z) for z in zRange for y in yRange for x in xRange])

    df = pd.read_csv(filename, skiprows=10, sep='\t',
                     header=None, names=['u', 'v', 'w'])
    df['x'] = pts[:, 0]
    df['y'] = pts[:, 1]
    df['z'] = pts[:, 2]

    return df, spacing, dimensions, origin
