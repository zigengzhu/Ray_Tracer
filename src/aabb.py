import numpy as np
import rtxRay as ry


class AABB:
    maximum: np.array
    minimum: np.array

    def __init__(self, minimum: np.array, maximum: np.array):
        self.minimum = minimum
        self.maximum = maximum

    def hit(self, r: ry.Ray, t_min: float, t_max: float):
        for a in range(0, 3):
            invD = 1.0 / r.direction[a]
            t0 = (self.minimum[a] - r.origin[a]) * invD
            t1 = (self.maximum[a] - r.origin[a]) * invD
            if invD < 0.0:
                temp = t0
                t0 = t1
                t1 = temp
            tmin: float
            tmax: float
            if t0 > t_min:
                tmin = t0
            else:
                tmin = t_min
            if t1 < t_max:
                tmax = t1
            else:
                tmax = t_max
            if tmax <= tmin:
                return False
        return True
