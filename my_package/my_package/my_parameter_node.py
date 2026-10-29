import random
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import Int32

class MyParameterNode(Node):
    def __init__(self):
        super().__init__('my_parameter_node')
        # 1) 파라미터 선언 : 이름, 초깃값
        self.declare_parameter('qos_depth', 10)
        self.declare_parameter('min_random_num', 0)
        self.declare_parameter('max_random_num', 9)
        
        # 2) 파라미터 값 읽기
        qos_depth = self.get_parameter('qos_depth').value
        self.min_random_num = self.get_parameter('min_random_num').value
        self.max_random_num = self.get_parameter('max_random_num').value
        
        # 3) 값 변경 요청이 오면 update_parameter 호출
        self.add_on_set_parameters_callback(self.update_parameter)

        self.publisher = self.create_publisher(Int32, 'random_number', qos_depth)
        self.timer = self.create_timer(1.0, self.publish_random_number)

    def update_parameter(self, params):
        for param in params:
            if param.name == 'min_random_num' and param.type_ == Parameter.Type.INTEGER:
                self.min_random_num = param.value
            elif param.name == 'max_random_num' and param.type_ == Parameter.Type.INTEGER:
                self.max_random_num = param.value
        return SetParametersResult(successful=True)
 
    def publish_random_number(self):
        msg = Int32()
        msg.data = random.randint(self.min_random_num, self.max_random_num)
        self.publisher.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = MyParameterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()



    