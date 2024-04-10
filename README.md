# Phần Linux Prog
## Tải dịch vụ gcc để có thể chạy code c
`sudo apt install gcc`
## Chạy Myid
<p> Biên dịch myid.c</p>

`gcc myid.c -o myid`
<p> Chạy myid.c</p>

`./myid`

## Chạy Mypasswd
<p> Biên dịch mypasswd.c</p>

`gcc mypasswd.c -o mypasswd -lcrypt`
<p> Chạy mypasswd.c (chạy dưới quyền root để có thể đọc/ghi các file)</p>

`./mypasswd`

# Phần SSH Logger
## Tải dịch vụ SSH ở cả máy người dùng và các máy SSH đến

`sudo apt install ssh`

## Chỉnh sửa file /etc/ssh/sshd_config

<p> Thêm đoạn sau</p>

```
PrintMotd no
PrintLastLog no
TCPKeepAlive yes
Banner /etc/issue.net
UsePAM yes
ChallengeResponseAuthentication yes
PasswordAuthentication yes
PermitRootLogin yes
PermitEmptyPasswords no

```

## Chạy từng file sshtrojan bằng quyền root để cho phép ghi log

`sudo bash sshtrojan1.sh`

`sudo bash sshtrojan2.sh`

# Phần HTTP Prog
## Tải python3 hoặc sử dụng python3 để chạy các file python
<p> File httpget.py </p>

`python3 httpget.py --url <link web http>`

<p> File httppost.py</p>

`python3 httppost.py --url <link web http> --user <tên user> --password <mật khẩu user> `

<p> File httpupload.py</p>

`python3 httpupload.py --url <link web http> --user <tên user có quyền quản lý> --password <mật khẩu user> --localfile <địa chỉ file ảnh đầy đủ>`

<p> File httpdownload.py</p>

`python3 httpdownload.py --url <link web http> --remotefile <địa chỉ bỏ đi domain chính>`
