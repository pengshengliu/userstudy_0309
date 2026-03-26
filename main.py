import streamlit as st
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import poplib
from email.parser import Parser

@st.cache_data
def send_email(email, password, array):
    # 构建邮件主体
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email  # 收件人邮箱
    msg['Subject'] = fr'{dataset} Number of submissions'
    
    # 邮件正文
    #string = ''.join([str(element) for element in array])
    string = str(array)
    text = MIMEText(string)
    msg.attach(text)
     
    # 发送邮件
    try:
        smtp = smtplib.SMTP('smtp.126.com')
        smtp.login(email, password)
        smtp.sendmail(email, email, msg.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        print('邮件发送失败，错误信息：', e)

@st.cache_data
def read_email(myemail, password):
    try:
        pop3_server = 'pop.126.com'
        subject_to_search = f'{dataset} Number of submissions'

        # 连接到 POP3 服务器
        mail_server = poplib.POP3_SSL(pop3_server, 995)
        mail_server.user(myemail)
        mail_server.pass_(password)

        # 搜索符合特定主题的邮件
        num_messages = len(mail_server.list()[1])
        content = None  # 初始化变量
        found = False
        for i in range(num_messages, 0, -1):
            raw_email = b'\n'.join(mail_server.retr(i)[1]).decode('utf-8')
            email_message = Parser().parsestr(raw_email)
            subject = email_message['Subject']
            
            if subject == subject_to_search:
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode(part.get_content_charset())
                        found = True
                        break  # 找到满足条件的邮件后及时跳出循环
                if found:
                    break

        # 关闭连接
        mail_server.quit()
        array = [int(char) for char in content]
        result = int("".join(map(str, array)))
        return result

    except Exception as e:
        st.error('网络问题，请刷新页面')

@st.cache_data
def read_email_(myemail, password):
    try:
        pop3_server = 'pop.126.com'
        subject_to_search = f'{dataset} Number of submissions'

        # 连接到 POP3 服务器
        mail_server = poplib.POP3_SSL(pop3_server, 995)
        mail_server.user(myemail)
        mail_server.pass_(password)

        # 搜索符合特定主题的邮件
        num_messages = len(mail_server.list()[1])
        content = None  # 初始化变量
        found = False
        for i in range(num_messages, 0, -1):
            raw_email = b'\n'.join(mail_server.retr(i)[1]).decode('utf-8')
            email_message = Parser().parsestr(raw_email)
            subject = email_message['Subject']
            
            if subject == subject_to_search:
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode(part.get_content_charset())
                        found = True
                        break  # 找到满足条件的邮件后及时跳出循环
                if found:
                    break

        # 关闭连接
        mail_server.quit()
        array = [int(char) for char in content]
        result = int("".join(map(str, array)))
        return result

    except Exception as e:
        st.error('网络问题，请刷新页面')

@st.cache_data
def data_collection(email, password, human_likeness, smoothness, semantic_accuracy, count):
    # 发送内容
    data1 = ''.join(str(x) for x in human_likeness)
    data2 = ''.join(str(x) for x in smoothness)
    data3 = ''.join(str(x) for x in semantic_accuracy)
    string = data1 + "\n" + data2 + "\n" + data3
    localtime = datetime.strptime(time.strftime('%m-%d %H-%M-%S', time.localtime()), '%m-%d %H-%M-%S')
    localtime += timedelta(hours=8)
    seconds = localtime.strftime('%S')
    localtime = localtime.strftime('%m-%d %H-%M-%S')
    # 打开文件并指定写模式
    ID = f"{count}-{seconds}"
    file_name = dataset + ' ' + str(count) + ' ' + localtime + ".txt"
    file = open(file_name, "w")
    # 将字符串写入文件
    file.write(string)
    # 关闭文件
    file.close()

    # 构建邮件主体
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email  # 收件人邮箱
    msg['Subject'] = dataset + ' ' + str(count) + ' '  + localtime

    # 邮件正文
    text = MIMEText(string)
    msg.attach(text)

    # 添加附件
    with open(file_name, 'rb') as f:
        attachment = MIMEApplication(f.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(attachment)

    # 发送邮件
    try:
        smtp = smtplib.SMTP('smtp.126.com')
        smtp.login(email, password)
        smtp.sendmail(email, email, msg.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        print('邮件发送失败，错误信息：', e)

    return ID, localtime

@st.cache_data
def instrunction():
    st.header("Instructions: ")
    st.markdown('''请仔细阅读以下对本研究的介绍，您需要在这几个虚拟人之间进行评分：''')
    st.markdown('''##### 1. 手势真实性评分''')
    st.markdown('''请观察视频中虚拟角色的手势，并判断其是否符合人类的真实行为习惯。重点关注手臂动作及整体姿势的真实感。手势是否流畅、协调，避免出现僵硬或过于突兀的手势动作。''')
    st.markdown('''##### 2. 手势多样性评分''')
    st.markdown('''观察虚拟角色在视频中的手势类型是否丰富多样。判断手势是否存在重复、单一或模式化的情况，评估整体手势表现是否具有变化性和表现力，而非机械重复。''')
    st.markdown('''##### 3. 语音与手势同步性评分''')
    st.markdown('''观察虚拟角色的手势动作是否与语音的节奏、语调和停顿保持一致。评估手势是否能够自然地跟随语音变化，而不会出现明显的提前、滞后或不协调现象。''')
    st.markdown('''###### 注意事项：本实验专注于手势动作，不需要关注面部表情。''')
    st.markdown('''###### 手机端用户可以在手机横屏状态下答题，如遇卡顿和视频播放不了的情况，建议在电脑端答题。''')

def QA(human_likeness, smoothness, semantic_accuracy, num, method_num):
    number = (num-1) * method_num - 1

    for i in range(1, method_num+1):
        col1, col2, col3, col4 = st.columns(4, gap="large")
        with col1:
            if i==1 : st.markdown(' .')
            st.write(f"第 {i} 个人")
        st.divider()
        with col2:
            if i==1 : st.markdown('''真实性''')
            human_likeness[number+i] = st.feedback("stars", key=f"button{num}.{i}")
        with col3:
            if i==1 : st.markdown('''多样性''')
            smoothness[number+i] = st.feedback("stars", key=f"button{num}.{i+5}")
        with col4:
            if i==1 : st.markdown('''语音与手势同步性''')
            semantic_accuracy[number+i] = st.feedback("stars", key=f"button{num}.{i+10}")

    # 检查是否有评分为None
    if None in human_likeness[number+1:number+4] or None in smoothness[number+1:number+4] or None in semantic_accuracy[number+1:number+4]:
        return False
    
    return True   
    
@st.cache_data
def play_video(file_name):
    video_bytes = open(file_name, 'rb').read()
    return video_bytes

def page(video_num, method_num, random_num):
    instrunction()
    file = open(r"filenames_beat2.txt", "r", encoding='utf-8') 
    file_list = file.readlines()
    file.close()

    def switch_page(page_num):
        st.session_state["page_num"] = page_num
        st.session_state["human_likeness"] = human_likeness 
        st.session_state["smoothness"] = smoothness 
        st.session_state["semantic_accuracy"] = semantic_accuracy
        st.rerun()  # 清空页面

    # 通过 st.session_state 实现页面跳转
    if "page_num" not in st.session_state:
        st.session_state["page_num"] = 1

    num = st.session_state["page_num"]

    st.subheader(fr"Video {num} / {video_num}")
    cur_num = random_num * video_num + num
    #st.write(file_list[num-1].rstrip())

    #st.write(f'这是第{cur_num}个视频，名称为{file_list[cur_num-1].rstrip()}')
    video_bytes = play_video(file_list[cur_num-1].rstrip())
    #video_bytes = play_video(r"E:\UserStudy\Comparsion\2_scott_0_1_1.mp4")
    st.video(video_bytes)

    st.write("视频从左到右，依次对应第一个人，第二个人。")
    st.write("请评分1 - 5，1为最差，5为最好。")
    res = QA(human_likeness, smoothness, semantic_accuracy, num, method_num)

    # 第1页
    if st.session_state["page_num"] == 1:
        if st.button("下一页"):
            if res:
                switch_page(st.session_state["page_num"] + 1)
            else:
                st.warning("请回答当前页问题！")

    # 中间页
    if num > 1 and num < video_num:
        col1, col2 = st.columns(2)
        if col2.button("上一页"):
            switch_page(st.session_state["page_num"] - 1)
        if col1.button("下一页"):
            if res:
                switch_page(st.session_state["page_num"] + 1)
            else:
                st.warning("请回答当前页问题！")

    # 最后一页
    if st.session_state["page_num"] == video_num:
        col1, col2 = st.columns(2)
        if "button_clicked" not in st.session_state:
            st.session_state.button_clicked = False

        if not st.session_state.button_clicked:
            if col1.button("提交结果"):
                if not res:
                    st.warning("请回答当前页问题！")
                else:
                    st.write('提交中...请耐心等待...')
                    count = read_email_(myemail, password)
                    count += 1
                    send_email(myemail, password, count)
                    ID, localtime = data_collection(myemail, password, human_likeness, smoothness, semantic_accuracy, count)
                    st.divider()
                    st.markdown(':blue[请对下面的结果进行截图。]')
                    st.write("**Result:**")
                    st.write("真实性: ", str(human_likeness))
                    st.write("多样性: ", str(smoothness))
                    st.write("语音与手势同步性: ", str(semantic_accuracy))
                    st.write("**提交时间:** ", localtime)
                    st.write("**提交ID:** ", ID)
                    st.session_state.button_clicked = True 

        if st.session_state.button_clicked == True:
            st.cache_data.clear()
            st.success("结果已成功提交，感谢使用。")

        if col2.button("上一页"):
            switch_page(st.session_state["page_num"] - 1)


if __name__ == '__main__':
    import random

    st.set_page_config(page_title="userstudy")
    st.cache_data.clear() # 初始化
    myemail = st.secrets["my_email"]["email"]  
    password = st.secrets["my_email"]["password"]
    video_num = 15
    method_num = 2
    dataset = "beat2"

    count = read_email(myemail, password)
    #print(count)
    #st.write(count)
    #count = 0

    if count>=30: 
        st.error("本场答题人数已满，感谢你的关注！")
        st.cache_data.clear()
    else:
        if "human_likeness" and "smoothness" and "semantic_accuracy" not in st.session_state:
            human_likeness = [1 for x in range(video_num*method_num)]
            smoothness = [1 for x in range(video_num*method_num)]
            semantic_accuracy = [1 for x in range(video_num*method_num)]
        else:
            human_likeness = st.session_state["human_likeness"]
            smoothness = st.session_state["smoothness"]
            semantic_accuracy = st.session_state["semantic_accuracy"]

        random_num = 0
        random_range = 60 // video_num
        if 'random_num' not in st.session_state:
            st.session_state.random_num = random.randint(0, random_range-1)
        random_num = st.session_state.random_num

        page(video_num, method_num, random_num)
