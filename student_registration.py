import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename,askdirectory
from PIL import Image,ImageTk,ImageFont,ImageDraw,ImageOps
from io import BytesIO
import re
import random
import sqlite3
import os
import win32api
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import my_email
from tkinter.ttk import Combobox,Treeview
from tkinter.scrolledtext import ScrolledText
import threading


root = tk.Tk()
root.geometry('500x600')
root.title('Tkinter Hub(Student Management && Registration System)')
bg_color = '#273b7a'

log_in_student = tk.PhotoImage(file='C:/Users/DELL/Downloads/Images/login_student_img.png')
log_in_student1 = tk.PhotoImage(file='C:/Users/DELL/Downloads/Images/admin_img.png')
log_in_student2 = tk.PhotoImage(file='C:/Users/DELL/Downloads/Images/add_student_img.png')
locked_img = tk.PhotoImage(file='C:/Users/DELL/Downloads/Images/locked.png')
unlocked_img = tk.PhotoImage(file='C:/Users/DELL/Downloads/Images/unlocked.png')
add_student_pic_ioc = tk.PhotoImage(file='C:/Users/DELL/Downloads/Images/add_image.png')


def init_database():
    if os.path.exists('student_accounts.db'):
        connection = sqlite3.connect('student_accounts.db')
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM data       
                """)
        connection.commit()
        print(cursor.fetchall())
        connection.close()





    else:
        connection = sqlite3.connect('student_accounts.db')
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE data (
        id_number text,
        password text,
        name text,
        age text,
        gender text,
        phone_number text,
        class text,
        email text,
        image blob
        )
        """)
        connection.commit()
        connection.close()

def check_data_already(id_number):
    connection = sqlite3.connect('student_accounts.db')
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT id_number FROM data WHERE id_number == '{id_number}'
      """)
    connection.commit()
    response = cursor.fetchall()
    connection.close()
    return response

def check_valid_passwoed(id_number,password):
    connection = sqlite3.connect('student_accounts.db')
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT id_number, password FROM data WHERE id_number == '{id_number}' AND password == '{password}'
      """)
    connection.commit()
    response = cursor.fetchall()
    connection.close()
    return response


def add_data(id_number,password,name,age,gender,phone_number,student_class,email,pic_data):
    connection = sqlite3.connect('student_accounts.db')
    cursor = connection.cursor()
    cursor.execute(f"""
    INSERT INTO data VALUES ('{id_number}','{password}','{name}','{age}','{gender}','{phone_number}','{student_class}','{email}',?)""",[pic_data])
    connection.commit()
    connection.close()

####Conformation box #######

def conformation_box(message):

    answer = tk.BooleanVar()
    answer.set(False)
    def action(ans):
        answer.set(ans)
        conformation_box_fm.destroy()

    conformation_box_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    message_lb = tk.Label(conformation_box_fm, text=message, font=('Bold',15))
    message_lb.pack(pady=20)
    conformation_box_fm.place(x=100,y=120,width=320,height=220)

    cancel_btn = tk.Button(conformation_box_fm,text='Cancel',font=('Bold',15),bd=1,bg=bg_color,fg='white',command=lambda:action(False))
    cancel_btn.place(x=50,y=160)
    yes_btn = tk.Button(conformation_box_fm, text='Yes', font=('Bold', 15), bd=1, bg=bg_color, fg='white',command=lambda:action(True))
    yes_btn.place(x=190, y=160,width=80)


    root.wait_window(conformation_box_fm)
    return answer.get()

def message_box(message):
    message_box_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    close_btn = tk.Button(message_box_fm,text='X',bd=0,font=('Bold',13),fg=bg_color,command=lambda: message_box_fm.destroy())
    message_lb = tk.Label(message_box_fm,text=message,font=('Bold',15))
    message_lb.pack(pady=50)
    close_btn.place(x=290,y=5)
    message_box_fm.place(x=100,y=120,height=200,width=320)

#################################################################  card   ##############################################
def draw_card(student_pic_path,student_data):
    lables = """
ID Number:
Name:
Age:
Gender:
Phone Number:
Class:
Email:
"""
    draw_student = Image.open('C:/Users/DELL/Downloads/Images/student_card_frame.png')
    pic = Image.open(student_pic_path).resize((100,100))
    draw_student.paste(pic,(15,25))
    draw = ImageDraw.Draw(draw_student)
    heading_font = ImageFont.truetype('bahnschrift',18)
    lables_font = ImageFont.truetype('arial', 13)
    data_font = ImageFont.truetype('bahnschrift', 13)
    draw.text(xy=(150,60),text='Student Card',fill=(0,0,0),font=heading_font)
    draw.multiline_text(xy=(15,120),text=lables,fill=(0,0,0),font=lables_font,spacing=10)
    draw.multiline_text(xy=(130, 120), text=student_data, fill=(0, 0, 0), font=lables_font, spacing=10)
    return draw_student

def student_card(student_card_obj,bypass_login_page=False):

    def save_student_card():
        path = askdirectory()
        if path:
            print(path)
            student_card_obj.save(f'{path}/draw_card.png')

    def print_student_card():
        path = askdirectory()
        if path:
            print(path)
            student_card_obj.save(f'{path}/draw_card.png')
            win32api.ShellExecute(0,'print',f'{path}/draw_card.png',None,'.',0)

    def close_page():
        student_card_fm.destroy()
        if not bypass_login_page:
            root.update()
            student_log_in_page()


    student_card_img = ImageTk.PhotoImage(student_card_obj)
    student_card_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    heading_lb = tk.Label(student_card_fm,text='Student Card',font=('Bold',18),bg=bg_color,fg='white')
    heading_lb.place(x=0,y=0,width=400)
    card_close_btn = tk.Button(student_card_fm,text='X',bd=0,font=('Bold',13),bg=bg_color,fg='white',command=close_page)
    card_close_btn.place(x=370,y=0)
    student_card_lb = tk.Label(student_card_fm,image=student_card_img)

    student_card_lb.place(x=50,y=50)
    student_card_lb.image = student_card_img
    save_btn = tk.Button(student_card_fm,text='Save Student Card',bd=1,font=('Bold',15),bg=bg_color,fg='white',command=save_student_card)
    save_btn.place(x=80,y=375)
    print_student_btn =  tk.Button(student_card_fm,text='🖨',bd=1,font=('Bold',18),bg=bg_color,fg='white',command=print_student_card)
    print_student_btn.place(x=270,y=370)
    student_card_fm.place(x=50,y=30,width=400,height=450)

