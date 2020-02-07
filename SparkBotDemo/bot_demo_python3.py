"""
Copyright 2016 Cisco Systems Inc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

def sendSparkGET(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = requests.get(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json",
                                     "Authorization": "Bearer "+bearer})
    return request.json()

def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = requests.post(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json",
                                     "Authorization": "Bearer "+bearer})
    return request.json()

class MainRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """
        When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
        using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
        further actions are taken. i.e.
        /batman    - replies to the room with text
        /batcave   - echoes the incoming text to the room
        /batsignal - replies to the room with an image
        """
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        webhook = json.loads(post_data)
        print(webhook['data']['id'])
        result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
        msg = None
        if webhook['data']['personId'] != bot_id:
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name, '')
            if 'batman' in in_message or "whoareyou" in in_message:
                msg = "I'm Batman!"
            elif 'batcave' in in_message:
                message = result.get('text').split('batcave')[1].strip(" ")
                if len(message) > 0:
                    msg = "The Batcave echoes, '{0}'".format(message)
                else:
                    msg = "The Batcave is silent..."
            elif 'batsignal' in in_message:
                print("NANA NANA NANA NANA")
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bat_signal})
            if msg != None:
                print(msg)
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Write response to server as utf-8 data
            self.wfile.write(bytes("true", "utf8"))
            return

####CHANGE THESE VALUES#####
bot_id = "MY_BOT_ID"
bot_name = "MY_BOT_NAME"
bearer = "MY_BOT_TOKEN"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"

def run():
    port = 10010
    server_address = ('127.0.0.1', port)
    server = HTTPServer(server_address, MainRequestHandler)
    print('running server on port {0}...'.format(port))
    server.serve_forever()

run()
