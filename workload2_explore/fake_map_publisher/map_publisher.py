#!/usr/bin/env python
import rospy
from nav_msgs.msg import OccupancyGrid

def callback(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    # publish the fake map
    pub = rospy.Publisher('/robot_1/map', OccupancyGrid, queue_size=5)
    data_list = [100]*len(data.data)
    data.data = tuple(data_list)
    pub.publish(data)
    
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('map_listener', anonymous=True)

    rospy.Subscriber("/robot_1/map", OccupancyGrid, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    

if __name__ == '__main__':
    listener()
