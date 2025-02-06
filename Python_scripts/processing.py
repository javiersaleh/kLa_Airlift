from skimage import io, color
from skimage.filters import threshold_otsu
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage as ndi
import numpy as np

def load_frames(path_pattern, start, end):
    """
    Load a series of image frames based on a file naming pattern.
    """
    frames = []
    for i in range(start, end):
        file_name = path_pattern.format(i)
        frames.append(io.imread(file_name))
    return frames

def process_frame(frame, crop_coords):
    """
    Crop, convert to grayscale, binarize, and apply watershed segmentation.
    Returns a segmented (labeled) image of the same size as the cropped frame.
    """
    y, x, h, w = crop_coords
    cropped_frame = frame[y:y+h, x:x+w]

    # Convert to grayscale and binarize
    gray = color.rgb2gray(cropped_frame)
    thresh = threshold_otsu(gray)
    binary = gray > thresh

    # Distance transform
    distance = ndi.distance_transform_edt(binary)

    # Find local maxima (coordinates)
    coords = peak_local_max(distance, footprint=np.ones((3, 3)), labels=binary)

    # Create a boolean mask of the same shape as 'distance'
    mask_peaks = np.zeros(distance.shape, dtype=bool)
    mask_peaks[tuple(coords.T)] = True

    # Label those maxima => markers must be 2D, same shape as distance
    markers, _ = ndi.label(mask_peaks)

    # Watershed segmentation
    segmented = watershed(-distance, markers, mask=binary)
    return segmented

def extract_properties(segmented_frame, min_area=20):
    """
    Extract region properties (centroids and areas) from a segmented frame.
    """
    from skimage.measure import regionprops
    properties = {}
    for region in regionprops(segmented_frame):
        if region.area >= min_area:
            properties[region.label] = (region.centroid, region.area)
    return properties