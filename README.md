# python-mq-client-app

# python-mq-app-feed

This container runs a Python script that will put a message a queue. That's it.

You need to pass some values using environment variables. Here is the list with a small description of each variable :
HOST_NAME: the host name where your queue manager is running ("127.0.0.1","localhost","192.168.1.52",...)
QUEUE_MANAGER_NAME : the queue manager name   
QUEUE_MANAGER_PORT_NUMBER : the port number the queue manager's listener is using.
CHANNEL_NAME : the script is opening a client connection. Therefore it needs a channel name (matching a SVRCONN channel defined on your queue manager) 
QUEUE_NAME : The target queue (local, alias, ...)


To build the image :
 docker build -t python-mq-app-feed -f .\dockerfile-mqfeed .

To run the container :
 docker run -e HOST_NAME="localhost" -e QUEUE_MANAGER_PORT_NUMBER="1515" -e QUEUE_MANAGER_NAME="QMGRA" -e CHANNEL_NAME="MQCONSUMER" -e QUEUE_NAME="mqConsumer001" python-mq-app-feed

Common errors :
An error occurred: MQI Error. Comp: 2, Reason 2538: FAILED: MQRC_HOST_NOT_AVAILABLE

It could be that the port number or the value of the host are incorrect. Make sure you use the right port (display listener/display lstatus) and the right host. It happened that neither localhost nor 127.0.0.1 were working. In that case, try with the IP of the machine running the queue manager (ipconfig to retrieve it in Windows)


# python-mq-app-consume

