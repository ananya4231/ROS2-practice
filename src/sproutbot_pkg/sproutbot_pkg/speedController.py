import rclpy #importing top-level package

#Python doesn't import submodules so must also import Node class.
# .node is the submodule and .Node is the class within that submodule.

from rclpy.node import Node

#Twist is a message type and represents both linear and angular velocity.
from geometry_msgs.msg import Twist

class SpeedController(Node):
    def __init__(self):
        super().__init__("speed_controller")

        #Calls the constructor for the Node class and initialises a node with the name:
        # speed_controller, this is the name it is registered under for ROS2, and how other nodes will see it

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        #Creates a publisher object that will publish messages of type Twist to the topic 'cmd_vel
        #The '10' is the size of the message queue, if the subscriber is not receiving messages fast enough

        self.timer_ = self.create_timer(0.1,self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.5
        msg.angular.z = 0.01
        self.publisher_.publish(msg)
            #Creates a new Twist message object, sets the linear x velocity to 0.5 m/s and angular z velocity to 0.01 rad/s
            #Then publishes the message to the cmd_vel topic
    
def main(args=None):
    rclpy.init(args=args)
    #Initialises ROS2 Python Client library
    #Sets up communication with the ROS graph
    #Must be called before creating any nodes

    node = SpeedController()
    #Instantiates class

    rclpy.spin(node)
    #Activates the node, allows it to process incoming messages and execute callbacks

    node.destroy_node()
    #Destroys the node when it is no longer needed, and spin is interrupted
    #Node clears its own resources and unregisters from the ROS graph

    rclpy.shutdown()
    #Shuts down the ROS2 client library, cleans up resources
    #Clears ROS2 in that specific Python script.

if __name__ == '__main__':
    main()
        
        