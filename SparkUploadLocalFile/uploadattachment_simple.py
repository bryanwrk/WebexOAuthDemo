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

from requests_toolbelt import MultipartEncoder
import requests

filepath    = '/Users/tahanson/Desktop/fox.jpg'
filetype    = 'image/jpg'
roomId      = 'Y2lzY29zcGFyazovL3VzL1JPT00vOWY0NzVkZDAtZDk3Yi0xMWU5LWFhNDAtMDc5NjI5ZjE3Yzkz' #Project Unicorn Ultimate
token       = 'ZmUyNDZiNmMtODRhZS00NWRlLWJlZGEtZjVhYTI0OWFkMmY3M2RmMWNiNjYtZWNh_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
url         = "https://api.ciscospark.com/v1/messages"

my_fields={'roomId': roomId,
           'markdown': 'Hello World',
           'files': ('screenshot', open(filepath, 'rb'), filetype)
           }
m = MultipartEncoder(fields=my_fields)
r = requests.post(url, data=m,
                  headers={'Content-Type': m.content_type,
                           'Authorization': 'Bearer ' + token})
print(m)
print(dir(r))
print(r.headers)
print r.json()
