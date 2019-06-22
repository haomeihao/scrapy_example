# coding=utf-8

from websocket import create_connection


class WebSocketClient():

    def __init__(self, url="ws://127.0.0.1:8080/webSocket"):
        self.url = url
        self.ws = create_connection(self.url)

    def send_msg(self, msg="Hello, World"):
        print("Sending " + msg + "")
        self.ws.send(msg)
        print("Sent")

    def recv_msg(self):
        print("Reeiving...")
        result = self.ws.recv()
        print("Received '%s'" % result)

    def close_connection(self):
        self.ws.close()


if __name__ == '__main__':
    client = WebSocketClient()
    client.send_msg("有新通知")