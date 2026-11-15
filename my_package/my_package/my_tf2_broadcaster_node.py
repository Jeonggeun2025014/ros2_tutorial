import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class MyTf2BroadcasterNode(Node):
    def __init__(self):
        super().__init__('my_tf2_broadcaster_node')

        # tf를 내보내는(broadcast) 객체. publisher와 비슷한 역할이지만
        # 일반 토픽이 아니라 /tf라는 전용 토픽으로 좌표 변환 정보를 보낸다.
        self.tf_broadcaster = TransformBroadcaster(self)

        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(0.1, self.broadcast_transform)

    def broadcast_transform(self):
        elapsed_sec = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        # TransformStamped: "어떤 좌표계(frame_id) 기준으로, 어떤 좌표계(child_frame_id)가
        # 어디에(translation) 어떤 방향(rotation)으로 있는지"를 담는 메시지
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'       # 부모 좌표계
        t.child_frame_id = 'my_frame'     # 자식 좌표계 (world 기준 위치를 알려줄 대상)

        # world 원점을 중심으로 반지름 1인 원을 그리며 도는 좌표를 계속 보냄
        t.transform.translation.x = math.cos(elapsed_sec)
        t.transform.translation.y = math.sin(elapsed_sec)
        t.transform.translation.z = 0.0

        # 회전 없음 (단위 쿼터니언: 회전이 전혀 없을 때의 고정값)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = MyTf2BroadcasterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

