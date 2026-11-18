import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster


class RobotSimulatorNode(Node):
    def __init__(self):
        super().__init__('robot_simulator_node')

        self.init_variables()
        self.init_publishers()
        self.init_subscribers()

        self.timer = self.create_timer(self.dt, self.update_state)

    def update_state(self):
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

    def cmd_vel_callback(self, msg):
        self.linear_x = msg.linear.x
        self.angular_z = msg.angular.z

    def init_variables(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.linear_x = 0.0
        self.angular_z = 0.0

        self.dt = 0.05

    def init_publishers(self):
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

    def init_subscribers(self):
        self.cmd_vel_sub = self.create_subscription(
            Twist, 'cmd_vel', self.cmd_vel_callback, 10)


def main(args=None):
    rclpy.init(args=args)
    node = RobotSimulatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
