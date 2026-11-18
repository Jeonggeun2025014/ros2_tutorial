import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry, Path
from std_srvs.srv import Trigger


def normalize_angle(angle):
    # 각도를 -pi ~ +pi 범위로 맞춰준다 (예: 350도 -> -10도)
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle


class PathFollowerNode(Node):
    """odom(현재 위치)과 square_path(목표 꼭짓점들)를 이용해 각도만 제어하고
    속도는 일정하게 유지하며 사각형을 따라 움직인다. 꼭짓점에 waypoint_tolerance
    이내로 가까워지면 다음 꼭짓점으로 넘어가고, 네 꼭짓점을 모두 돌면
    /get_next_path 서비스를 호출해 새로운 랜덤 경로를 요청한다.
    """

    def __init__(self):
        super().__init__('path_follower_node')

        self.init_parameters()
        self.init_variables()
        self.init_publishers()
        self.init_subscribers()
        self.init_clients()

        self.timer = self.create_timer(0.05, self.control_loop)  # 20Hz

    def control_loop(self):
        if self.path is None or self.waiting_for_new_path:
            self.cmd_vel_pub.publish(Twist())  # 정지
            return

        target = self.path.poses[self.target_index].pose.position
        dx = target.x - self.current_x
        dy = target.y - self.current_y
        distance = math.hypot(dx, dy)

        if distance < self.tolerance:
            self.target_index += 1
            if self.target_index >= len(self.path.poses):
                # 네 꼭짓점을 모두 돌았으므로 새 랜덤 경로 요청
                self.waiting_for_new_path = True
                self.send_next_path_request()
            self.cmd_vel_pub.publish(Twist())
            return

        target_yaw = math.atan2(dy, dx)
        yaw_error = normalize_angle(target_yaw - self.current_yaw)

        twist = Twist()
        twist.linear.x = self.linear_speed
        angular = self.angular_gain * yaw_error
        twist.angular.z = max(-self.max_angular_speed,
                               min(self.max_angular_speed, angular))
        self.cmd_vel_pub.publish(twist)

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        # 로봇이 z축으로만 회전하므로 (qx=qy=0), yaw는 이렇게 간단히 구해진다
        self.current_yaw = 2.0 * math.atan2(qz, qw)

    def path_callback(self, msg):
        self.path = msg
        self.target_index = 0
        self.waiting_for_new_path = False
        self.get_logger().info('New path received, starting from waypoint 0')

    def send_next_path_request(self):
        if not self.get_next_path_client.service_is_ready():
            self.get_logger().info('get_next_path service not available yet')
            return

        def response_callback(future):
            response = future.result()
            self.get_logger().info(f'get_next_path result: {response.message}')

        request = Trigger.Request()
        future = self.get_next_path_client.call_async(request)
        future.add_done_callback(response_callback)

    def init_parameters(self):
        self.declare_parameter('linear_speed', 0.5)
        self.declare_parameter('waypoint_tolerance', 0.1)
        self.declare_parameter('angular_gain', 2.0)
        self.declare_parameter('max_angular_speed', 1.5)

        self.linear_speed = self.get_parameter('linear_speed').value
        self.tolerance = self.get_parameter('waypoint_tolerance').value
        self.angular_gain = self.get_parameter('angular_gain').value
        self.max_angular_speed = self.get_parameter('max_angular_speed').value

    def init_variables(self):
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

        self.path = None            # 최근에 받은 Path (꼭짓점 리스트)
        self.target_index = 0       # 지금 향하고 있는 꼭짓점의 인덱스
        self.waiting_for_new_path = False  # 한 바퀴 다 돌고 새 경로를 기다리는 중

    def init_publishers(self):
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def init_subscribers(self):
        self.odom_sub = self.create_subscription(
            Odometry, 'odom', self.odom_callback, 10)
        self.path_sub = self.create_subscription(
            Path, 'square_path', self.path_callback, 10)

    def init_clients(self):
        self.get_next_path_client = self.create_client(Trigger, 'get_next_path')


def main(args=None):
    rclpy.init(args=args)
    node = PathFollowerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
