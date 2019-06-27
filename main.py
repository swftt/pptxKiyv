import numpy as np
import pptk
import json
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


def sample_polygon(V, num, eps=0.25):
    # samples polygon V s.t. consecutive samples are no greater than eps apart
    # assumes last vertex in V is a duplicate of the first
    M = np.ceil(np.sqrt(np.sum(np.diff(V, axis=0) ** 2, axis=1)) / eps)
    Q = []
    for (m, v1, v2) in zip(M, V[: -1], V[1:]):
        Q.append(np.vstack([
            np.linspace(v1[0], v2[0], m, endpoint=False),
            np.linspace(v1[1], v2[1], m, endpoint=False),
            np.linspace(num * 10, num * 10, m, endpoint=False)]).T)
    Q = np.vstack(Q)
    return Q


if __name__ == "__main__":
    with open('kyiv_counted_points.geojson', 'rb') as fd:
        data = json.load(fd)

    Vs = [np.array(F['geometry']['coordinates'][0]) for F in data['features']]
    Ws = [np.c_[V[:, 0].tolist(), V[:, 1].tolist()] for V in Vs]
    nums = [poly['properties']['NUMPOINTS'] for poly in data['features']]
    P = np.vstack([sample_polygon(W, num) for W, num in zip(Ws, nums)])
    P -= np.mean(P, axis=0)[None, :]
    v = pptk.viewer(P,  P[:, 2])
    v.set(point_size=1)
    v.color_map('summer')

