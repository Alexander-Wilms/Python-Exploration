"""
Forward kinematics for a 6 DOF robot arm

Based on https://github.com/Alexander-Wilms/Robotics-simulation/blob/master/Termin%202%20und%203/Durchf%C3%BChrung/C%2B%2BProjekt/Termin2u3/Termin2u3.cpp
"""

import math
from enum import Enum

import numpy as np
import pyarma as pa
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt


class JointType(Enum):
    ROT_X = 0
    ROT_Y = 1
    ROT_Z = 2
    TRANS_X = 3
    TRANS_Y = 4
    TRANS_Z = 5


class KinematicData:
    def __init__(self, joint_type, trans_x, trans_y, trans_z, rot_x, rot_y, rot_z):
        self.type = joint_type
        self.trans_x = trans_x
        self.trans_y = trans_y
        self.trans_z = trans_z
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.rot_z = rot_z


def vector_to_homogeneous_matrix(rot_x, rot_y, rot_z, trans_x, trans_y, trans_z):
    rot = np.array([rot_x, rot_y, rot_z])
    rotation = pr.active_matrix_from_intrinsic_euler_xyz(rot)
    translation = np.array([trans_x, trans_y, trans_z])
    T = pt.transform_from(rotation, translation)
    T = pa.mat(T)
    return T


def homogeneous_matrix_to_vector(T):
    T_np = np.array(T)
    euler_angles = pr.euler_from_matrix(T_np[0:3, 0:3], 0, 1, 2, False)
    translation = T_np[:3, 3]
    vector = pa.trans(pa.mat([*euler_angles, *translation]))
    return vector


def deg2rad(degree: float) -> float:
    radians = degree * 2 * math.pi / 360
    return radians


def forward_kinematics(robot: KinematicData, axes, qi: int = 0, qn: int = 5):
    """
    Calculates the forward kinematic from joint qi to qn
    """

    T = pa.eye(4, 4)
    # T.print("T:")
    Rot = pa.mat(3, 3)
    Transf = pa.mat(3, 1)

    # transformation due to joint rotation
    while qi < qn:
        match robot.type[qi]:
            case JointType.ROT_X:
                Rot = vector_to_homogeneous_matrix(deg2rad(axes[qi]), 0, 0, 0, 0, 0)
            case JointType.ROT_Y:
                Rot = vector_to_homogeneous_matrix(0, deg2rad(axes[qi]), 0, 0, 0, 0)
            case JointType.ROT_Z:
                Rot = vector_to_homogeneous_matrix(0, 0, deg2rad(axes[qi]), 0, 0, 0)
            case JointType.TRANS_X:
                Rot = vector_to_homogeneous_matrix(0, 0, 0, axes[qi], 0, 0)
            case JointType.TRANS_Y:
                Rot = vector_to_homogeneous_matrix(0, 0, 0, 0, axes[qi], 0)
            case JointType.TRANS_Z:
                Rot = vector_to_homogeneous_matrix(0, 0, 0, 0, 0, axes[qi])

        # transformation from one joint to the next
        Transf = vector_to_homogeneous_matrix(
            deg2rad(robot.rot_x[qi]),
            deg2rad(robot.rot_y[qi]),
            deg2rad(robot.rot_z[qi]),
            robot.trans_x[qi],
            robot.trans_y[qi],
            robot.trans_z[qi],
        )

        T = T * Rot
        T = T * Transf

        qi += 1

    return T


if __name__ == "__main__":
    joint_type = [
        JointType.ROT_Z,
        JointType.ROT_Y,
        JointType.ROT_Y,
        JointType.ROT_Z,
        JointType.ROT_Y,
        JointType.ROT_Z,
    ]
    trans_x = [100, 265, 270, 0, 0, 0]
    trans_y = [0, 0, 0, 0, 0, 0]
    trans_z = [350, 0, 0, 0, 75, 0]
    rot_x = [0, 0, 0, 0, 0, 0]
    rot_y = [0, 0, 90, 0, 0, 0]
    rot_z = [0, 0, 0, 0, 0, 0]
    robot = KinematicData(joint_type, trans_x, trans_y, trans_z, rot_x, rot_y, rot_z)

    # rotation and location of Tool Center Point
    print("► x -> to homogeneous transformation matrix -> T -> to vector -> x")
    x = pa.trans(pa.mat([0, 0, 0, 1, 2, 3]))
    x.print("x:")
    T = vector_to_homogeneous_matrix(*x)
    T.print("T:")
    x = homogeneous_matrix_to_vector(T)
    x.print("v:")

    print("► joint values q -> forward kinematics -> transformation matrix")
    joint_values = pa.trans(pa.mat([0.0, -142.65, 96.1763, 0.0, 51.4737, 0.0]))
    joint_values.print("joint_values:")
    T = forward_kinematics(robot, joint_values)
    T.print("T:")
