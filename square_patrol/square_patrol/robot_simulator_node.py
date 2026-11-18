import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster


class RobotSimulatorNode(Node):
    """cmd_vel(Twist)을 받아 로봇 위치(x, y, theta)를 적분하고,
    그 결과를 odom(Odometry)과 tf(odom -> base_link)로 내보내는 가상 로봇.
    실제 로봇/Gazebo 없이 평면 위에서 움직이는 점으로 로봇을 흉내낸다.
    """

    def __init__(self):
        super().__init__('robot_simulator_node')

        # 로봇의 현재 상태 (평면 위 위치 x, y와 진행 방향 theta)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # 가장 최근에 받은 속도 명령 (안 받으면 멈춰있음)
        self.linear_x = 0.0
        self.angular_z = 0.0

        self.cmd_vel_sub = self.create_subscription(
            Twist, 'cmd_vel', self.cmd_vel_callback, 10)
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.dt = 0.05  # 20Hz 로 위치를 갱신
        self.timer = self.create_timer(self.dt, self.update_state)

    def cmd_vel_callback(self, msg):
        self.linear_x = msg.linear.x
        self.angular_z = msg.angular.z

    def update_state(self):
        # 단순 유니사이클 모델: 직진 속도(linear_x)와 회전 속도(angular_z)로
        # 매 dt마다 위치/방향을 적분
        self.x += self.linear_x * math.cos(self.theta) * self.dt
        self.y += self.linear_x * math.sin(self.theta) * self.dt
        self.theta += self.angular_z * self.dt

        now = self.get_clock().now().to_msg()

        # z축 회전만 있으므로 쿼터니언은 간단히 계산 가능 (qx=qy=0)
        qz = math.sin(self.theta / 2.0)
        qw = math.cos(self.theta / 2.0)

        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw
        odom.twist.twist.linear.x = self.linear_x
        odom.twist.twist.angular.z = self.angular_z
        self.odom_pub.publish(odom)

        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = RobotSimulatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
