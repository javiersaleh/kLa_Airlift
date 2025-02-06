from config import experiment_params, file_pattern, start, end
from processing import load_frames, process_frame, extract_properties
from calculations import compute_kLa

def main():
    # 1. Load the frames
    print("Loading frames...")
    frames = load_frames(file_pattern, start, end)
    print(f"Total frames loaded: {len(frames)}")

    # 2. Process frames (segmentation + property extraction)
    print("Processing frames...")
    frames_centroids_areas = {}
    for i, frame in enumerate(frames):
        segmented = process_frame(frame, experiment_params["crop_coords"])
        props = extract_properties(segmented, min_area=experiment_params["min_area"])
        frames_centroids_areas[i] = props

    # 3. Perform calculations (kLa, velocities, etc.)
    print("Calculating kLa and related parameters...")
    kLas, kLs, areas, velocities = compute_kLa(frames_centroids_areas, experiment_params)

    # 4. (Optional) Print some summary statistics
    #print(velocities)
    #print(areas)
    print(kLas)
    average = sum(kLas.values()) / len(kLas) if kLas else 0
    print(f"El promedio es: {average}")

if __name__ == "__main__":
    main()