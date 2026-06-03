from cave_utils import Socket


def test_socket():
    socket = Socket(silent=True)
    socket.broadcast("Test broadcast message", {"key": "value"})
    socket.notify("Test notify message", {"key": "value"})
