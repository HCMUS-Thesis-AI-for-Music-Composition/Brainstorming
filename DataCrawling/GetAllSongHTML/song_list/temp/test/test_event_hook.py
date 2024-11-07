import queue
import time
from locust import User, SequentialTaskSet, task
from locust.event import EventHook

release_port_event_hook = EventHook()

request_free_port_event_hook = EventHook()
send_free_port_event_hook = EventHook()

class SequentialSeleniumTasks(SequentialTaskSet):
    free_port = None

    def receive_free_port_handler(self, free_port):
        self.free_port = free_port

    def on_start(self):
        send_free_port_event_hook.add_listener(self.receive_free_port_handler)

    @task
    def init(self):
        print(f"Requesting free port")
        request_free_port_event_hook.fire()
        print(f"Requested free port")

    @task
    def process(self):
        for i in range(2):
            time.sleep(1)
            print(f"{self.free_port}: processing {i} of {2} seconds")

    @task
    def on_done(self):
        release_port_event_hook.fire(
            port = self.free_port
        )

available_ports = queue.Queue()
        
class MyUser(User):
    tasks = [SequentialSeleniumTasks]
    global available_ports
    def release_port_handler(self, port):
        print(f"{port}: releasing. Used ports: {self.available_ports.queue}")
        self.available_ports.put(port)

    def request_free_port_handler(self):
        port_to_run_browser = self.available_ports.get()
        
        print(f"{port_to_run_browser}: allocated. Available ports: {self.available_ports.queue}")

        send_free_port_event_hook.fire(
            free_port = port_to_run_browser
        )

        self.available_ports.task_done()

    def on_start(self):
        n_ports = 5
        for i in range(n_ports):
            self.available_ports.put(40000 + i)

        request_free_port_event_hook.add_listener(self.request_free_port_handler)
        release_port_event_hook.add_listener(self.release_port_handler)