import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    param_file = os.path.join(
        get_package_share_directory('square_patrol'),
        'param',
        'square_patrol_params.yaml')

    return LaunchDescription([
        Node(
            package='square_patrol',
            executable='robot_simulator_node',
            name='robot_simulator_node',
            output='screen'),
        Node(
            package='square_patrol',
            executable='path_manager_node',
            name='path_manager_node',
            output='screen',
            parameters=[param_file]),
        Node(
            package='square_patrol',
            executable='path_follower_node',
            name='path_follower_node',
            output='screen',
            parameters=[param_file]),
        # rviz2는 설정 파일 없이 띄움. 실행 후 아래를 직접 추가해서 확인:
        #   Global Options -> Fixed Frame: odom
        #   Add -> By topic -> /odom -> Odometry
        #   Add -> By topic -> /square_path -> Path
        #   Add -> By display type -> TF
        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'),
    ])


