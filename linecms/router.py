class Router:
    routes = []

    def put(self, handler):
        self.routes.append(handler)
        return handler

    def handle_event(self, event):
        for route in self.routes:
            agent = route.handle_event(event)

            if agent is not None:
                return agent
        return None
