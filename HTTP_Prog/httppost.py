import argparse
import socket

def get_args():
  parser=argparse.ArgumentParser()
  parser.add_argument('--url')
  parser.add_argument('--user')
  parser.add_argument('--password')
  return parser.parse_args()

def get_domain(url):
  domain = ""
  if url[0:8] == "https://":
  	for i in range(8, len(url)):
  		if url[i] == "/":
  			break;
  		domain += url[i]
  if url[0:7] == "http://":
  	for i in range(7, len(url)):
  		if url[i] == "/":
  			break;
  		domain += url[i]
  return domain
  
  
def login(domain,user,password):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((domain,80))
    data=f"log={user}&pwd={password}"
    header=f"POST /wp-login.php HTTP/1.1\r\nHost: {domain}\r\nContent-Length: {str(len(data))}\r\nContent-Type: application/x-www-form-urlencoded\r\nConnection: Keep-alive\r\n\r\n"
    header+=data
    #print(header)
    s.sendall(header.encode())
    res_text=b""
    while 1:
      data=s.recv(2048)
      if not data:
        break
      res_text+=data
    if b'login_error' not in res_text:
      print(f"User {user} dang nhap thanh cong")
    else:
      print(f"User {user} dang nhap that bai")

def main():
  args=get_args()
  url = args.url
  user = args.user
  password=args.password
  domain=get_domain(url)
  login(domain,user,password)


if __name__ == '__main__':
  main()