#####################   WELLCOME PAGE ##################################################
def wellcome_page():
    def forward_to_student_login_page():
        wellcomepage_fm.destroy()
        root.update()
        student_log_in_page()

    def forward_to_admin_login_page():
        wellcomepage_fm.destroy()
        root.update()
        admin_login_page()

    def forward_to_crerate_account_page():
        wellcomepage_fm.destroy()
        root.update()
        create_acc()




    wellcomepage_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)

    heading_lb = tk.Label(wellcomepage_fm,text='Wellcome To Student Registration\n$$ and Management System',
                          bg=bg_color,fg='white',font=('Bold',18))
    heading_lb.place(x=0,y=0,width=400)

    student_login_btn = tk.Button(wellcomepage_fm,text='Login Student',bg=bg_color,fg='white',font=('Bold',15), bd=0,command=forward_to_student_login_page)
    student_login_btn.place(x=140,y=125,width=200)

    student_login_img = tk.Button(wellcomepage_fm,image=log_in_student, bd=0,command=forward_to_student_login_page)
    student_login_img.place(x=60,y=100,width=100)

    student_admin_btn = tk.Button(wellcomepage_fm,text='Login Admin',bg=bg_color,fg='white',font=('Bold',15), bd=0,command=forward_to_admin_login_page)
    student_admin_btn.place(x=140,y=217,width=200)

    student_admin_img = tk.Button(wellcomepage_fm,image=log_in_student1, bd=0,command=forward_to_admin_login_page)
    student_admin_img.place(x=60,y=191,width=100)

    student_add_btn = tk.Button(wellcomepage_fm,text='Create Account',bg=bg_color,fg='white',font=('Bold',15), bd=0,command=forward_to_crerate_account_page)
    student_add_btn.place(x=140,y=311,width=200)

    student_add_img = tk.Button(wellcomepage_fm,image=log_in_student2, bd=0,command=forward_to_crerate_account_page)
    student_add_img.place(x=60,y=286,width=100)


    wellcomepage_fm.pack(pady=30)
    wellcomepage_fm.pack_propagate(False)
    wellcomepage_fm.config(width=400,height=420)

##########################################  email send ######################

def send_mail_to_student(email,message,subject):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    username = my_email.email_address
    password = my_email.password
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = email
    msg.attach(MIMEText(_text=message, _subtype='html'))

    smtp_connection = smtplib.SMTP(host=smtp_server,port=smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(user=username,password=password)

    smtp_connection.sendmail(from_addr=username,to_addrs=email,msg=msg.as_string())
    smtp_connection.quit()

################ forget function ###############################
def forget_password_page():
######################      recover function         ###############################
    def recover_password():
        if check_data_already(id_number=student_id_ent.get()):
            print("Correct id")

            connection = sqlite3.connect('student_accounts.db')
            cursor = connection.cursor()

            cursor.execute(f"""
            SELECT password FROM data WHERE id_number == '{student_id_ent.get()}'
            """)

            connection.commit()
            recovered_password = cursor.fetchall()[0][0]

            cursor.execute(f"""
                        SELECT email FROM data WHERE id_number == '{student_id_ent.get()}'
                        """)

            connection.commit()
            student_email = cursor.fetchall()[0][0]
            connection.close()

            conformation = conformation_box(message=f"""We Will Send\nYour Forget Password
Via Email Adderss:
{student_email}
Do You Want to Continue?
            """)
            if conformation:
                msg = f"""<h1> Your Forgot Password is :</h1>
                <h2>{recovered_password}</h2>
                <p>Once Remember Your Password, After Delete This Message</p>"""

                send_mail_to_student(email=student_email, message=msg,
                                     subject='Password Recovered')



        else:
            print("Incorrect ID")
            message_box(message="Invalid ID Number")



    forget_password_page_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)


    heading_lable = tk.Label(forget_password_page_fm,text='⚠ Forgetting Password', bg=bg_color,fg='white',font=('Bold',18))
    heading_lable.place(x=0,y=0,width=350)

    close_btn = tk.Button(forget_password_page_fm, text='X', bd=0, font=('Bold', 13), bg=bg_color, fg='white',command=lambda: forget_password_page_fm.destroy())
    close_btn.place(x=322, y=0)

    student_id_lb = tk.Label(forget_password_page_fm, text='Enter Student ID Number.', fg=bg_color, font=('Bold', 15))
    student_id_lb.place(x=70, y=40)

    student_id_ent = tk.Entry(forget_password_page_fm, font=('Bold', 15), highlightcolor=bg_color,
                             highlightbackground='gray', highlightthickness=2)
    student_id_ent.place(x=70, y=70, width=180)

    info_lb = tk.Label(forget_password_page_fm, text="""Via Your Email Address
We Will Send to You
Your Forget Password.""", justify=tk.LEFT)
    info_lb.place(x=70, y=110)

    next_btn = tk.Button(forget_password_page_fm,text='NEXT', bd=1,font=('Bold',15),bg=bg_color,fg='white',command=recover_password)
    next_btn.place(x=130,y=200,width=80)



    forget_password_page_fm.place(x=75,y=120,width=350,height=250)

########################################     fectal data to home page ###########

def fetch_student_data(query):
    connection = sqlite3.connect('student_accounts.db')
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    response = cursor.fetchall()
    cursor.close()
    return response



###############################  student dash board  ########################

