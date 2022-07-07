import time
from locust import HttpUser, task, constant

class QuickstartUser(HttpUser):
    wait_time = constant(0.5)

    @task
    def hello_world(self):
        files = {'image_file': open('abc.jpg','rb')}
        self.client.post("/function/hello-python",files=files, name="/item")
