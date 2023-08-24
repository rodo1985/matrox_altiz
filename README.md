# Matrox AltiZ Data Acquisition and Point Cloud Visualization

This code demonstrates how to acquire 3D sensor data and visualize it as a point cloud using Python and the Matrox Imaging Library (MIL).

## Usage

1. Install the required libraries including MIL. See the [requirements.txt](requirements.txt) file for the list of required libraries.
2. Connect the 3D sensor to the computer.
3. Run the code in a Python environment.
4. The code will set the 3D sensor parameters, start the acquisition, and plot the point cloud in a 2D graph.
5. Press the 'q' key to stop the acquisition and exit the program.

## Code Overview

The code consists of two main functions: `get_pointcloud` and `main`.

### `get_pointcloud`

This function takes a MIL container as input and returns a point cloud as a NumPy array. It does the following:

1. Gets the component ID for the range data.
2. Gets the range image sizes, offsets, and resolutions.
3. Gets the range image array as a NumPy array.
4. Creates an empty point cloud as a NumPy array.
5. Fills the point cloud with the range data.
6. Removes the points with a zero z value.
7. Returns the point cloud.

### `main`

This function sets the 3D sensor parameters, starts the acquisition, and plots the point cloud in a 2D graph. It does the following:

1. Allocates MIL objects.
2. Sets the 3D sensor parameters.
3. Starts the acquisition.
4. Gets the point cloud.
5. Plots the point cloud in a 2D graph.
6. Checks if the 'q' key is pressed to stop the acquisition and exit the program.
7. Releases the MIL objects.

## Conclusion

This code demonstrates how to acquire 3D sensor data and visualize it as a point cloud using Python and the Matrox Imaging Library (MIL). It can be used as a starting point for developing more advanced 3D sensor applications.