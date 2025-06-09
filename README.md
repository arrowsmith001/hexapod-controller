# Hexapod Controller

Code for controlling a hexapod.

## Features

**Open-ended autonomous movement:** any "gait" can be defined by expressing it as a set of non-overlapping scheduled leg motions. Motions can be lines or Bezier curves. Motions are vectors that apply to the foot of a specified leg in world space. IK calculations are performed ahead of time to transform these into sequences of angles.

**Ripple Gait example:**

![Image](https://github.com/user-attachments/assets/6b5a8747-70fe-453b-aac7-3ad592ad6dc0)

**Tripod Gait (left turn) example:**

![Image](https://github.com/user-attachments/assets/02ffb4ed-c9e8-44b5-833b-754daf3c5851)

## How to use

1. Configure the dimensions and resting angles of a real (or virtual) hexapod.
2. Define "gaits" as a sequence of vectors that transform foot positions in 3D space.
3. Apply gaits to a configured hexapod
```
hexapod.add_gait("walk", my_gait)
```
4. Execute code such as the following in `main.py`:
```
hexapod.set_active_gait("walk")

while True:
    t = 0
    while t < hexapod.get_active_gait().duration:
        hexapod.set_angles_at(t)
        t += dt
        time.sleep(dt)
```

## Upcoming

- [ ] Interactive calibration routine
- [ ] Teleoperated movement
- [ ] Sensors
