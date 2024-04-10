import socket
import sys
import string
import argparse
import re

def get_args():
  args = argparse.ArgumentParser()
  args.add_argument("--url")
  args.add_argument("--username")
  args.add_argument("--password")
  args.add_argument("--localfile")
  return args.parse_args()
  
args = get_args()


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


def recvall(s):
    total_data = []
    res = s.recv(2048)
    while (len(res) > 0):
        total_data.append(res.decode())
        res = s.recv(2048)
    res = ''.join(total_data)
    return res


def get_cookies(res):
    cookies = []
    stringSplit = res.split("\r\n")	
    for i in stringSplit:
        if "Set-Cookie: " in i:
            cookies.append(i.split(";")[0].split(":")[1].strip())
    return ";".join(cookies)


def getWpNonce(cookies, domain):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, 80))
    valid = string.ascii_lowercase+string.digits
    req= "GET /wp-admin/media-new.php HTTP/1.1\r\n" + "Host: "+domain+"\r\n"+"Cookie: "+cookies+"\r\n\r\n"
    # print(req)
    s.send(req.encode())
    res = recvall(s)
    start = re.search('name="_wpnonce"', res).end() + 8
    end = start + 10
    return res[start:end]
    return result


def upload_image(cookies, domain, fileName, pathLocalFile):
    data = open(pathLocalFile, 'rb').read()
    test = ""
    for i in data:
        test += chr(i)
    wpnonce = getWpNonce(cookies, domain)
    contentType = fileName.split(".")[-1]
    contentType = "jpeg"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, 80))
    body = "------WebKitFormBoundary"+"\r\n"+"Content-Disposition: form-data; name=\"name\"" + \
        "\r\n\r\n"+fileName+"\r\n"+"------WebKitFormBoundary"+"\r\n" + \
        "Content-Disposition: form-data; name=\"action\"" + \
        "\r\n\r\n"+"upload-attachment"+"\r\n"+"------WebKitFormBoundary"+"\r\n" + \
        "Content-Disposition: form-data; name=\"_wpnonce\""+"\r\n\r\n"+wpnonce+"\r\n"+"------WebKitFormBoundary" + \
        "\r\n"+"Content-Disposition: form-data; name=\"async-upload\"; filename=\"" + \
        fileName+"\""+"\r\n"+"Content-Type: image/"+contentType+"\r\n\r\n"
    body = body.encode()+data+b"\r\n"+b"------WebKitFormBoundary--"
    lenBody = str(len(body))
    req = "POST /wp-admin/async-upload.php HTTP/1.1\r\n"+"Host: "+domain+"\r\n"+"Cookie: " + \
        cookies+"\r\n"+"Connection: keep-alive\r\n"+"Content-Type: multipart/form-data; boundary=----WebKitFormBoundary" + \
        "\r\n"+"Content-Length: "+lenBody+"\r\n"+"\r\n"
    s.send(req.encode()+body)
    res= recvall(s)
    if "HTTP/1.1 200 OK" in res and "{\"success\":true" in res:
        print("Upload success.")
        path_url = ""
        for i in range(0, len(res)):
            if(path_url != ""):
                break
            if res[i:i+7] == "\"url\":\"":
                for j in range(i+7, len(res)):
                    if(res[j] == "\""):
                        break
                    path_url += res[j]
        path_url = path_url.replace('\\', '')
        print("File upload url:"+path_url)
    else:
        print("Upload fail.")
    return

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = args.url
username =args.username
password = args.password
pathLocalFile = args.localfile
domain = get_domain(url)
fileName = pathLocalFile.split("/")[-1]
s.connect((domain, 80))
body = "log="+username+"&pwd="+password
req= "POST /wp-login.php HTTP/1.1\r\n"+"HOST: "+domain + "\r\n"+"Content-Length: "+str(len(body))+"\r\n"+"Content-Type: application/x-www-form-urlencoded"+"\r\n"+"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"+"\r\n"+"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"+"\r\n" + "Cookie: wordpress_test_cookie=WP Cookie check; wp_lang=en_US"+"\r\n" \
    "\r\n"+body
s.send(req.encode())
res= recvall(s)
if "HTTP/1.1 302 Found" in res and "is incorrect" not in res and "is not registered on this site" not in res:
    cookies = get_cookies(res)
    upload_image(cookies, domain, fileName, pathLocalFile)
else:
    print("User "+username+" dang nhap that bai.")
    exit(0)