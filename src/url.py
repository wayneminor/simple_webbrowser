import socket

from typing import TextIO

class URL:
    def __init__(self, url: str) -> None:
        # simple parser of url
        #   hypothesis:
        #       url := protocal://host-name/path
        #           |:= protocal://host-name
        self.scheme, url = url.split('://', 1)
        assert self.scheme == 'http'

        if '/' not in url:
            url += '/'
        
        self.host, url = url.split('/', 1)
        self.path = '/'

    def request(self) -> str:
        sock = socket.socket(
            family = socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        sock.connect((self.host, 80))

        request = f"GET {self.path} HTTP/1.0 \r\n"
        request += f"Host: {self.host}\r\n"
        request += "\r\n"


        # send request and construct the response
        sock.send(request.encode('utf-8'))
        response: TextIO = sock.makefile('r', encoding='utf-8', newline='\r\n')


        # parse response
        status_line: str = response.readline()
        version, status, explanation = status_line.split(' ', 2) # type: ignore
        # headers
        response_headers: dict[str, str] = {}
        while True:
            line = response.readline()
            if line == '\r\n':
                break
            header, value = line.split(':', 1)
            response_headers[header.casefold()] = value.strip()

            assert "transfer-encoding" not in response_headers
            assert "content-encoding" not in response_headers

        content: str = response.read()
        sock.close()

        return content
        
def show(body: str):
    in_tag = False # 打印状态开关
    for c in body:
        if c == '<':
            in_tag = True
        elif c == '>':
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url: URL):
    body: str = url.request()
    show(body)


if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))

    # for test
    # load(URL('http://example.org/'))