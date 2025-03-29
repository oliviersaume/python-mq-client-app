import pymqi
import os
import time

def get_env_variable(var_name):

    return os.getenv(var_name)

def get_env_variable_optional(var_name,default_value):
    try:
      # Try to get the environment variable 'MY_VARIABLE'
      return os.getenv(var_name)
    except KeyError:
      # If 'MY_VARIABLE' is not found, use 'default_value'
      return default_value
    

# Connection details - get values from environment variables
queue_manager = get_env_variable("QUEUE_MANAGER_NAME")       
channel = get_env_variable("CHANNEL_NAME") 
host = get_env_variable("HOST_NAME") 
port = get_env_variable("QUEUE_MANAGER_PORT_NUMBER") 
queue_name = get_env_variable("QUEUE_NAME") 
getwait_interval = get_env_variable_optional("GETWAIT_INTERVAL",60) 

conn_info = '%s(%s)' % (host, port)


# Message Descriptor
md = pymqi.MD()

# Get Message Options
gmo = pymqi.GMO()
gmo.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
gmo.WaitInterval = 5000 # 5 seconds

qmgr = pymqi.connect(queue_manager, channel, conn_info)
queue = pymqi.Queue(qmgr, queue_name)

keep_running = True

while keep_running:
    try:
        # Wait up to to gmo.WaitInterval for a new message.
        message = queue.get(None, md, gmo)

        # Process the message here..
        print(f"Message received: {message}")

        # Reset the MsgId, CorrelId & GroupId so that we can reuse
        # the same 'md' object again.
        md.MsgId = pymqi.CMQC.MQMI_NONE
        md.CorrelId = pymqi.CMQC.MQCI_NONE
        md.GroupId = pymqi.CMQC.MQGI_NONE

    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
            # No messages, that is OK, we can ignore it.
            print("No more mesage ... back to getwait mode")
            pass
        else:
            # Some other error condition.
            raise

queue.close()
qmgr.disconnect()