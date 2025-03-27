import pymqi
import os

def get_env_variable(var_name):
    return os.getenv(var_name)

# Connection details - get values from environment variables
queue_manager = get_env_variable("QUEUE_MANAGER_NAME")       
channel = get_env_variable("CHANNEL_NAME") 
host = get_env_variable("HOST_NAME") 
port = get_env_variable("QUEUE_MANAGER_PORT_NUMBER") 
queue_name = get_env_variable("QUEUE_NAME") 


# MQ connection parameters
conn_info = f"{host}({port})"

# Create connection to the queue manager
try:
    # Initialize the connection
    qmgr = pymqi.connect(queue_manager, channel, conn_info)
    
    # Open the queue for putting messages
    queue = pymqi.Queue(qmgr, queue_name)
    
    # Put a message
    message = "Hello, IBM MQ!"
    queue.put(message)
    print(f"Message sent: {message}")
    
    # Close the queue and disconnect
    queue.close()
    qmgr.disconnect()
    print("Disconnected from IBM MQ.")

except pymqi.MQMIError as e:
    print(f"An error occurred: {e}")
