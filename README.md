# kLa Determination in an Airlift Reactor Using Image Analysis

This Python script implements a novel methodology to determine the volumetric mass transfer coefficient (**kLa**) in an Airlift reactor through image analysis.

## Features
- **Video to Frames Conversion**: Converts video recordings into individual frames for processing.
- **Processing**: Extracts centroids and areas of bubbles from the frames.
- **Calculations**: Computes bubble diameters, velocities, and ultimately **kLa** using the Higbie model.
- **Configuration**: Allows users to set experimental parameters such as:
  - Conversion factors
  - Diffusivity
  - Frame rate (**fps**)
  - Volume
  - Cropping coordinates

## Important Notes
- The **crop coordinates** and **conversion factor** must be adjusted when changing the internal column dimensions.  
- An **example image** is provided to illustrate the necessary modifications.  

This methodology enables precise and automated **kLa** estimation, facilitating the study of mass transfer in Airlift reactors.