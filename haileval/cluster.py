import numpy as np
from scipy.spatial.distance import pdist, squareform


def cluster_storms(coords, max_dist):
    dist_matrix = squareform(pdist(coords))
    all_dist_matrix = np.array(dist_matrix[:, :])
    mask_dist = max_dist + 1
    dist_matrix[np.triu_indices(dist_matrix.shape[0])] = mask_dist
    dist_matrix[dist_matrix > max_dist] = mask_dist
    unclustered = list(range(coords.shape[0]))
    clusters = {}
    c_num = 0
    while dist_matrix.min() < mask_dist:
        pair = np.unravel_index(np.argmin(dist_matrix), dist_matrix.shape)
        if pair[0] in unclustered and pair[1] in unclustered:
            for p in pair:
                if len(clusters) > 0:
                    min_cluster_dist = mask_dist + 1
                    closest_cluster = -1
                    for c_key in clusters.keys():
                        c_dist = all_dist_matrix[p, clusters[c_key]].min()
                        if c_dist < min_cluster_dist:
                            min_cluster_dist = c_dist
                            closest_cluster = c_key
                    if min_cluster_dist <= max_dist:
                        clusters[closest_cluster].append(p)
                    else:
                        clusters[c_num] = [p]
                        c_num += 1
                else:
                    clusters[c_num] = [p]
                    c_num += 1
                unclustered.remove(p)
        elif pair[0] in unclustered and pair[1] not in unclustered:
            for c_key in clusters.keys():
                if pair[1] in clusters[c_key]:
                    clusters[c_key].append(pair[0])
            unclustered.remove(pair[0])
        elif pair[1] in unclustered and pair[0] not in unclustered:
            for c_key in clusters.keys():
                if pair[0] in clusters[c_key]:
                    clusters[c_key].append(pair[1])
            unclustered.remove(pair[1])

        dist_matrix[pair] = mask_dist
    for c in unclustered:
        clusters[c_num] = c
        c_num += 1
    cluster_array = np.zeros(coords.shape[0])
    for cluster_num, indices in clusters.items():
        cluster_array[indices] = cluster_num
    return cluster_array


def merge_storm_clusters():
    return
