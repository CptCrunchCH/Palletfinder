import threading
from threading import Thread
import queue

# **********************************************
# How to Share Local Variables between functions
# **********************************************
# create a queue
q = queue.Queue()
# The queue must be shared and accessible to each thread and within the function where the 
# local variable is defined and used.

# custom task function executed by a thread
def task_function(q):
	# create a local variable
	data = 55
	# share the local variable
	q.put(data)

# custom task function executed by another thread
def another_task_function(q):
	# get shared local data from the queue
	data = q.get()
    

if __name__ == "__main__":
    thread0 = Thread(target=task_function,args = q)
    thread0.start()
    thread1 = Thread(target=another_task_function, args = q)
    thread1.start()