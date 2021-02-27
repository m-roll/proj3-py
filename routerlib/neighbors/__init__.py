
class Neighbors():
    def __init__(self) -> None:
        pass

    def send_no_route(self, dest):
        msg = {dest: dest, src: self._get_ip(dest)}

    def _get_ip(self):
        pass
