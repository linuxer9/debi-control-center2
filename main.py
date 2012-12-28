# -*- coding: utf-8 -*-
import gtk
import webkit
import os
from ConfigParser import SafeConfigParser
from locale import getdefaultlocale
import gettext
if not os.path.isdir("./locale/"):
	gettext.bindtextdomain('dcc', '/usr/share/locale/')
else:
	gettext.bindtextdomain('dcc', './locale/')
gettext.textdomain('dcc')
_ = gettext.gettext

app_dir=os.getcwd()
def execute(command):
  	'''this execute shell command and return output
	execute() هذه الدالة لتنفيذ أمر بالطرفية واخراج الناتج'''
	p = os.popen(command)
	return p.readline()
	p.close

def functions(widget, nom,ida):
	'''This function is to receive functions from webkit
	functions(widget, nom,ida) لاستقبال الأوامر والدوال من المتصفح'''
	if ida=="about":
		'''launch About dialog
		ida==about فتح صندوق حوار عن البرنامج'''
		about = gtk.AboutDialog()
        	about.set_program_name("debi control center")
        	about.set_version("0.1")
        	about.set_copyright("Mohamed Mohsen")
        	about.set_comments(_("debi GNU/Linux control center"))
        	about.set_website("http://debi.sf.net")
        	about.run()
        	about.destroy()
	if "pro_" in ida:
		#TODO: التحقق من أن البرنامج يعمل \موجود وإظهار رسالة خطأ عند عدم تنفيذه.
		execute(ida.split('pro_')[1])

def get_info(info):
	'''this function is to get computer information
	get_info() هذه الدالة لجلب معلومات الجهاز '''
	if info=="os": return open('/etc/issue', 'r').read().split('\\n')[0]
	if info=="arc": return os.uname()[4]
	if info=="host": return os.uname()[1]	
	if info=="kernel": return os.uname()[0] +' '+ os.uname()[2]
	if info=="processor": return execute("cat /proc/cpuinfo | grep 'model name'").split(':')[1]
	if info=="mem": return execute("free -m|awk '/^Mem:/{print $2}'") + 'MB'
	if info=="gfx": return execute("lspci |grep VGA").split('controller:')[1].split('(rev')[0]
	if info=="audio": return execute("lspci |grep Audio").split('device:')[1].split('(rev')[0]
	if info=="eth": return execute("lspci |grep Ethernet").split('controller:')[1].split('(rev')[0]
	if info=="desk": return execute("echo $XDG_CURRENT_DESKTOP")

def get_modules(section):
	'''this function is to get all modules in the dir "section" 
	get_modules() هذه الدالة لجلب الإضافات من الدليل المحدد وإخراج ناتج عند عدم وجود إضافات
	'''
	mod_dir=os.listdir("%s/modules/%s/" %(app_dir, section))
	if mod_dir==[]:
		return "<p>" + _("no modules found!") + "</p>"
	else:
		parser = SafeConfigParser()
		pro=""
		for i in mod_dir :
			parser.read("%s/modules/%s/%s" %(app_dir, section, i))
			'''Know if the icon exists
			ico معرفة إذا كانت الأيقونة موجودة بالمتغير '''
			ico =parser.get('module', 'ico')
			if os.path.exists("%s/frontend/icons/modules/" %(app_dir) + ico):
				ico="file://%s/frontend/icons/modules/" %(app_dir) + ico
			else:
				ico="file://%s/frontend/icons/modules/notfound.png"
			pro+='''<div id="launcher" onclick="changeTitle('pro_%s')">
			<img src="%s" />
			<h3>%s</h3>
			<span>%s</span>
			</div>''' % ( parser.get('module', 'command'),
			ico, 
			parser.get('module', 'name'), 
			parser.get('module', 'desc') )
		return pro
		
def frontend_fill():
	'''This function is to build all the html document viewed
	frontend_fill() هذه الدالة لبناء ملف الواجهة html '''
	
	html=open(app_dir + '/frontend/default.html', 'r')
	html=html.read()
	if 'ar_' in getdefaultlocale()[0]:
		html=html.replace("{css}", "ar")
	else:
		html=html.replace("{css}", "all")
	html=html.replace("{string_1}", _("System information"))
	html=html.replace("{string_2}", _("This is a quick overview of your system.."))
	html=html.replace("{string_3}", _("Computer"))
	html=html.replace("{string_4}", _("Operating system: "))
	html=html.replace("{string_5}", _("Processor: "))
	html=html.replace("{string_6}", _("Archticture: "))
	html=html.replace("{string_7}", _("Ram: "))
	html=html.replace("{string_8}", _("Devices"))
	html=html.replace("{string_9}", _("Graphics card: "))
	html=html.replace("{string_10}", _("Audio adapter: "))
	html=html.replace("{string_11}", _("Ethernet: "))
	html=html.replace("{string_12}", _("Misc"))
	html=html.replace("{string_13}", _("Host name: "))
	html=html.replace("{string_14}", _("Kernel: "))
	html=html.replace("{string_15}", _("Desktop: "))
	html=html.replace("{string_16}", _("Software & Packages"))
	html=html.replace("{string_17}", _("Working with software, packages and sources.."))
	html=html.replace("{string_18}", _("Desktop"))
	html=html.replace("{string_19}", _("Manage your desktop environment!"))
	html=html.replace("{string_20}", _("System"))
	html=html.replace("{string_21}", _("This is a set of useful tools for your system.."))
	html=html.replace("{string_22}", _("Hardware"))
	html=html.replace("{string_23}", _("here you can use Hardware tools, install drivers..etc"))
	html=html.replace("{string_24}", _("Other tools"))
	html=html.replace("{string_25}", _("all other tools that aren't related to any of these categories.."))
	#system information معلومات الجهاز
	for i in ['os', 'arc', 'processor', 'mem', 'gfx', 'audio', 'eth', 'kernel', 'host', 'desk'] :
		html=html.replace("{%s}" %(i), get_info(i))
	#categories أقسام الإضافات
	for i in ['packs', 'system', 'desktop', 'hardware', 'other'] :
		html=html.replace("{%s_list}" %(i), get_modules(i))

	return html
	
def main():	
	#TODO: تنظيم أفضل لهذه الأوامر
	window = gtk.Window()
	window.connect('destroy', gtk.main_quit)
	window.set_title(_("debi control center"))
	window.set_size_request(774, 540)
	window.set_resizable(False)
	window.set_position(gtk.WIN_POS_CENTER)
	browser = webkit.WebView()
	browser.connect("title-changed", functions)
	browser.load_html_string(frontend_fill(), 'file://%s/frontend/' %(app_dir))
	#no right click menu
	settings = browser.get_settings()
	settings.set_property('enable-default-context-menu', False)
	browser.set_settings(settings) 
	swindow = gtk.ScrolledWindow()
	window.add(swindow)
	swindow.add(browser)
	window.show_all()
	
main()
gtk.main()

