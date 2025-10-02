import rclpy
import time
#Brings the ROS2 Python client library

import serial
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SerialToTwistNode(Node):
    # By writing (Node), we are inheriting from the Node class
    def __init__(self):
        super().__init__("serial_to_twist_node")
        #ROS2 graph is like a network of nodes, topics services, etc.. 
        #Each node must have a unique name

        self.publisher_ = self.create_publisher(Twist, "cmd_vel",10)
        #Messages of type Twist will be published to the "cmd_vel", with a queue size of 10
        #Can use self.create_publisher method as this belongs to the parent class Node

        self.serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        #Opens a serial connection to the Arduino, 9600 is the baud rate and timeout=1 means it will wait 1 second for data before giving up

        self.timer_ = self.create_timer(0.1,self.print_speeds)

    def print_speeds(self):
        #if self.serial_port.in_waiting > 0:
            #line = self.serial_port.readline().decode('utf-8').strip()
        line = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
        vel_parts = line.split(',')
        if len(vel_parts) == 2:
            msg = Twist()
            msg.linear.x = float(vel_parts[0]) * -1.0
            msg.angular.z = float(vel_parts[1])
            self.publisher_.publish(msg)
       
          
def main(args=None):
    rclpy.init(args=args)
    #Initialises ROS2 Python Client library
    #Sets up communication with the ROS graph
    #Must be called before creating any nodes

    node = SerialToTwistNode()
    #Instantiates class

    rclpy.spin(node)
    #Activates the node, allows it to process incoming messages and execute callbacks

    rclpy.shutdown()
    #Shuts down the ROS2 client library, cleans up resources
    #Clears ROS2 in that specific Python script.


if __name__ == '__main__':
    main()

