# identify the possible malicious connections in ROS

import os

def identify_message_type(message_name):
    # an keyword based way to do categorization. Not really accurate for now.
    stream = os.popen('rosmsg info %s'%str(message_name))
    output = stream.read()
    categories = ['odometry', 'state', 'map', 'reward', 'goal']
    result = []
    if 'odom' in output.lower():
        result.append('odometry')
    if 'map' in output or "grid" in output.lower():
        result.append('map')
    if 'state' in output.lower():
        result.append('state')
    if 'goal' in output.lower():
        result.append('goal')
    return result


# step 1: define the namespace for the compromised robot

namespace = "/robot_1" 

# step 2: use rostopic to list down all nodes.

stream = os.popen('rosnode list')
output = stream.read().split()

# step 3: find nodes subscribe to robot namespace publisher

malicious_subscriber_node = {}

for node in output:
    if namespace not in node: # we are not interested in internal communications 
        command = 'rosnode info %s'%node
        stream = os.popen(command)
        topic_info = stream.read().split('\n')
        # subscription information is in "Subscription section". 
        start = False
        topic_subscription_info = []
        for topic_line in topic_info:
            if "Subscriptions:" in topic_line:
                start = True
            if "Services:" in topic_line:
                start = False
            if start:
                if namespace in topic_line: # subscribe to malicious robot node
                    topic_subscription_info.append(topic_line)
        malicious_subscriber_node[node] = topic_subscription_info
                    

# remove the common ROS components that are not related to malicious robot: /rviz, /gazebo
malicious_subscriber_node.pop('/rviz', None)
malicious_subscriber_node.pop('/gazebo', None)
malicious_subscriber_node.pop('/gazebo_gui', None)
malicious_subscriber_node.pop('/rosout', None)

# print(malicious_subscriber_node)

# identify the message types from the topics to the nodes.

result = {}
for keyname in malicious_subscriber_node:
    result[keyname] = {}
    node_list = malicious_subscriber_node[keyname]
    for node_name in node_list:
        message_name = node_name[node_name.find('[')+1:-1]
        message_type = identify_message_type(message_name)
        result[keyname][message_name] = message_type

print(result)
    
    
        
    




