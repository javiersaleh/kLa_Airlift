import numpy as np

def compute_kLa(frames_centroids_areas, params):
    """
        :param frames_centroids_areas: dict
        Dictionary where each key is a frame index and each value is another dict 
        of {label: (centroid, area)}.
    :param params: dict
        A dictionary of parameters, e.g.:
        {
            'conv_pix_mm': 55/520,
            'fps': 240,
            'diffusivity': 2.6e-3,
            'volume_total': 2.97e6,  # mm^3
            'column_internal': 440 * np.pi / 4 * (60**2 - 55**2),
            'height_covered': (55/520)*(1200-20),  # as in original snippet
            'riser_width': 440
        }

    :return: 
        kLas (dict): kLa value per frame,
        kLs (list): list of (centroid, kL),
        areas (list): total area per frame,
        velocities (list): list of (centroid, velocity).
    """
    conv_pix_mm = params['conv_pix_mm']
    fps = params['fps']
    diffusivity = params['diffusivity']
    volume_total = params['volume_total']
    column_internal = params['column_internal']
    height_covered = params['height_covered']
    riser_width = params['riser_width']

    # Derived quantities
    volume_reactor = volume_total - column_internal
    todo_riser = riser_width / height_covered

    # Output data structures
    kLas = {}
    kLs = []
    areas = []
    velocities = []

    # We iterate one less than total frames because we compare frame[i] with frame[i+1]
    for frame_idx in range(len(frames_centroids_areas) - 1):
        # Initialize per-frame accumulators
        kLa_local = 0
        area_local = 0
        recorrido = {}

        frame_inicial = frames_centroids_areas[frame_idx]
        frame_nuevo = frames_centroids_areas[frame_idx + 1]

        # For each bubble in the current frame, find a matching bubble in the next frame
        for i in frame_inicial:
            distancias = {}
            centroid_i, area_i = frame_inicial[i]

            for j in frame_nuevo:
                centroid_j, area_j = frame_nuevo[j]

                # Euclidean distance in 2D
                distance = np.linalg.norm(np.array(centroid_j) - np.array(centroid_i))
                # Vertical difference (assuming centroid_i[0] is 'y' coordinate)
                difference = centroid_i[0] - centroid_j[0]

                distancias[j] = (distance, difference)

            distancia_minima = 1e6
            label_min = None

            # Find the closest bubble under certain conditions
            for k in distancias.keys():
                dist_val, diff_val = distancias[k]
                # Original logic:
                # 1. dist_val < distancia_minima
                # 2. diff_val > 0
                # 3. dist_val > 4
                # 4. y coordinate of bubble > 20
                if (dist_val < distancia_minima and
                    diff_val > 0 and
                    dist_val > 4 and
                    centroid_i[0] > 20):
                    distancia_minima = dist_val
                    label_min = k

            if distancia_minima < 1e5:  
                # "Recorrido" stores the minimal distance found for this bubble
                recorrido[i] = distancia_minima

        # Now compute velocities, kL, and area contribution for each matched bubble
        for l in recorrido:
            distance_min_l = recorrido[l]
            centroid_l, area_l = frame_inicial[l]

            velocity = distance_min_l * conv_pix_mm * fps  # mm/s
            velocities.append((centroid_l, velocity))

            diameter = (area_l * (conv_pix_mm ** 2) * 4 / np.pi) ** 0.5  # mm
            #Higbie model aplication
            kL = 1.13 * (diffusivity * velocity / diameter) ** 0.5       # mm/s
            kLs.append((centroid_l, kL))

            # Interfacial specific area
            a = np.pi * (diameter ** 2) / volume_reactor  # mm^-1
            area_local += a

            # kLa_local increment (in h^-1)
            kLa_local += kL * a * 3600

        # Multiply by the "todo_riser" factor
        kLas[frame_idx] = kLa_local * todo_riser
        areas.append(area_local)

    return kLas, kLs, areas, velocities