def student_dashboard(student_id):

    get_student_detail = fetch_student_data(f"""
    SELECT name, age, gender, class, phone_number, email FROM data WHERE id_number == '{student_id}'
    """)

    get_student_pic = fetch_student_data(f"""
        SELECT image FROM data WHERE id_number == '{student_id}'
        """)

    student_pic = BytesIO(get_student_pic[0][0])

    def logout():

        confirm = conformation_box(message="Do You Want to\n Logout Your Account")

        if confirm:
            dashboard_fm.destroy()
            wellcome_page()
            root.update()




    def switch(indicator,page):

        home_indicator_btn.config(bg="#c3c3c3")
        student_card_indicator_btn.config(bg="#c3c3c3")
        security_indicator_btn.config(bg="#c3c3c3")
        delete_account_indicator_btn.config(bg="#c3c3c3")
        edit_indicator_btn.config(bg="#c3c3c3")


        indicator.config(bg=bg_color)

        for child in pages_fm.winfo_children():
            child.destroy()
            root.update()
        page()


    dashboard_fm = tk.Frame(root,highlightthickness=3,highlightbackground=bg_color)

    option_fm = tk.Frame(dashboard_fm,highlightthickness=2,highlightbackground=bg_color,bg='#c3c3c3')
    option_fm.place(x=0,y=0,width=120,height=575)

    home_btn = tk.Button(dashboard_fm,text='Home',font=('Bold',15),bg='#c3c3c3',fg=bg_color,bd=0,command=lambda :switch(home_indicator_btn, page=home_page))
    home_btn.place(x=10,y=50)

    home_indicator_btn = tk.Label(dashboard_fm, bg=bg_color)
    home_indicator_btn.place(x=5, y=48,width=3,height=40)

    student_card_btn = tk.Button(dashboard_fm, text='Student\nCard', font=('Bold', 15), bg='#c3c3c3', fg=bg_color, bd=0,justify=tk.LEFT,
                                 command=lambda :switch(student_card_indicator_btn, page=student_page))
    student_card_btn.place(x=10, y=100)

    student_card_indicator_btn = tk.Label(dashboard_fm, bg='#c3c3c3')
    student_card_indicator_btn.place(x=5, y=108, width=3, height=40)

    security_btn = tk.Button(dashboard_fm, text='Security', font=('Bold', 15), bg='#c3c3c3', fg=bg_color, bd=0, command=lambda :switch(security_indicator_btn,page=security_page))
    security_btn.place(x=10, y=170)

    security_indicator_btn = tk.Label(dashboard_fm, bg='#c3c3c3')
    security_indicator_btn.place(x=5, y=170, width=3, height=40)

    edit_btn = tk.Button(dashboard_fm, text='Edit Data', font=('Bold', 15), bg='#c3c3c3', fg=bg_color, bd=0, command=lambda :switch(edit_indicator_btn,page=edit_page))
    edit_btn.place(x=10, y=220)

    edit_indicator_btn = tk.Label(dashboard_fm, bg='#c3c3c3')
    edit_indicator_btn.place(x=5, y=220, width=3, height=40)

    delete_account_btn = tk.Button(dashboard_fm, text='Delete\nAccount', font=('Bold', 15), bg='#c3c3c3', fg=bg_color, bd=0,justify=tk.LEFT,
                                   command=lambda: switch(delete_account_indicator_btn,page=delete_page)
                                   )
    delete_account_btn.place(x=10, y=270)

    delete_account_indicator_btn = tk.Label(dashboard_fm, bg='#c3c3c3')
    delete_account_indicator_btn.place(x=5, y=280, width=3, height=40)

    logout_btn = tk.Button(dashboard_fm, text='Logout', font=('Bold', 15), bg='#c3c3c3', fg=bg_color, bd=0,command=logout)
    logout_btn.place(x=10, y=340)

    def home_page():

        #pic_img_obj = ImageTk.PhotoImage(Image.open(student_pic))
        student_pic_omg_obj = Image.open(student_pic)
        size = 100
        mask = Image.new(mode='L',size=(size,size))

        draw_circle = ImageDraw.Draw(im=mask)
        draw_circle.ellipse(xy=(0, 0, size, size),fill=255,outline=True)

        output = ImageOps.fit(image=student_pic_omg_obj,size=mask.size,centering=(1,1))
        output.putalpha(mask)


        student_picture = ImageTk.PhotoImage(output)

        home_fm = tk.Frame(pages_fm)


        student_pic_lb = tk.Label(home_fm,image=student_picture)
        student_pic_lb.image = student_picture

        student_pic_lb.place(x=10,y=10)

        hi_lb = tk.Label(home_fm,text=f"!Hi {get_student_detail[0][0]}",font=('Bold',15))
        hi_lb.place(x=130,y=50)

        student_details = f"""
Student ID : {student_id}\n
Name : {get_student_detail[0][0]}\n
Age : {get_student_detail[0][1]}\n
Gender : {get_student_detail[0][2]}\n
Class : {get_student_detail[0][3]}\n
Contact : {get_student_detail[0][4]}\n
Email : {get_student_detail[0][5]}\n
"""
        student_details_lb = tk.Label(home_fm,text=student_details,font=('Bold',13),justify=tk.LEFT)
        student_details_lb.place(x=20,y=130)
        home_fm.pack(fill=tk.BOTH,expand=True)

    def student_page():
        student_fm = tk.Frame(pages_fm)

        student_details = f"""
{student_id}
{get_student_detail[0][0]}
{get_student_detail[0][1]}
{get_student_detail[0][2]}
{get_student_detail[0][4]}
{get_student_detail[0][3]}
{get_student_detail[0][5]}
"""

        student_card_image_obj = draw_card(student_pic_path=student_pic,student_data=student_details)
        student_card_img = ImageTk.PhotoImage(student_card_image_obj)

        def save_student_card():
            path = askdirectory()
            if path:

                student_card_image_obj.save(f'{path}/draw_card.png')

        def print_student_card():
            path = askdirectory()
            if path:

                student_card_image_obj.save(f'{path}/draw_card.png')
                win32api.ShellExecute(0, 'print', f'{path}/draw_card.png', None, '.', 0)



        card_lb = tk.Label(student_fm,image=student_card_img)
        card_lb.image = student_card_img
        card_lb.place(x=20,y=50)

        save_student_card_btn = tk.Button(student_fm,text='Save Student Card', font=('Bold',15),bg=bg_color,fg='white',bd=1,command=save_student_card)
        save_student_card_btn.place(x=  40,y=400)

        print_student_card_btn = tk.Button(student_fm, text='🖨', font=('Bold', 15), bg=bg_color,
                                          fg='white', bd=1,command=print_student_card)
        print_student_card_btn.place(x=240, y=400)

        student_fm.pack(fill=tk.BOTH,expand=True)

    def security_page():

        def show_hide_password():
            if current_password_ent['show'] == '*':
                current_password_ent.config(show='')
                show_hide_btn.config(image=unlocked_img)
            else:
                current_password_ent.config(show='*')
                show_hide_btn.config(image=locked_img)

        def set_password():
            if new_password_ent.get() != '':
                confirm = conformation_box(message="Do You Want To Change\n You Password ?")

                if confirm:
                    connection = sqlite3.connect('student_accounts.db')
                    cursor = connection.cursor()

                    cursor.execute(f"""UPDATE data SET password = '{new_password_ent.get()}' 
                    WHERE id_number == '{student_id}'""")

                    connection.commit()
                    connection.close()

                    message_box(message="Password Changed Successfully")

                    current_password_ent.config(state=tk.NORMAL)
                    current_password_ent.delete(0,tk.END)
                    current_password_ent.insert(0, new_password_ent.get())
                    current_password_ent.config(state='readonly')

                    new_password_ent.delete(0,tk.END)

            else:
                message_box(message="New Password Required.")

        security_fm = tk.Frame(pages_fm)

        current_password_lb = tk.Label(security_fm,text='Your Current Password.',font=('Bold',12))
        current_password_lb.place(x=80,y=30)

        current_password_ent = tk.Entry(security_fm, font=('Bold', 15),justify=tk.CENTER,show='*')
        current_password_ent.place(x=50, y=80)

        student_current_password = fetch_student_data(f"SELECT password FROM data WHERE id_number == '{student_id}'")

        current_password_ent.insert(tk.END,student_current_password[0][0])
        current_password_ent.config(state='readonly')

        show_hide_btn = tk.Button(security_fm, image=locked_img, bd=0, command=show_hide_password)
        show_hide_btn.place(x=280, y=70)

        change_password_lb = tk.Label(security_fm, text='Change Password', font=('Bold', 15),bg='red',fg='white')
        change_password_lb.place(x=30, y=210,width=290)

        new_password_lb = tk.Label(security_fm, text='Set New Password', font=('Bold', 12))
        new_password_lb.place(x=100, y=280)

        new_password_ent = tk.Entry(security_fm, font=('Bold', 15), justify=tk.CENTER, show='*')
        new_password_ent.place(x=60, y=330)

        change_password_btn = tk.Button(security_fm,text='Set Password',font=('Bold',13),bg=bg_color,fg='white',command=set_password)
        change_password_btn.place(x=110,y=380)

        security_fm.pack(fill=tk.BOTH,expand=True)

    def edit_page():
        edit_fm = tk.Frame(pages_fm)

        class_list = ["5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"]

        pic_path = tk.StringVar()
        pic_path.set('')

        def open_pic():
            path = askopenfilename()
            if path:
                img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
                pic_path.set(path)

                add_pic_btn.config(image=img)
                add_pic_btn.image = img

        def remove_warning(entry):
            if entry['highlightbackground'] != 'gray':
                if entry.get() != '':
                    entry.config(highlightbackground='gray', highlightcolor=bg_color)

        def check_invalid_email(email):
            pattern = "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"
            match = re.match(pattern=pattern, string=email)
            return match

        def check_input():
            nonlocal get_student_detail,get_student_pic,student_pic
            if student_name_ent.get() == '':
                student_name_ent.config(highlightcolor='red',highlightbackground='red')
                student_name_ent.focus()
                message_box(message='Student Full Name is Required')
            elif student_age_ent.get() == '':
                student_age_ent.config(highlightcolor='red',highlightbackground='red')
                student_age_ent.focus()
                message_box(message='Student Age is Required')
            elif student_con_ent.get() == '':
                student_con_ent.config(highlightcolor='red',highlightbackground='red')
                student_con_ent.focus()
                message_box(message='Student Contact Number is Required')
            elif student_em_ent.get() == '':
                student_em_ent.config(highlightcolor='red',highlightbackground='red')
                student_em_ent.focus()
                message_box(message='Student Email is Required')

            elif not check_invalid_email(email=student_em_ent.get().lower()):
                student_em_ent.config(highlightcolor='red', highlightbackground='red')
                student_em_ent.focus()
                message_box(message='Enter Valid Email')

            else:
                if pic_path.get() != '':
                    new_student_picture = Image.open(pic_path.get()).resize((100,100))
                    new_student_picture.save('temp_pic.png')

                    with open('temp_pic.png','rb') as read_new_pic:
                        new_picture_binary = read_new_pic.read()
                        read_new_pic.close()

                    connection = sqlite3.connect('student_accounts.db')
                    cursor = connection.cursor()

                    cursor.execute(f"UPDATE data SET image=? WHERE id_number == '{student_id}'",[new_picture_binary])

                    connection.commit()
                    connection.close()



                    message_box(message='Data Updated Successfully')

                name = student_name_ent.get()
                age = student_age_ent.get()
                selected_class = select_class_bt.get()
                contact = student_con_ent.get()
                email = student_em_ent.get()

                connection = sqlite3.connect('student_accounts.db')
                cursor = connection.cursor()

                cursor.execute(f"""
                UPDATE data SET name = '{name}', age = '{age}', class = '{selected_class}', phone_number = '{contact}', email = '{email}'
                """)

                connection.commit()
                connection.close()

                get_student_detail = fetch_student_data(f"""
                SELECT name, age, gender, class, phone_number, email FROM data WHERE id_number == '{student_id}'
                """)

                get_student_pic = fetch_student_data(f"""
                SELECT image FROM data WHERE id_number == '{student_id}'
                """)

                student_pic = BytesIO(get_student_pic[0][0])
                message_box(message='Data Updated Successfully')



        student_current_pic = ImageTk.PhotoImage(Image.open(student_pic))



        add_pic_section_fm = tk.Frame(edit_fm, highlightbackground=bg_color, highlightthickness=2)

        add_pic_btn = tk.Button(add_pic_section_fm, image=student_current_pic, bd=0, command=open_pic)
        add_pic_btn.image = student_current_pic
        add_pic_btn.pack()

        add_pic_section_fm.place(x=5, y=5, width=105, height=105)

        student_name = tk.Label(edit_fm, text='Student Full Name.', font=('Bold', 12))
        student_name.place(x=5, y=130)

        student_name_ent = tk.Entry(edit_fm, font=('Bold', 15), highlightcolor=bg_color,
                                    highlightbackground='gray', highlightthickness=2)
        student_name_ent.place(x=5, y=160, width=180)
        student_name_ent.bind('<KeyRelease>', lambda e: remove_warning(entry=student_name_ent))
        student_name_ent.insert(tk.END, get_student_detail[0][0])

        student_age = tk.Label(edit_fm, text='Student Age.', font=('Bold', 12))
        student_age.place(x=5, y=210)

        student_age_ent = tk.Entry(edit_fm, font=('Bold', 15), highlightcolor=bg_color,
                                   highlightbackground='gray', highlightthickness=2)
        student_age_ent.place(x=5, y=235, width=180)
        student_age_ent.bind('<KeyRelease>', lambda e: remove_warning(entry=student_age_ent))
        student_age_ent.insert(tk.END, get_student_detail[0][1])

        student_contact = tk.Label(edit_fm, text='Student Contact.', font=('Bold', 12))
        student_contact.place(x=5, y=285)

        student_con_ent = tk.Entry(edit_fm, font=('Bold', 15), highlightcolor=bg_color,
                                   highlightbackground='gray', highlightthickness=2)
        student_con_ent.place(x=5, y=310, width=180)
        student_con_ent.bind('<KeyRelease>', lambda e: remove_warning(entry=student_con_ent))
        student_con_ent.insert(tk.END, get_student_detail[0][4])

        student_class = tk.Label(edit_fm, text='Student Class.', font=('Bold', 12))
        student_class.place(x=5, y=360)

        select_class_bt = Combobox(edit_fm, font=('Bold', 12), state='readonly', values=class_list)
        select_class_bt.place(x=5, y=385, height=30, width=180)
        select_class_bt.set(get_student_detail[0][3])

        student_email = tk.Label(edit_fm, text='Email Address.', font=('Bold', 12))
        student_email.place(x=5, y=440)

        student_em_ent = tk.Entry(edit_fm, font=('Bold', 15), highlightcolor=bg_color,
                                  highlightbackground='gray', highlightthickness=2)
        student_em_ent.place(x=5, y=470, width=180)
        student_em_ent.bind('<KeyRelease>', lambda e: remove_warning(entry=student_em_ent))
        student_em_ent.insert(tk.END, get_student_detail[0][5])

        update_button = tk.Button(edit_fm,text='Update',font=('Bold',13),bg=bg_color,fg='white',command=check_input)
        update_button.place(x=220,y=470,width=80)



        edit_fm.pack(fill=tk.BOTH,expand=True)

    def delete_page():

        def confirm_delete_account():
            confirm = conformation_box(message="⚠ Do You Want to Delete\nYour Account")

            if confirm:
                connection = sqlite3.connect('student_accounts.db')
                cursor = connection.cursor()

                cursor.execute(f"""
                DELETE FROM data WHERE id_number == '{student_id}'
                """)

                connection.commit()
                connection.close()

                dashboard_fm.destroy()
                wellcome_page()
                root.update()

                message_box(message="Account Successfully Deleted")


        delete_fm = tk.Frame(pages_fm)

        delete_account_lb = tk.Label(delete_fm,text='⚠ Delete Account',font=('Bold',15),bg='red',fg='white')
        delete_account_lb.place(x=30,y=100,width=290)

        delete_account_btn = tk.Button(delete_fm, text='DELETE Account', font=('Bold', 13), bg='red', fg='white',command=confirm_delete_account)
        delete_account_btn.place(x=110, y=200)

        delete_fm.pack(fill=tk.BOTH,expand=True)

    pages_fm = tk.Frame(dashboard_fm)
    pages_fm.place(x=122, y=5, width=350,height=565)
    home_page()



    dashboard_fm.pack(pady=5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.config(width=480,height=580)


# login page
def student_log_in_page():

    def show_hide_password():
        if pass_number_ent['show'] == '*':
            pass_number_ent.config(show='')
            show_hide_btn.config(image=unlocked_img)
        else:
            pass_number_ent.config(show='*')
            show_hide_btn.config(image=locked_img)
    def forward_to_wellcome_page():
        log_page_fm.destroy()
        root.update()
        wellcome_page()

    def remove_warning(entry):
        if entry['highlightbackground']!= 'gray':
            if entry.get() != '':
                entry.config(highlightbackground='gray',highlightcolor=bg_color)

    def login_account():
        verify_id_number = check_data_already(id_number=id_number_ent.get())
        if verify_id_number:
            print("ID is correct")
            verify_password = check_valid_passwoed(id_number=id_number_ent.get(),password=pass_number_ent.get())
            if verify_password:
                id_number = id_number_ent.get()
                log_page_fm.destroy()
                student_dashboard(student_id=id_number)
                root.update()
            else:
                print("Password is Incorrect")
                pass_number_ent.config(highlightbackground='red', highlightcolor='red')
                message_box(message='Please Enter Password')
        else:
            print("ID is incorrect")
            id_number_ent.config(highlightbackground='red', highlightcolor='red')
            message_box(message='Please Enter Valid ID Number')


    log_page_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)

    heading_lb = tk.Label(log_page_fm,text='Student Login Page', bg=bg_color,fg='white',font=('Bold',18))
    heading_lb.place(x=0,y=0,width=400)

    log_ioc = tk.Label(log_page_fm, image=log_in_student)
    log_ioc.place(x=150,y=40)

    bck_btn = tk.Button(log_page_fm,text='←', font=('Bold',20),fg=bg_color,bd=0,command=forward_to_wellcome_page)
    bck_btn.place(x=5,y=40)

    id_number_lb = tk.Label(log_page_fm,text='Enter Student ID Number.', fg=bg_color,font=('Bold',15))
    id_number_lb.place(x=80,y=140)

    id_number_ent = tk.Entry(log_page_fm,font=('Bold',15),justify=tk.CENTER,highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    id_number_ent.place(x=80,y=190)
    id_number_ent.bind('<KeyRelease>',lambda e:remove_warning(entry=id_number_ent))

    pass_number_lb = tk.Label(log_page_fm,text='Enter Student Password.', fg=bg_color,font=('Bold',15))
    pass_number_lb.place(x=80,y=240)

    pass_number_ent = tk.Entry(log_page_fm,font=('Bold',15),justify=tk.CENTER,highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2,show='*')
    pass_number_ent.place(x=80,y=290)
    pass_number_ent.bind('<KeyRelease>', lambda e: remove_warning(entry=pass_number_ent))

    show_hide_btn = tk.Button(log_page_fm,image=locked_img, bd=0,command=show_hide_password)
    show_hide_btn.place(x=310,y=280)


    login_bt = tk.Button(log_page_fm,text='Login',font=('Bold',15),bg=bg_color,fg='white',command=login_account)
    login_bt.place(x=95,y=340,width=200,height=40)

    forget_bt = tk.Button(log_page_fm,text='⚠\nForget Password',fg=bg_color,bd=0,command=forget_password_page)
    forget_bt.place(x=95,y=390,width=200,height=40)



    log_page_fm.pack(pady=30)
    log_page_fm.pack_propagate(False)
    log_page_fm.config(width=400, height=450)


##################   admin dashboar #################################

def admin_dashboard():

    def switch(indicator,page):
        home_indicator_btn.config(bg='#c3c3c3')
        student_find_indicator_btn.config(bg='#c3c3c3')
        student_announcement_indicator_btn.config(bg='#c3c3c3')

        indicator.config(bg=bg_color)

        for child in pages_fm.winfo_children():
            child.destroy()
            root.update()

        page()




    dashboard_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)


    option_fm = tk.Frame(dashboard_fm, highlightthickness=2, highlightbackground=bg_color, bg='#c3c3c3')
    option_fm.place(x=0, y=0, width=120, height=575)

    home_btn = tk.Button(dashboard_fm, text='Home', font=('Bold', 15), bg='#c3c3c3', fg=bg_color, bd=0,command=lambda: switch(indicator=home_indicator_btn,page=home_page))
    home_btn.place(x=10, y=50)

    home_indicator_btn = tk.Label(dashboard_fm,text='', bg=bg_color)
    home_indicator_btn.place(x=5, y=48, width=3, height=40)

    student_find_btn = tk.Button(dashboard_fm, text='Find\nStudent', font=('Bold', 15), bg='#c3c3c3', fg=bg_color, bd=0,command=lambda: switch(indicator=student_find_indicator_btn,page=find_student_page))
    student_find_btn.place(x=10, y=100)

    student_find_indicator_btn = tk.Label(dashboard_fm,text='', bg='#c3c3c3')
    student_find_indicator_btn.place(x=5, y=108, width=3, height=40)

    student_announcement_btn = tk.Button(dashboard_fm, text='Annou📢\n-ncement', font=('Bold', 15), bg='#c3c3c3', fg=bg_color, bd=0,command=lambda :switch(indicator=student_announcement_indicator_btn,page=announcement_page))
    student_announcement_btn.place(x=10, y=170)

    student_announcement_indicator_btn = tk.Label(dashboard_fm, text='',bg='#c3c3c3')
    student_announcement_indicator_btn.place(x=5, y=180, width=3, height=40)

    def logout():
        confirm = conformation_box(message="Do You Want to\nLogout")

        if confirm:
            dashboard_fm.destroy()
            wellcome_page()
            root.update()

    logout_btn = tk.Button(dashboard_fm, text='Logout', font=('Bold', 15), bg='#c3c3c3', fg=bg_color, bd=0, command=logout)
    logout_btn.place(x=10, y=250)

    def home_page():

        class_list = ["5th","6th","7th","8th","9th","10th","11th","12th"]

        home_page_fm = tk.Frame(pages_fm)
        admin_login_ion = tk.Label(home_page_fm,image=log_in_student1)
        admin_login_ion.image = log_in_student2
        admin_login_ion.place(x=10,y=10)

        hi_lb = tk.Label(home_page_fm,text='!Hi Admin',font=('Bold',15))
        hi_lb.place(x=120,y=40)

        class_list_lb = tk.Label(home_page_fm,text='Number of Student by Class.',font=('Bold',13),bg=bg_color,fg='white')
        class_list_lb.place(x=20,y=130)

        student_number_lb = tk.Label(home_page_fm,text='',font=('Bold',13),justify=tk.LEFT)
        student_number_lb.place(x=20,y=170)

        for i in class_list:
            result = fetch_student_data(query=f"SELECT COUNT(*) FROM data WHERE class == '{i}'")

            student_number_lb['text'] += f"{i} Class :{result[0][0]}\n\n"



        home_page_fm.pack(fill = tk.BOTH,expand=True)

    def find_student_page():

        def find_student():

            if find_by_option_btn.get() == 'id':
                found_data = fetch_student_data(query=f"""
                SELECT id_number, name, class, gender, age FROM data WHERE id_number == '{search_input.get()}'
                """)

                print(found_data)

            elif find_by_option_btn.get() == 'name':
                found_data = fetch_student_data(query=f"""
                SELECT id_number, name, class, gender, age FROM data WHERE name LIKE '%{search_input.get()}%'
                """)

                print(found_data)

            elif find_by_option_btn.get() == 'class':
                found_data = fetch_student_data(query=f"""
                SELECT id_number, name, class, gender, age FROM data WHERE class == '{search_input.get()}'
                """)

                print(found_data)

            elif find_by_option_btn.get() == 'age':
                found_data = fetch_student_data(query=f"""
            SELECT id_number, name, class, gender, age FROM data WHERE age == '{search_input.get()}'
                """)


                print(found_data)

            elif find_by_option_btn.get() == 'gender':
                found_data = fetch_student_data(query=f"""
            SELECT id_number, name, class, gender, age FROM data WHERE gender == '{search_input.get()}'
                """)

                print(found_data)

            if found_data:

                for item in record_table.get_children():
                    record_table.delete(item)

                for details in found_data:
                    record_table.insert(parent='',index='end',values=details)

            else:
                for item in record_table.get_children():
                    record_table.delete(item)

        def generate_student_card():
            selection = record_table.selection()
            selected_id = record_table.item(item=selection, option='values')[0]


            get_student_detail = fetch_student_data(f"""
                SELECT name, age, gender, class, phone_number, email FROM data WHERE id_number == '{selected_id}'
                """)

            get_student_pic = fetch_student_data(f"""
                    SELECT image FROM data WHERE id_number == '{selected_id}'
                    """)

            student_pic = BytesIO(get_student_pic[0][0])

            student_details = f"""
{selected_id}
{get_student_detail[0][0]}
{get_student_detail[0][1]}
{get_student_detail[0][2]}
{get_student_detail[0][4]}
{get_student_detail[0][3]}
{get_student_detail[0][5]}
"""

            student_card_image_obj = draw_card(student_pic_path=student_pic, student_data=student_details)
            student_card(student_card_obj=student_card_image_obj,bypass_login_page=True)
            #student_card_img = ImageTk.PhotoImage(student_card_image_obj)

        def clear_result():
            find_by_option_btn.set('id')
            search_input.delete(0, tk.END)

            for items in record_table.get_children():
                record_table.delete(items)


        search_filter = ['id','name','class','gender','age']

        find_student_page_fm = tk.Frame(pages_fm)

        find_student_record_lb = tk.Label(find_student_page_fm,text='Find Student Record',font=('Bold',13),fg='white',bg=bg_color)
        find_student_record_lb.place(x=20,y=10,width=300)

        find_student_by_lb = tk.Label(find_student_page_fm, text='Find By', font=('Bold', 13))
        find_student_by_lb.place(x=15, y=50)

        find_by_option_btn = Combobox(find_student_page_fm,font=('Bold',11),state='readonly',values=search_filter)
        find_by_option_btn.place(x=80,y=50,width=80)
        find_by_option_btn.set('id')

        search_input = tk.Entry(find_student_page_fm,font=('Bold',12))
        search_input.place(x=20,y=90)
        search_input.bind('<KeyRelease>', lambda  e:find_student())

        record_table_lb = tk.Label(find_student_page_fm,text='Record Table',font=('Bold',12),bg=bg_color,fg='white')
        record_table_lb.place(x=20,y=160,width=300)

        record_table = Treeview(find_student_page_fm)
        record_table.place(x=0,y=200,width=350)
        record_table.bind('<<TreeviewSelect>>',lambda e:generate_student_card.config(state=tk.NORMAL))

        record_table['columns'] = ('id','name','class','gender','age')

        record_table.column('#0',stretch=tk.NO,width=0)

        record_table.heading('id',text='ID Number',anchor=tk.W)
        record_table.column('id',width=50,anchor=tk.W)
        record_table.heading('name', text='Name', anchor=tk.W)
        record_table.column('name', width=90, anchor=tk.W)
        record_table.heading('class', text='Class', anchor=tk.W)
        record_table.column('class', width=30, anchor=tk.W)
        record_table.heading('gender', text='Gender', anchor=tk.W)
        record_table.column('gender', width=40, anchor=tk.W)
        record_table.heading('age', text='Age', anchor=tk.W)
        record_table.column('age', width=30, anchor=tk.W)

        generate_student_card = tk.Button(find_student_page_fm,text='Generate Student Card',font=('Bold',13),bg=bg_color,fg='white',state=tk.DISABLED,
                                          command=generate_student_card)
        generate_student_card.place(x=10,y=450)

        clear_btn = tk.Button(find_student_page_fm, text='Clear', font=('Bold', 13), bg=bg_color, fg='white',command=clear_result)
        clear_btn.place(x=250, y=450)

        find_student_page_fm.pack(fill=tk.BOTH,expand=True)

    def announcement_page():

        selected_class = []

        def add_class(name):
            if selected_class.count(name):
                selected_class.remove(name)
            else:

                selected_class.append(name)
            print(selected_class)

        def collect_email():
            fetched_email = []
            for _class in selected_class:
                emails = fetch_student_data(f"SELECT email FROM data WHERE class == '{_class}'")

                for email_address in emails:
                    fetched_email.append(*email_address)

            thread = threading.Thread(target=send_announcement, args=[fetched_email])
            thread.start()

        def send_announcement(email_addresses):
            box_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)

            heading_ld = tk.Label(box_fm,text='Sending Email',font=('Bold',12),fg='white',bg=bg_color)
            heading_ld.place(x=0,y=0,width=300)

            sending_lb = tk.Label(box_fm,justify=tk.LEFT,font=('Bold',12))
            sending_lb.pack(pady=50)


            box_fm.place(x=100,y=120,width=300,height=200)

            message = f"<h3 style= 'white-space:pre-wrap'>{announcement_message.get(0.1,tk.END)}</h3>"

            subject = announcement_subject.get()

            sent_count=0

            for email in email_addresses:
                sending_lb.config(text=f"Sending To:\n{email}\n\n{sent_count}/{len(email_addresses)}")

                send_mail_to_student(email=email,subject=subject,message=message)

                sent_count += 1
                sending_lb.config(text=f"Sending To:\n{email}\n\n{sent_count}/{len(email_addresses)}")

            box_fm.destroy()
            message_box(message="Announcement Sent\n Successfully")
            root.update()




        class_list = ["5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"]

        announcement_page_fm = tk.Frame(pages_fm)

        subject_ld = tk.Label(announcement_page_fm,text='Enter Announcement Subject',font=('Bold',12))
        subject_ld.place(x=10,y=10)

        announcement_subject = tk.Entry(announcement_page_fm,font=('Bold',12))
        announcement_subject.place(x=10,y=40,height=25,width=210)

        announcement_message = ScrolledText(announcement_page_fm,font=('Bold',12))
        announcement_message.place(x=10,y=100,height=200,width=300)

        classes_list_ld = tk.Label(announcement_page_fm,font=('Bold',12),text='Select Classes to Announcement')
        classes_list_ld.place(x=10,y=320)

        y_position =350

        for grade in class_list:
            class_check_btn = tk.Checkbutton(announcement_page_fm,text=f"Class {grade}",command=lambda grade=grade: add_class(name=grade))
            class_check_btn.place(x=10,y=y_position)
            y_position += 25

        send_announcement_btn = tk.Button(announcement_page_fm,text='Send Announcement',font=('Bold',12),bg=bg_color,fg='white',command=collect_email)
        send_announcement_btn.place(x=180,y=520)


        announcement_page_fm.pack(fill=tk.BOTH,expand=True)

    pages_fm = tk.Frame(dashboard_fm)
    pages_fm.place(x=122,y=5,width=350,height=550)

    home_page()
    #find_student_page()
    #announcement_page()

    dashboard_fm.pack(pady=5)
    dashboard_fm.propagate(False)
    dashboard_fm.config(height=580,width=480)


