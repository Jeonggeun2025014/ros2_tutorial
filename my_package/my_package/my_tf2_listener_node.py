import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class MyTf2ListenerNode(Node):
    def __init__(self):
        super().__init__('my_tf2_listener_node')

        # Buffer: 여러 broadcaster로부터 받은 tf들을 시간순으로 모아두는 저장소
        # TransformListener: /tf, /tf_static 토픽을 구독해서 Buffer를 채워주는 역할
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.timer = self.create_timer(1.0, self.lookup_transform)

    def lookup_transform(self):
        try:
            # 'world' 기준으로 'my_frame'이 현재 어디 있는지 조회
            t = self.tf_buffer.lookup_transform('world', 'my_frame', Time())
        except TransformException as ex:
            # broadcaster가 아직 안 떴거나 tf가 아직 도착하지 않은 경우
            self.get_logger().info(f'Could not get transform: {ex}')
            return

        self.get_logger().info(
            f'my_frame position -> x: {t.transform.translation.x:.2f}, '
            f'y: {t.transform.translation.y:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = MyTf2ListenerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


