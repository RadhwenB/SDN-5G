from app import app
import threading


from app.request_handler import receive

receiveThread = threading.Thread(target=receive)
receiveThread.start()
