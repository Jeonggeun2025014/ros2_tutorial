import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MyServiceServerNode(Node):
    def __init__(self):
        super().__init__('my_service_server_node')  # 노드 이름 등록

        # 'add_two_ints'라는 이름으로 서비스를 개설.
        # 요청이 들어오면 add_two_ints_callback이 자동으로 호출된다.
        self.add_two_ints_srv = self.create_service(
            AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        # 서비스를 새로 추가할 땐 위와 같은 create_service() 한 줄 + 아래 같은 콜백 메서드를 추가하면 됩니다.
        # self.other_srv = self.create_service(OtherType, 'other_service', self.other_callback)

    # request: 클라이언트가 보낸 요청 (a, b)
    # response: 여기에 결과를 채워서 return하면 클라이언트에게 전달됨
    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(
            f'Incoming request: a={request.a}, b={request.b}, sum={response.sum}')
        return response

    # def other_callback(self, request, response):
    #     ...
    #     return response

def main(args=None):
    rclpy.init(args=args)  # rclpy 초기화 (모든 ROS2 파이썬 프로그램의 시작점)
    my_service_server_node = MyServiceServerNode()

    # spin()이 계속 돌아야 서비스 요청을 받을 때마다 콜백이 호출된다 (Ctrl+C 전까지 대기)
    rclpy.spin(my_service_server_node)

    # 프로그램 종료 시 정리
    my_service_server_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
