import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


# ros2 launch가 호출하는 진입점. 여기서 반환한 LaunchDescription 안에 담긴
# 액션(Node 등)들이 한꺼번에 실행된다.
def generate_launch_description():
    # 빌드 후 설치된 param/example.yaml의 절대 경로를 구함
    # (설치 경로: install/my_package/share/my_package/param/example.yaml)
    param_file = os.path.join(
        get_package_share_directory('my_package'),
        'param',
        'example.yaml')

    return LaunchDescription([
        # my_package 패키지의 my_publisher_node 실행 파일을 하나의 프로세스로 띄움
        # (ros2 run my_package my_publisher_node 와 동일한 효과)
        Node(
            package='my_package',
            executable='my_publisher_node',
            name='my_publisher_node',
            output='screen',  # 노드의 로그(get_logger)를 터미널 화면에 바로 출력
            parameters=[param_file]),  # yaml에 선언된 파라미터 값을 초깃값으로 적용

        # my_subscriber_node도 같은 방식으로 별도 프로세스로 띄움
        # 리스트에 담긴 Node들은 launch가 동시에(병렬로) 실행시킨다
        Node(
            package='my_package',
            executable='my_subscriber_node',
            name='my_subscriber_node',
            output='screen'),
    ])

