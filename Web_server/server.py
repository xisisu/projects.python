# https://www.shiyanlou.com/courses/552/labs/1867/document

import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer


class ServerException(Exception):
  pass


class RequestHandler(BaseHTTPRequestHandler):
  Page = '''
  <html>
    <body>
      <table>
        <tr>  <td>Header</td>         <td>Value</td>          </tr>
        <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
        <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
        <tr>  <td>Client port</td>    <td>{client_port}</td>  </tr>
        <tr>  <td>Command</td>        <td>{command}</td>      </tr>
        <tr>  <td>Path</td>           <td>{path}</td>         </tr>
      </table>
    </body>
  </html>
  '''

  def do_GET(self):

    try:
      full_path = os.getcwd() + self.path
      default_file = os.path.join(full_path, '\index.html')

      if not os.path.exists(full_path):
        raise ServerException("'{0}' not found.".format(self.path))

      elif os.path.isfile(full_path) and full_path.endswith('.py'):
        content = subprocess.check_output(['python.exe', full_path], shell=True)
        self.send_content(content)

      elif os.path.isfile(full_path):
        self.handle_file(full_path)

      elif os.path.isdir(full_path) and os.path.isfile(default_file):
        self.handle_file(default_file)

      else:
        raise ServerException("'{0}' is not a file.".format(self.path))

    except Exception as msg:
      self.handle_error(msg)

  def handle_file(self, full_path):
    try:
      with open(full_path, 'rb') as reader:
        content = reader.read()
      self.send_content(content)
    except IOError as msg:
      msg = "'{0}' cannot be read: {1}".format(self.path, msg)
      self.handle_error(msg)

  Error_Page = '''
    <html>
      <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
      </body>
    </html>
  '''

  def handle_error(self, msg):
    content = self.Error_Page.format(path=self.path, msg=msg)
    self.send_content(content.encode('utf-8'), code=404)

  def send_content(self, content, code=200):
    self.send_response(code)
    self.send_header('Content-Type', 'text/html')
    self.send_header('Content-Length', str(len(content)))
    self.end_headers()
    self.wfile.write(content)


if __name__ == '__main__':
  server_address = ('', 8081)
  server = HTTPServer(server_address, RequestHandler)
  server.serve_forever()
