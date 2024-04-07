#include <stdio.h>
#include <pwd.h>
#include <grp.h>
#include <string.h>

int main(){
	char n[100];
	printf("Enter Username: ");
	scanf("%s", n);

	struct passwd *pw;
        pw = getpwnam(n); // tìm dòng trong /etc/passwd chứa  tên người dùng nhập vào
	struct group *up;
	    

	if(pw != NULL) // kiểm tra xem có người dùng được trả về hay không
    {
        // nếu có in ra những thông tin sau
		printf("User ID = %u\n", pw->pw_uid); // in ra User ID của người dùng
		printf("User Name = %s\n", pw->pw_name); // in ra tên người dùng
		printf("Home = %s\n", pw->pw_dir); // in ra thư mục home người dùng
		printf("Group ="); 
		printf(" %s", pw->pw_name); // in ra nhóm cơ bản của người dùng (nhóm trùng với tên)
		
        int i = 0;
		setgrent(); // đặt vị trí con trỏ vào đầu file /etc/group để đọc

		while((up = getgrent()) != NULL) // duyệt tất cả các group trong /etc/group
        {
			i=0; // thiết lập lại i cho mỗi group mới để duyệt từng thành viên
			while( *(up->gr_mem + i)) // duyệt qua tất cả thành viên trong group
            {
				if (strcmp(n,*(up->gr_mem + i))==0) // so sánh tên người dùng với tên thành viên trong group, trùng thì in ra
                {
					printf(" %s", up->gr_name);
				}	
				i++; // duyệt thành viên tiếp
			}
		}
		endgrent(); // đóng file /etc/group
                
		printf("\n");
	} 
	else printf("Can not find this User\n");	
	return 0;
}