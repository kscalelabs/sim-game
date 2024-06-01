"""Defines the Stompy arm as an agent."""

from copy import deepcopy

import numpy as np
import sapien
from mani_skill.agents.base_agent import BaseAgent, Keyframe
from mani_skill.agents.controllers.pd_ee_pose import PDEEPoseControllerConfig
from mani_skill.agents.registration import register_agent

from simgame.config import get_model_dir


def deepcopy_dict(configs: dict) -> dict:
    assert isinstance(configs, dict), type(configs)
    ret = {}
    for k, v in configs.items():
        if isinstance(v, dict):
            ret[k] = deepcopy_dict(v)
        else:
            ret[k] = deepcopy(v)
    return ret


@register_agent("stompy_arm")
class StompyArm(BaseAgent):
    uid = "stompy_arm"
    urdf_path = f"{get_model_dir()}/stompy_arm/left_arm.urdf"

    urdf_config = {
        "_materials": {
            "gripper": {
                "static_friction": 2.0,
                "dynamic_friction": 2.0,
                "restitution": 0.0,
            },
        },
        "link": {
            "link_right_arm_1_hand_1_gripper_1": {
                "material": "gripper",
                "patch_radius": 0.1,
                "min_patch_radius": 0.1,
            },
            "link_right_arm_1_hand_1_gripper_2": {
                "material": "gripper",
                "patch_radius": 0.1,
                "min_patch_radius": 0.1,
            },
        },
    }

    startpos = [0.0, 0.0, 0.0]
    startorn = [0.0, 0.0, 0.0, 1.0]
    startrpy = [0.0, 0.0, 0.0]
    keyframes = dict(
        rest=Keyframe(
            pose=sapien.Pose(p=startpos, q=startorn),
            qpos=np.array([1.0, 1.0, 1.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0]),
        )
    )

    # fix_root_link = True
    # balance_passive_force = True
    # load_multiple_collisions = True

    arm_joint_names = [
        "joint_rmd_x8_90_mock_1_dof_x8",
        "joint_rmd_x8_90_mock_2_dof_x8",
        "joint_rmd_x4_24_mock_1_dof_x4",
        "joint_rmd_x4_24_mock_2_dof_x4",
        "joint_rmd_x4_24_mock_3_dof_x4",
        "joint_rmd_x4_24_mock_4_dof_x4",
        "joint_rmd_x4_24_mock_5_dof_x4",
        "joint_rmd_x4_24_mock_6_dof_x4",
    ]

    ee_link_name = "link_rmd_x4_24_mock_6_inner_rmd_x4_24_1"

    arm_stiffness = 1e3
    arm_damping = 1e2
    arm_force_limit = 100

    gripper_stiffness = 1e3
    gripper_damping = 1e2
    gripper_force_limit = 100

    @property
    def _controller_configs(self) -> dict:
        arm_pd_ee_delta_pose = PDEEPoseControllerConfig(
            joint_names=self.arm_joint_names,
            pos_lower=-0.1,
            pos_upper=0.1,
            rot_lower=-0.1,
            rot_upper=0.1,
            stiffness=self.arm_stiffness,
            damping=self.arm_damping,
            force_limit=self.arm_force_limit,
            ee_link=self.ee_link_name,
            urdf_path=self.urdf_path,
        )
        arm_pd_ee_target_delta_pose = deepcopy(arm_pd_ee_delta_pose)
        arm_pd_ee_target_delta_pose.use_target = True
        controller_configs = {"pd_ee_delta_pose": {"arm": arm_pd_ee_delta_pose}}

        # Make a deepcopy in case users modify any config
        return deepcopy_dict(controller_configs)
