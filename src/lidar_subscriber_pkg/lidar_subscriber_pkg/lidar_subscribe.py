import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class LidarSubscribe(Node):

    def __init__(self):
        super().__init__("lidar_subscriber")
        #Subscribing to lidar readings
        self.subscription = self.create_subscription(LaserScan,"/scan",self.scan_callback,10)

        #Publishing velocities based on readings
        self.publisher = self.create_publisher(Twist,"/cmd_vel",10)
        self.leftTurnCount = 0
        self.rightTurnCount = 0

    def turnTurtle(self,currentAngular,minLeftDistance, minRightDistance):
        if(minLeftDistance < minRightDistance):
            self.rightTurnCount = self.rightTurnCount + 1
            return currentAngular - 1
        else:
            self.leftTurnCount = self.leftTurnCount + 1
            return currentAngular + 1


    #msg containing all the values is directly passed into the callback function by ROS2
    def scan_callback(self,msg):

        #Filtering out 0 and positive infinity
        values = [r for r in msg.ranges if r>0 and r<float("inf")]

        #Getting +/- 30 degrees from the middle to check for obstacles in front of the robot
        front_values = msg.ranges[0:45] + msg.ranges[315:360]

        #self.get_logger().info(f"Scan length: {len(msg.ranges)}")

        left_values = msg.ranges[45:135]
        right_values = msg.ranges[225:315]
        back_values = msg.ranges[135:225]


        #Determining obstacle closest to robot
        minFrontDistance = min(front_values)
        minLeftDistance = min(left_values)
        minRightDistance = min(right_values)
        minBackDistance = min(back_values)


        #Changing speed based on distance to closest obstacle
        speedVal = Twist()

        if(minFrontDistance <0.4):
            speedVal.linear.x = 0.0
            speedVal.angular.z = self.turnTurtle(speedVal.angular.z,minLeftDistance, minRightDistance)
            if(self.leftTurnCount + self.rightTurnCount > 4):
                speedVal.linear.x = -0.05
                self.leftTurnCount = 0
                self.rightTurnCount = 0
            if(minBackDistance <0.4):
                speedVal.linear.x = -0.01
        else:
            speedVal.linear.x = 0.5
        
        #elif(minFrontDistance <1.0):
        #    speedVal.linear.x = 0.3
        #    speedVal.angular.z = self.turnTurtle(speedVal.angular.z,minLeftDistance, minRightDistance)
        #    if(minBackDistance <0.4):
        #        speedVal.linear.x = -0.01                
    
        self.publisher.publish(speedVal)
    
    
def main(args=None):
    rclpy.init(args=args)
    #Initialises ROS2 Python Client library
    #Sets up communication with the ROS graph
    #Must be called before creating any nodes

    node = LidarSubscribe()
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


