import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from std_msgs.msg import String
from rclpy.parameter import Parameter


class MyPublisherNode(Node):
    def __init__(self):
        super().__init__('my_publisher_node')
        self.publisher_ = self.create_publisher(Int32, 'my_topic', 10)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0

        self.declare_parameter('my_param1', 100)
        self.declare_parameter('my_param2.param2_1', 200)
        self.declare_parameter('my_param2.param2_2', 300)

        self.my_param1 = self.get_parameter('my_param1').value
        self.my_param2_1 = self.get_parameter('my_param2.param2_1').value
        self.my_param2_2 = self.get_parameter('my_param2.param2_2').value

    def timer_callback(self):
        msg = Int32()
        msg.data = self.count

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.get_logger().info(
            f'my_param1: {self.my_param1}, '
            f'my_param2.param2_1: {self.my_param2_1}, '
            f'my_param2.param2_2: {self.my_param2_2}')
        
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    my_publisher_node = MyPublisherNode()
    rclpy.spin(my_publisher_node)
    my_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

