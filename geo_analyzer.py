import math
import numpy as np

def geo_params(geom) :
    """
Returns a tuple with the following.
ring plane angle in degrees (0 is parallel)
ring center offsets, ring 2's center from ring 1 first
distance from the magnesium atoms to the line going through the centers of the rings
parallel offsets of the magnesium atoms to their respective rings
absolute error of each ring from the ideal plane
horizontal offsets of each magnesium atom to each carbon in its ring.
"""
    r1 = np.array([g[1:] for g in geom[:5]])
    r2 = np.array([g[1:] for g in geom[5:10]])
    mg1 = np.array(geo[-2][1:])
    mg2 = np.array(geo[-1][1:])
    c1 = sum(r for r in r1) / len(r1)
    c2 = sum(r for r in r2) / len(r2)
    coefs1, alpha1, _ = plane_params(r1, 0)
    coefs2, alpha2, _ = plane_params(r2, 0)
    r1_norm = np.array([-1, coefs1[0], coefs1[1]])
    r2_norm = np.array([-1, coefs2[0], coefs2[1]])
    r1_norm /= np.linalg.norm(r1_norm)
    r2_norm /= np.linalg.norm(r2_norm)
    alpha = (180 / math.pi) * math.acos(np.dot(r1_norm, r2_norm))
    delta1 = np.linalg.norm(np.dot(c1 - c2, r1_norm) / np.dot(r1_norm, r2_norm) * r2_norm - c1 + c2)
    delta2 = np.linalg.norm(np.dot(c2 - c1, r2_norm) / np.dot(r1_norm, r2_norm) * r1_norm - c2 + c1)
    mg1offset = np.linalg.norm(mg1 - np.dot(mg1, c2 - c1) / np.linalg.norm(c2 - c1) * (c2 - c1))
    mg2offset = np.linalg.norm(mg2 - np.dot(mg2, c2 - c1) / np.linalg.norm(c2 - c1) * (c2 - c1))
    mgdel1 = np.linalg.norm(mg1 - np.dot(mg1, r1_norm) * r1_norm)
    mgdel2 = np.linalg.norm(mg2 - np.dot(mg2, r2_norm) * r2_norm)
    abserr1 = sum(abs(r[0] - coefs1[0] * r[1] - coefs1[1] * r[2] - alpha1) for r in r1) / len(r1)
    abserr2 = sum(abs(r[0] - coefs2[0] * r[1] - coefs2[1] * r[2] - alpha2) for r in r2) / len(r2)
    r1_diff = [np.linalg.norm(mg1 - np.dot(mg1, r1_norm) * r1_norm - r) for r in r1]
    r2_diff = [np.linalg.norm(mg2 - np.dot(mg2, r2_norm) * r2_norm - r) for r in r2]
    return (alpha, delta1, delta2, mg1offset, mg2offset, mgdel1, mgdel2, abserr1, abserr2, r1_diff, r2_diff)
