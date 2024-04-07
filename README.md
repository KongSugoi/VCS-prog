# Tải dịch vụ gcc trên Ubuntu Linux để có thể run code
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
