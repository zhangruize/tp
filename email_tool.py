# coding:utf8
import codecs
import getopt
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class EmailSender:
    def __init__(self, password, user, to_list, tag, body):
        self.to_list = to_list
        self.user = user
        self.tag = tag
        self.cc_list = []
        self.doc = None
        self.mailServer = 'smtp.qq.com'
        self.port = '465'
        self.pwd = password
        self.content = body

    def send(self):
        try:
            server = smtplib.SMTP_SSL(self.mailServer, self.port)
            server.login(self.user, pwd)
            server.sendmail("<%s>" % from_email, to_email, self._get_attach())
            server.quit()
            print("send email successful")
        except Exception as e:
            print("send email failed {}".format(e))

    def _get_attach(self):
        '''
        构造邮件内容
        '''
        attach = MIMEMultipart()

        # 添加邮件内容
        # txt = MIMEText(self.content, 'plain', 'utf-8')
        txt = MIMEText(self.content, 'plain', 'utf-8')
        attach.attach(txt)

        if self.tag is not None:
            # 主题,最上面的一行
            attach["Subject"] = self.tag
        if self.user is not None:
            # 显示在发件人
            # attach["From"] = "Jd.Id Android<%s>"%self.user
            attach['From'] = formataddr(["Jd.Id Android", self.user])
        if self.to_list:
            # 收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            # 抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.doc:
            # 估计任何文件都可以用base64，比如rar等
            # 文件名汉字用gbk编码代替
            name = os.path.basename(self.doc).encode("gbk")
            f = open(self.doc, "rb")
            doc = MIMEText(f.read(), "base64", "gb2312")
            doc["Content-Type"] = 'application/octet-stream'
            doc["Content-Disposition"] = 'attachment; filename="' + name + '"'
            attach.attach(doc)
            f.close()
        return attach.as_string()


def send_email():
    print('start send emails !!!')

    sender = EmailSender(pwd, from_email, to_email, subject, content)
    sender.send()


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "p:f:t:c:i:s:")
    arg_map = {}
    for opt, arg in opts:
        arg_map[opt] = arg
    pwd = arg_map['-p']
    from_email = arg_map['-f']
    to_email = arg_map['-t'].split(',')
    subject = arg_map['-s']
    content = ''
    if '-c' in arg_map:
        content = arg_map['-c']
    elif '-i' in arg_map:
        with codecs.open(arg_map['-i'], 'r') as f:
            content += f.read()

    send_email()
