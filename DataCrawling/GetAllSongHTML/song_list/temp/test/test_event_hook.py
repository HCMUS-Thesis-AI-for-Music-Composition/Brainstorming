from locust import User, SequentialTaskSet, task
from locust.event import EventHook

port_manager_event_hook = EventHook()

request_used_ports_event_hook = EventHook()
send_used_ports_event_hook = EventHook()

class SequentialSeleniumTasks(SequentialTaskSet):
    used_ports = []

    def receive_used_ports_handler(self, _used_ports):
        self.used_ports = _used_ports

    def on_start(self):
        send_used_ports_event_hook.add_listener(self.receive_used_ports_handler)

    @task
    def init(self):
        port_to_run_browser = 40000

        request_used_ports_event_hook.fire()

        print(type(self.used_ports))
        print(self.used_ports)
        exit()
        
        while port_to_run_browser in used_ports:
            port_to_run_browser += 1

        request_used_ports_event_hook.fire(
            port = port_to_run_browser,
            should_release = False
        ) 

        self.free_port = port_to_run_browser
        print(f"Got free port: {self.free_port}")
        
class MyUser(User):
    tasks = [SequentialSeleniumTasks]
    used_ports = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def port_manager_handler(self, port, should_release):
        if should_release:
            self.used_ports.remove(port)
        else:
            self.used_ports.append(port)


    def request_used_ports_handler(self):
        send_used_ports_event_hook.fire(
            _used_ports = self.used_ports
        )

    def on_start(self):
        port_manager_event_hook.add_listener(self.port_manager_handler)
        request_used_ports_event_hook.add_listener(self.request_used_ports_handler)