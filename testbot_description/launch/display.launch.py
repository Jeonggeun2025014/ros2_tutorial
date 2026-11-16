"""URDF 를 RViz 에서 보는 launch 파일.

robot_state_publisher      : URDF 를 읽고, 관절값(/joint_states)으로 TF 를 계산해 발행
joint_state_publisher_gui  : 슬라이더로 관절값(/joint_states)을 만들어 준다
rviz2                      : 모델과 TF 를 화면에 표시
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('testbot_description')
    urdf_file = os.path.join(pkg, 'urdf', 'testbot.urdf')
    rviz_file = os.path.join(pkg, 'rviz', 'testbot.rviz')

    # URDF 파일을 문자열로 읽어서 파라미터로 전달한다
    with open(urdf_file, 'r', encoding='utf-8') as f:
        robot_description = f.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description,
                         'use_sim_time': False}],
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_file],
            output='screen',
        ),
    ])
