# py2

# python3
import pickle
import rospy
from std_msgs.msg import String
from nav_msgs.msg import OccupancyGrid
import numpy as np
import matplotlib.pyplot as plt


def load_map(map_name="house_map.pickle"):
    file_to_read = open(map_name, "rb")
    loaded_object = pickle.load(file_to_read)
    file_to_read.close()
    return loaded_object

def callback(data):

    # try to store the data into a file that we can constantly recall.
    map_to_store = open("test.pickle", "wb")
    pickle.dump(data, map_to_store)
    map_to_store.close()
    print("map stored")
    
    #my_map = np.asarray(data.data)
    #my_map = np.reshape(my_map, (int(data.info.width), int(data.info.height)))



def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/map_merge/map", OccupancyGrid, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def draw_map(map_1, map_2):
    #plt.figure(1)
    #plt.imshow(map_1)
    #plt.colorbar()
    #plt.show()


    plt.figure(2)
    plt.imshow(map_2)
    plt.colorbar()
    plt.show()


if __name__ == '__main__':
    # pre-processing 
    #listener()
    map_o1 = load_map()
    map_o2 = load_map('test.pickle')
    map_1 = np.asarray(map_o1.data)
    map_1 = np.reshape(map_1, (int(map_o1.info.width), int(map_o1.info.height)))
    map_2 = np.asarray(map_o2.data)
    map_2 = np.reshape(map_2, (int(map_o2.info.height), int(map_o2.info.width)))
    draw_map(map_1, map_2)
    
    

#print(test_map.shape)
#plt.imshow(standard_region)
#plt.colorbar()
#plt.show()

#print(np.sum(test_map==standard_region))

# plot the two figures below
'''
plt.figure(1)
plt.imshow(my_map[128:223,128:224])
plt.colorbar()
plt.show()


plt.figure(2)
plt.imshow(test_map)
plt.colorbar()
plt.show()

'''
