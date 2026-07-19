#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial ## for adding extra args into the function

## With OOPS:
 
 
class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__("add_two_ints_client") 
        self.client_ = self.create_client(AddTwoInts, "add_two_ints" )


    def call_add_two_ints(self, a, b):

        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Add Two Ints Server....")

        ## once service is found:
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.client_.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_add_two_ints, request=request))
        ## partial function used in above line


		## we get response from this callback function
    def callback_call_add_two_ints(self,future,request):
        response = future.result()
        #self.get_logger().info("Got response: " + str(response.sum))
        self.get_logger().info(str(request.a) + " + " 
                           + str(request.b) + " = " + str(response.sum))


 
 
def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClient()
    ## with one client we can send several requests to service server
    node.call_add_two_ints(3,7)
    node.call_add_two_ints(2,10)
    node.call_add_two_ints(5,90) 
    rclpy.spin(node) ## node needs to be spinning to get the response
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()

