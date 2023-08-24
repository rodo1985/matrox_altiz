import mil as MIL
import numpy as np
import ctypes
from matplotlib import pyplot as plt
import keyboard

def get_pointcloud(MilContainer):
   
   # get the component id for the range data
   ComponentId = MIL.MbufInquireContainer(MilContainer, MIL.M_COMPONENT_BY_INDEX(0), MIL.M_COMPONENT_ID)

   # MIL.MbufAllocContainer(MilSystem, MIL.M_PROC + MIL.M_GRAB, MIL.M_DEFAULT)

   # get range image sizes
   size_x = MIL.MbufInquire(ComponentId, MIL.M_SIZE_X)
   size_y = MIL.MbufInquire(ComponentId, MIL.M_SIZE_Y)

   # get offsets
   offset_x = MIL.MbufInquire(ComponentId, MIL.M_3D_OFFSET_X)
   offset_y = MIL.MbufInquire(ComponentId, MIL.M_3D_OFFSET_Y)
   offset_z = MIL.MbufInquire(ComponentId, MIL.M_3D_OFFSET_Z)

   # get resolutions
   resolution_x =MIL.MbufInquire(ComponentId, MIL.M_3D_SCALE_X)
   resolution_y =MIL.MbufInquire(ComponentId, MIL.M_3D_SCALE_Y)
   resolution_z =MIL.MbufInquire(ComponentId, MIL.M_3D_SCALE_Z)
   
   # get the range image array
   host_address = MIL.MbufInquire(ComponentId, MIL.M_HOST_ADDRESS)
   host_address_ptr = ctypes.cast(host_address, ctypes.POINTER(ctypes.c_uint16))
   image_array = np.ctypeslib.as_array(host_address_ptr, (size_y, size_x))

   # create an empty point cloud
   pointcloud = np.zeros((size_y * size_x, 3), dtype=np.float32)

   # fill the point cloud
   for y in range(size_y):
      for x in range(size_x):
         if image_array[y, x] != 0:
            pointcloud[y * size_x + x, 0] = (x * resolution_x) + offset_x
            pointcloud[y * size_x + x, 1] = (y * resolution_y) + offset_y
            pointcloud[y * size_x + x, 2] = image_array[y, x] * resolution_z + offset_z

   # remove the points with a zero z value
   pointcloud = pointcloud[pointcloud[:,2] != 0.0]

   return pointcloud

def main():

   print("Allocating MIL objects...")

   # Allocate defaults.
   MilApplication = MIL.MappAlloc("M_DEFAULT", MIL.M_DEFAULT)
   MilSystem = MIL.MsysAlloc(MIL.M_DEFAULT, MIL.M_SYSTEM_DEFAULT, MIL.M_DEFAULT, MIL.M_DEFAULT)
   MilDigitizer = MIL.MdigAlloc(MilSystem, MIL.M_DEFAULT, "M_DEFAULT", MIL.M_DEFAULT)
   MilContainerDisp = MIL.MbufAllocContainer(MilSystem, MIL.M_PROC + MIL.M_DISP + MIL.M_GRAB, MIL.M_DEFAULT)
   
   ###############################
   # Set 3D sensor parameters
   ###############################

   # load default parameters
   MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_VALUE, "UserSetDefault", MIL.M_TYPE_STRING, "Profile")
   MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_EXECUTE, "UserSetLoad", MIL.M_DEFAULT, MIL.M_NULL)

   # exoposure time both cameras
   for i in range(2):
      MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_VALUE, "SourceSelector", MIL.M_TYPE_STRING, "Source0" if i == 0 else "Source1")
      MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_VALUE, "ExposureTime", MIL.M_TYPE_DOUBLE, np.array(500.0))

   # length
   MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_VALUE, "Scan3dVolumeLengthWorld", MIL.M_TYPE_DOUBLE, np.array(0.0))
   
   # laser power
   MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_VALUE, "LightLaserBrightness", MIL.M_TYPE_STRING, "100")
  
   # trigger
   MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_VALUE, "TriggerSelector", MIL.M_TYPE_STRING, "LineStart")
   MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_VALUE, "TriggerSource", MIL.M_TYPE_STRING, "Line0")
   MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_VALUE, "TriggerMode", MIL.M_TYPE_STRING, "On")
   MIL.MdigControlFeature(MilDigitizer, MIL.M_FEATURE_VALUE, "TriggerActivation", MIL.M_TYPE_STRING, "LevelHigh")

   print("3D sensor parameters set.")

   print("Ready to acquire")
   
   while(True):

      # start acquisition
      MIL.MdigGrab(MilDigitizer, MilContainerDisp)
     
      # wait for the end of the acquisition
      MIL.MdigGrabWait(MilDigitizer, MIL.M_GRAB_FRAME_END )

      # get the point cloud
      pointcloud = get_pointcloud(MilContainerDisp)

      # plot the point cloud in a 2D graph
      plt.plot(pointcloud[:,0], pointcloud[:,2], 'ro')
      # show the plot 1 sec
      plt.pause(0.001)
      # clear the plot
      plt.clf()
      
      # check if 'q' key is pressed
      if keyboard.is_pressed('q'):
        break

   # Release defaults.
   MIL.MbufFree(MilContainerDisp)
   MIL.MdigFree(MilDigitizer)
   MIL.MsysFree(MilSystem)
   MIL.MappFree(MilApplication)
      
if __name__ == "__main__":
   main()