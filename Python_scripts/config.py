import numpy as np

experiment_params = {
    'conv_pix_mm': 55/520, #This one is variable depending on the relation for each internal tube
    'fps': 240, #Constant for this experiment
    'diffusivity': 2.6e-3, # mm^2/s
    'volume_total': 2.97e6,  # mm^3, Constant for this Airlift reactor
    'column_internal': 440 * np.pi / 4 * (32**2-28**2), #This one also variable, depending on the internal tube diameter
    'height_covered': (55/520)*(1250-20),
    'riser_width': 440, #Constant
    'crop_coords': (0, 420, 1250, 270),  # y, x, h, w
    "min_area": 20 #Constant
}
#need to change the following file_patern and the starting and final frame to analize
file_pattern = "C:/Users/javie/OneDrive/Documentos/paper/Videos/col28_fl10/frames_it1/frame{:03d}.PNG"
start = 500
end = 515
