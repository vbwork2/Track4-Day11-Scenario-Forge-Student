"""Part B: physics check. TODO 3."""
from __future__ import annotations

G = 9.81


def is_feasible(p: dict) -> bool:
    """TODO 3. False for scenarios no real road user could produce. Reject if ANY of:

    - the lane change needs more sideways grip than the road has: the cosine lane change of 3.5 m over
      p["cutDur"] seconds peaks at a_lat = (pi / cutDur)^2 * 3.5 / 2; reject if a_lat > mu * g;
    - the post-merge braking p["cutBrake"] exceeds mu * g;
    - the pedestrian runs: p["pedV"] > 2.5 m/s;
    - the cut-in speed p["cutV"] is not in (0, 22] m/s.
    mu is p["mu"]. A search that keeps infeasible scenarios reports failures that cannot happen.
    """
    try:
        mu = float(p["mu"])
        cut_dur = float(p["cutDur"])
        cut_brake = float(p["cutBrake"])
        ped_v = float(p["pedV"])
        cut_v = float(p["cutV"])
    except (KeyError, TypeError, ValueError):
        return False
    if cut_dur <= 0 or mu < 0:
        return False
    grip = mu * G
    lateral_accel = (3.141592653589793 / cut_dur) ** 2 * 3.5 / 2
    return not (lateral_accel > grip or cut_brake > grip or ped_v > 2.5 or not (0 < cut_v <= 22))
