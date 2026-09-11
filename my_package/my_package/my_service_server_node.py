import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MyServiceServerNode(Node):
    def __init__(self):
        super().__init__('my_service_server_node')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}, sum={response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    my_service_server_node = MyServiceServerNode()
    rclpy.spin(my_service_server_node)
    my_service_server_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

