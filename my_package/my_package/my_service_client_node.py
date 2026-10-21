import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MyServiceClientNode(Node):
    def __init__(self):
        super().__init__('my_service_client_node')  # 노드 이름 등록
        self.add_two_ints_client = self.create_client(AddTwoInts, 'add_two_ints')

        while not self.add_two_ints_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

    def send_add_two_ints_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        def response_callback(future):
            response = future.result()
            self.get_logger().info(f'Result: {response.sum}')

        future = self.add_two_ints_client.call_async(request)
        future.add_done_callback(response_callback)

def main(args=None):
    rclpy.init(args=args)  # rclpy 초기화 (모든 ROS2 파이썬 프로그램의 시작점)
    my_service_client_node = MyServiceClientNode()
    my_service_client_node.send_add_two_ints_request(int(sys.argv[1]), int(sys.argv[2]))
    rclpy.spin(my_service_client_node)
    my_service_client_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

