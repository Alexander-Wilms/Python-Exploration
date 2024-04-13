import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

n_joints = 3


def forward_kinematics(
    joint_values: list[float],
) -> tuple[list[list[float]], list[list[float]]]:
    x = 0.0
    y = 0.0
    z = 0.0

    joint_coordinates = [[x, y, z]]
    joint_rotations = []

    for joint_idx in range(n_joints):
        theta = joint_values[joint_idx]
        u: float = np.sin(2 * theta)
        v: float = np.sin(3 * theta)
        w: float = np.cos(3 * theta)

        x += u
        y += v
        z += w

        joint_coordinates.append([x, y, z])
        joint_rotations.append([u, v, w])

    return joint_coordinates, joint_rotations


arrows = [[0, 0, 0]] * n_joints


def init_func() -> None:
    t = 0
    joint_coordinates, joint_rotations = forward_kinematics([0, np.cos(3 * t + math.pi / 3), t])
    for joint_idx in range(n_joints):
        arrows[joint_idx] = ax.quiver(*joint_coordinates[joint_idx], *joint_rotations[joint_idx])


def get_arrows_at_frame(frame: int) -> None:
    t = frame / 60
    joint_coordinates, joint_rotations = forward_kinematics([0, np.cos(3 * t + math.pi / 3), t])
    for joint_idx in range(n_joints):
        arrows[joint_idx].remove()
        arrows[joint_idx] = ax.quiver(*joint_coordinates[joint_idx], *joint_rotations[joint_idx])


fps = 30
interval = math.floor(1 / fps * 1000)
ani = FuncAnimation(fig, get_arrows_at_frame, frames=None, init_func=init_func, interval=interval)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(0, 2)
plt.show()