#admin login page
def admin_login_page():

    def show_hide_password1():
        if pss_number_ent['show'] == '*':
            pss_number_ent.config(show='')
            show_hide_btn1.config(image=unlocked_img)
        else:
            pss_number_ent.config(show='*')
            show_hide_btn1.config(image=locked_img)

    def backward_to_admin_login_page():
        admin_login_page.destroy()
        root.update()
        wellcome_page()

    def login_account():
        if id_number_ent1.get() == 'admin':

            if pss_number_ent.get() == 'admin':
               admin_login_page.destroy()
               root.update()
               admin_dashboard()
            else:
                message_box(message='Password is Incorrect')

        else:
            message_box(message='Username is Invalid')


    admin_login_page = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)

    heading_lab = tk.Label(admin_login_page,text='Admin Login Page', bg=bg_color,fg='white',font=('Bold',18))
    heading_lab.place(x=0,y=0,width=400)

    bck_btn1 = tk.Button(admin_login_page, text='←', font=('Bold', 20), fg=bg_color, bd=0, command=backward_to_admin_login_page)
    bck_btn1.place(x=5, y=40)

    log_iocn = tk.Label(admin_login_page, image=log_in_student)
    log_iocn.place(x=150,y=40)

    id_number_lab = tk.Label(admin_login_page,text='Enter Admin User Name.', fg=bg_color,font=('Bold',15))
    id_number_lab.place(x=80,y=140)

    id_number_ent1 = tk.Entry(admin_login_page,font=('Bold',15),justify=tk.CENTER,highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    id_number_ent1.place(x=80,y=190)

    pass_number_lab = tk.Label(admin_login_page,text='Enter Admin Password.', fg=bg_color,font=('Bold',15))
    pass_number_lab.place(x=80,y=240)

    pss_number_ent = tk.Entry(admin_login_page,font=('Bold',15),justify=tk.CENTER,highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2,show='*')
    pss_number_ent.place(x=80,y=290)

    show_hide_btn1 = tk.Button(admin_login_page,image=locked_img, bd=0,command=show_hide_password1)
    show_hide_btn1.place(x=310,y=280)


    login_btn = tk.Button(admin_login_page,text='Login',font=('Bold',15),bg=bg_color,fg='white',command=login_account)
    login_btn.place(x=95,y=340,width=200,height=40)

    forget_btn = tk.Button(admin_login_page,text='⚠\nForget Password',fg=bg_color,bd=0)
    forget_btn.place(x=95,y=390,width=200,height=40)

    admin_login_page.pack(pady=30)
    admin_login_page.pack_propagate(False)
    admin_login_page.config(width=400, height=450)

##### create account ######
def create_acc():
    pic_path = tk.StringVar()
    pic_path.set('')

    def open_pic():
        path = askopenfilename()
        if path:
            img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
            pic_path.set(path)

            add_pic_btn.config(image=img)
            add_pic_btn.image = img

    student_gen = tk.StringVar()

    class_list = ["5th","6th","7th","8th","9th","10th","11th","12th"]

    def backward_wellcome():
        ans=conformation_box(message='Do You Want to Leave\nRegistration Form')

        if ans:

            add_account_page_fm.destroy()
            root.update()
            wellcome_page()

    def remove_warning(entry):
        if entry['highlightbackground']!= 'gray':
            if entry.get() != '':
                entry.config(highlightbackground='gray',highlightcolor=bg_color)

    def check_invalid_email(email):
        pattern = "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"
        match = re.match(pattern=pattern, string=email)
        return match

    def generate_id():
        generated_id=''
        for r in range(6):
            generated_id += str(random.randint(0,9))
        if not check_data_already(id_number=generated_id):
            print('id_number:',generated_id)
            student_id_ent.config(state=tk.NORMAL)
            student_id_ent.delete(0, tk.END)
            student_id_ent.insert(tk.END,generated_id)
            student_id_ent.config(state='readonly')
        else:
            generate_id()


    def check_input_validation():
        if student_name_ent.get() == '':
            student_name_ent.config(highlightcolor='red',highlightbackground='red')
            student_name_ent.focus()
            message_box('Student Name is Required.')
        elif student_age_ent.get() == '':
            student_age_ent.config(highlightcolor='red',highlightbackground='red')
            student_age_ent.focus()
            message_box('Student Age is Required.')
        elif student_con_ent.get() == '':
            student_con_ent.config(highlightcolor='red',highlightbackground='red')
            student_con_ent.focus()
            message_box('Student Contact is Required.')
        elif select_class_bt.get() == '':
            select_class_bt.focus()
            message_box('Student Class is Required.')
        elif student_em_ent.get() == '':
            student_em_ent.config(highlightcolor='red',highlightbackground='red')
            student_em_ent.focus()
            message_box('Student Email is Required.')
        elif not check_invalid_email(email=student_em_ent.get().lower()):
            student_em_ent.config(highlightcolor='red', highlightbackground='red')
            student_em_ent.focus()
            message_box('Enter a valid Email.')
        elif account_em_ent.get() == '':
            account_em_ent.config(highlightcolor='red',highlightbackground='red')
            account_em_ent.focus()
            message_box('Student password is Required.')
        else:
            pic_data = b''
            if pic_path.get() !='':
                resize_pic = Image.open(pic_path.get()).resize((100,100))
                resize_pic.save('temp.png')
                read_data = open('temp.png','rb')
                pic_data = read_data.read()
                read_data.close()
            else:
                read_data = open('C:/Users/DELL/Downloads/Images/add_student_img.png','rb')
                pic_data = read_data.read()
                read_data.close()

                pic_path.set('C:/Users/DELL/Downloads/Images/add_student_img.png')

            add_data(id_number=student_id_ent.get(),
                     password=account_em_ent.get(),
                     name=student_name_ent.get(),
                     age=student_age_ent.get(),
                     gender=student_gen.get(),
                     phone_number=student_con_ent.get(),
                     student_class=select_class_bt.get(),
                     email=student_em_ent.get(),
                     pic_data=pic_data)


            data = f"""
{student_id_ent.get()}
{student_name_ent.get()}
{student_age_ent.get()}
{student_gen.get()}
{student_con_ent.get()}
{select_class_bt.get()}
{student_em_ent.get()}           
"""
            get_student_card = draw_card(student_pic_path=pic_path.get(),student_data=data)
            student_card(student_card_obj=get_student_card)

            add_account_page_fm.destroy()
            root.update()

            message_box('Account Added Successful')



    add_account_page_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)

    add_pic_section_fm = tk.Frame(add_account_page_fm,highlightbackground=bg_color,highlightthickness=2)

    add_pic_btn = tk.Button(add_pic_section_fm,image=add_student_pic_ioc,bd=0,command=open_pic)
    add_pic_btn.pack()

    add_pic_section_fm.place(x=5,y=5,width=105,height=105)

    student_name = tk.Label(add_account_page_fm,text='Enter Student Full Name.',font=('Bold',12))
    student_name.place(x=5,y=130)

    student_name_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    student_name_ent.place(x=5,y=160,width=180)
    student_name_ent.bind('<KeyRelease>',lambda e:remove_warning(entry=student_name_ent))

    student_gender = tk.Label(add_account_page_fm,text='Select Student Gender.',font=('Bold',12))
    student_gender.place(x=5,y=210)

    male_gender = tk.Radiobutton(add_account_page_fm,text='Male',font=('Bold',12),variable=student_gen,value='male')
    male_gender.place(x=5,y=235)

    female_gender = tk.Radiobutton(add_account_page_fm,text='female',font=('Bold',12),variable=student_gen,value='female')
    female_gender.place(x=75,y=235)
    student_gen.set('male')

    student_age = tk.Label(add_account_page_fm,text='Enter Student Age.',font=('Bold',12))
    student_age.place(x=5,y=275)

    student_age_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    student_age_ent.place(x=5,y=305,width=180)
    student_age_ent.bind('<KeyRelease>', lambda e: remove_warning(entry=student_age_ent))

    student_contact = tk.Label(add_account_page_fm,text='Enter Student Contact.',font=('Bold',12))
    student_contact.place(x=5,y=360)

    student_con_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    student_con_ent.place(x=5,y=390,width=180)
    student_con_ent.bind('<KeyRelease>', lambda e: remove_warning(entry=student_con_ent))

    student_class = tk.Label(add_account_page_fm,text='Select Student Class.',font=('Bold',12))
    student_class.place(x=5,y=445)

    select_class_bt = Combobox(add_account_page_fm,font=('Bold',12),state='readonly',values=class_list)
    select_class_bt.place(x=5,y=475,height=30,width=180)

    student_id = tk.Label(add_account_page_fm,text='Student ID Number:',font=('Bold',12))
    student_id.place(x=240,y=35)

    student_id_ent = tk.Entry(add_account_page_fm,font=('Bold',18),bd=0)
    student_id_ent.place(x=380,y=35,width=80)


    student_id_ent.config(state='readonly')
    generate_id()

    id_info = tk.Label(add_account_page_fm,text="""Automatically Generated ID Number
! Remember Using This ID Number
Student Will Login Account.""",justify=tk.LEFT)
    id_info.place(x=240,y=65)

    student_email = tk.Label(add_account_page_fm,text='Enter Email Address.',font=('Bold',12))
    student_email.place(x=240,y=130)

    student_em_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    student_em_ent.place(x=240,y=160,width=180)
    student_em_ent.bind('<KeyRelease>', lambda e: remove_warning(entry=student_em_ent))

    em_info = tk.Label(add_account_page_fm,text="""Via Email Address Student
Can Recover Account
! In Case Forgetting Password And Also
Student will get Future Notification.""",justify=tk.LEFT)
    em_info.place(x=240,y=200)

    account_pass = tk.Label(add_account_page_fm,text='Create Account Password.',font=('Bold',12))
    account_pass.place(x=240,y=270)

    account_em_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    account_em_ent.place(x=240,y=307,width=180)
    account_em_ent.bind('<KeyRelease>', lambda e: remove_warning(entry=account_em_ent))

    ac_info = tk.Label(add_account_page_fm,text="""Via Student Create Password
And Provided Student ID Number
Student can Login the Account.""",justify=tk.LEFT)
    ac_info.place(x=240,y=345)

    home_bt = tk.Button(add_account_page_fm,text='Home',font=('Bold',15),bg='red',fg='white',bd=1,command=backward_wellcome)
    home_bt.place(x=240,y=420)

    sub_bt = tk.Button(add_account_page_fm,text='Submit',font=('Bold',15),bg='blue',fg='white',bd=1,command=check_input_validation)
    sub_bt.place(x=360,y=420)


    add_account_page_fm.pack(pady=5)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.config(width=480,height=580)


###   conformation box############################################################################################
#init_database()
#student_card()
#forget_password_page()
#create_acc()
#student_dashboard(student_id=115148)
#student_log_in_page()
#admin_dashboard()
#admin_login_page()

wellcome_page()
root.mainloop()