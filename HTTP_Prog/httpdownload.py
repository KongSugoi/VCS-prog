import argparse
import socket
import re
import html
def get_args():
  args=argparse.ArgumentParser()
  args.add_argument('--url')
  args.add_argument('--remotefile')
  return args.parse_args()

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

def get_image(url, remotefile):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((url,80))
    header=f"GET {remotefile} HTTP/1.1\r\nHost: {url}\r\nConnection: close\r\n\r\n"
    #header = header.replace("\n", "\r\n")
    s.sendall(f'{header}'.encode())
    #print(header)
    res_text = b''
    while 1:
      data=s.recv(2048)
      #print(data)
      if not data:
      	break
      res_text += data
    return res_text
    
        
def main():
  args=get_args()
  url=args.url
  remotefile = args.remotefile
  domain=get_domain(url)
  res_text = get_image(domain, remotefile)
  #print(res_text)
  if b'Content-Type: image/' not in res_text:
  	print("Khong ton tai anh")
  	exit()
  else:
  	data = res_text.split(b"\r\n\r\n")[1]
  	data = res_text.decode('iso-8859-1').split('\r\n\r\n')[1].encode('iso-8859-1')
  	print("Kick thuoc file anh: " + str(len(data.decode('iso-8859-1'))) + ' bytes')
  	name_image = remotefile.split("/")[-1]
  	f = open(name_image, "wb")
  	f.write(data)


if __name__ == '__main__':
  main()