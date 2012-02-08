





#import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
 
EMAIL_HOST = 'smtp.comcast.net'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'andremara'
EMAIL_HOST_PASSWORD = 'pw goes here'
EMAIL_FROM = "WMSAutomation@FranklinStorage.com"
EMAIL_TO = "andremara@verizon.net"

#get the contents of the error file that foxpro made
errfile='c:/Projects/Pythonlearn/MrgOuErr.txt'
fp = open(errfile,'rb')
ErrMsgPre = fp.read()
fp.close()
ErrMsgTriArray=ErrMsgPre.partition('Batch Details:')


#merge errors into html template file 
txtfile='c:/Projects/Pythonlearn/MailMrgO.template'
fp = open(txtfile, 'rb')
msghtml=(fp.read())
fp.close()
msghtml=msghtml.replace('_errorsummary_',ErrMsgTriArray[0])
msghtml=msghtml.replace('_errordetail_',ErrMsgTriArray[2])
# We reference the image in the IMG SRC attribute by the ID we give it below
msghtml=msghtml+'<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!'
#...and also merge errors into plain text template file, 
#to cover our bases in case client can't do html
txtfile='c:/Projects/Pythonlearn/MailMrgOTXT.template'
fp = open(txtfile, 'rb')
msgtxt=(fp.read())
fp.close()
msgtxt=msgtxt.replace('_errorsummary_',ErrMsgTriArray[0])
msgtxt=msgtxt.replace('_errordetail_',ErrMsgTriArray[2])

#prepare text and html messages for MIME 
plaintext = MIMEText(msgtxt, 'plain')
htmltext = MIMEText(msghtml,'html')

#pesky html break <br> and newlines /n mess up the email. get rid of em.
subj='Outbound Merge Errors in %s' % ErrMsgTriArray[0]
subj=subj.replace('<br>','')
subj=subj.replace('\n','')
subj=subj.replace('\r',' ')

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = subj
msgRoot['From'] = EMAIL_FROM
msgRoot['To'] = EMAIL_TO
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)
msgAlternative.attach(plaintext)
msgAlternative.attach(htmltext)

# Get image - assumes its in current directory
fp = open('TopImage.gif', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)

#attach a pdf
fp = open('C:/Users/AMM/Documents/AMM Development/Sales Info/Best-of Web Documents for existing accounts - Year 2011/Executive Summary for Current WMS Customers 2011.pdf', 'rb')
img = MIMEApplication(fp.read(),'pdf')
fp.close()
img.add_header('Content-Disposition', 'attachment', filename='Executive Summary for Current WMS Customers 2011.pdf')
msgRoot.attach(img)
msgRoot.
#send it!
x=smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
x.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
#"zee@inetnebr.com"
x.sendmail(EMAIL_FROM,EMAIL_TO,msgRoot.as_string())
