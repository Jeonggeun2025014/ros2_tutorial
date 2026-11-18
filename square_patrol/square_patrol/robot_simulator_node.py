import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster


def euler_to_quaternion(roll, pitch, yaw):
    # roll(x축 회전), pitch(y축 회전), yaw(z축 회전)를 쿼터니언(x,y,z,w)으로 변환하는
    # 일반 공식. 이 로봇은 평면 위에서만 움직이므로 roll=pitch=0으로 호출된다.
    cr = math.cos(roll / 2.0)
    sr = math.sin(roll / 2.0)
    cp = math.cos(pitch / 2.0)
    sp = math.sin(pitch / 2.0)
    cy = math.cos(yaw / 2.0)
    sy = math.sin(yaw / 2.0)

    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    qw = cr * cp * cy + sr * sp * sy
    return qx, qy, qz, qw


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

        # roll=0, pitch=0, yaw=self.theta (평면 이동이라 z축으로만 회전)
        qx, qy, qz, qw = euler_to_quaternion(0.0, 0.0, self.theta)

        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.x = qx
        odom.pose.pose.orientation.y = qy
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
        t.transform.rotation.x = qx
        t.transform.rotation.y = qy
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

