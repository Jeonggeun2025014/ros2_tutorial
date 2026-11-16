# testbot_description

3축 매니퓰레이터 URDF 실습 패키지 (ament_python). 4차시 자료와 함께 사용.

## 빌드와 실행
    cd ~/ros2_ws && colcon build --packages-select testbot_description
    source install/setup.bash
    ros2 launch testbot_description display.launch.py

## 설치가 필요한 패키지 (배포판 이름 예: humble)
    sudo apt install ros-$ROS_DISTRO-joint-state-publisher-gui ros-$ROS_DISTRO-robot-state-publisher ros-$ROS_DISTRO-rviz2 liburdfdom-tools

## 확인
    check_urdf install/testbot_description/share/testbot_description/urdf/testbot.urdf
    ros2 run tf2_tools view_frames

ROS 2 에서 실행해 보지 않았고 XML/문법만 검사했습니다.
원본 예제: OpenRT(OROCA) URDF 글, CC BY 4.0
