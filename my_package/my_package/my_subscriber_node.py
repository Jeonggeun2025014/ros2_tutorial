import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from std_msgs.msg import String

class MySubscriberNode(Node):
    def __init__(self):
        super().__init__('my_subscriber_node')
        self.subscription = self.create_subscription(
            Int32,
            'my_topic',
            self.subscriber_callback,
            10)
        self.string_subscription = self.create_subscription(
            String,
            'my_string_topic',
            self.string_subscriber_callback,
            10)
    
        self.subscription  # prevent unused variable warning
        self.string_subscription

    def subscriber_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

    def string_subscriber_callback(self, string_msg):
        self.get_logger().info(f'I heard: "{string_msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    my_subscriber_node = MySubscriberNode()
    rclpy.spin(my_subscriber_node)
    my_subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

