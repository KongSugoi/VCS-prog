import argparse
import socket
import re
import html

# định nghĩa cho đối số --url
def get_args():
  args=argparse.ArgumentParser()
  args.add_argument('--url')
  return args.parse_args()

# nhận vào giá trị url 
def get_domain(url):
    domain = ""
    if url[0:8] == "https://":
        for i in range(8, len(url)):
            if url[i] == '/':
                break
            domain += url[i]
    if url[0:7] == "http://":
        for i in range(7, len(url)):
            if url[i] == '/':
                break
            domain += url[i]
    return domain

# thực hiện get URL được cấp
def get(url):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((url,80))
    header=f"GET / HTTP/1.1\r\nHost: {url}\r\nConnection: close\r\n\r\n"
    
    #print(header)
    s.sendall(f'{header}'.encode())
    while 1:
      data=s.recv(2048)
      
      #print(data)
      title=re.findall(b'<title>(.*)</title>',data)
      if len(title)!=0:
        print(f"Title: {html.unescape(title[0].decode())}")
        exit(0)
      if not data:
        break

def main():
  args=get_args()
  url=args.url
  domain=get_domain(url)
  get(domain)


if __name__ == '__main__':
  main()