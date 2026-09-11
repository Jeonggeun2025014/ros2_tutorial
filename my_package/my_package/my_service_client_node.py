import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MyServiceClientNode(Node):
    def __init__(self):
        super().__init__('my_service_client_node')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.request = AddTwoInts.Request()

    def send_request(self, a, b):
        self.request.a = a
        self.request.b = b
        self.future = self.client.call_async(self.request)

def main(args=None):
    rclpy.init(args=args)
    my_service_client_node = MyServiceClientNode()

    my_service_client_node.send_request(int(sys.argv[1]), int(sys.argv[2]))
    rclpy.spin_until_future_complete(my_service_client_node, my_service_client_node.future)
    response = my_service_client_node.future.result()    
    my_service_client_node.get_logger().info(f'Result: {response.sum}')

    my_service_client_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

