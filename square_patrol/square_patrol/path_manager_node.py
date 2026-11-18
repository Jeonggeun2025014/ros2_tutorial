import random

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from std_srvs.srv import Trigger


class PathManagerNode(Node):
    """한 변의 길이가 side_length인 정사각형의 네 꼭짓점을 임의의 순서로 섞어
    nav_msgs/Path로 발행한다. /get_next_path 서비스가 호출되면 다시 섞어서 새로
    발행한다 (한 바퀴를 다 돌고 나면 path_follower_node가 이 서비스를 호출한다).
    """

    def __init__(self):
        super().__init__('path_manager_node')

        self.init_parameters()
        self.init_variables()
        self.init_publishers()
        self.init_services()

        self.publish_random_path()

    def publish_random_path(self):
        order = self.corners.copy()
        random.shuffle(order)

        path = Path()
        path.header.frame_id = 'odom'
        path.header.stamp = self.get_clock().now().to_msg()

        for x, y in order:
            pose = PoseStamped()
            pose.header.frame_id = 'odom'
            pose.pose.position.x = x
            pose.pose.position.y = y
            path.poses.append(pose)

        self.path_pub.publish(path)
        self.get_logger().info(f'New path: {order}')

    def get_next_path_callback(self, request, response):
        self.publish_random_path()
        response.success = True
        response.message = 'New random path published'
        return response

    def init_parameters(self):
        self.declare_parameter('side_length', 2.0)
        self.side_length = self.get_parameter('side_length').value

    def init_variables(self):
        # 정사각형 네 꼭짓점 좌표 (좌표 자체는 고정, 방문 순서만 매번 랜덤하게 섞임)
        side = self.side_length
        self.corners = [
            (0.0, 0.0),
            (side, 0.0),
            (side, side),
            (0.0, side),
        ]

    def init_publishers(self):
        self.path_pub = self.create_publisher(Path, 'square_path', 10)

    def init_services(self):
        self.get_next_path_srv = self.create_service(
            Trigger, 'get_next_path', self.get_next_path_callback)


def main(args=None):
    rclpy.init(args=args)
    node = PathManagerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
