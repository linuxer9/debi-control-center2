# -*- coding: utf-8 -*-
import gtk
import webkit
import os
from ConfigParser import SafeConfigParser
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
	if ida=="non":
		widget.win.move(0, 0)
	if ida=="about":
		'''launch About dialog
		ida==about فتح صندوق حوار عن البرنامج'''
		about = gtk.AboutDialog()
        	about.set_program_name("debi control center")
        	about.set_version("0.1")
        	about.set_copyright("Mohamed Mohsen")
        	about.set_comments("debi GNU/Linux control center")
        	about.set_website("http://debi.sf.net")
        	about.run()
        	about.destroy()
	if "pro_" in ida:
		#TODO: التحقق من أن البرنامج يعمل \موجود وإظهار رسالة خطأ عند عدم تنفيذه.
		execute(ida.split('pro_')[1])

def get_info(info):
	'''this function is to get computer information
	get_info() هذه الدالة لجلب معلومات الجهاز '''
	if info=="operatingsystem": return open('/etc/issue', 'r').read().split('\\n')[0]
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
		return "<p>no modules found!</p>"
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
	#TODO: تنظيم هذه الدالة وإختصارها XD
	html=open(app_dir + '/frontend/default.html', 'r')
	html=html.read()
	html=html.replace("{os}", get_info("operatingsystem"))
	html=html.replace("{arc}", get_info("arc"))
	html=html.replace("{processor}", get_info("processor"))
	html=html.replace("{mem}", get_info("mem"))
	html=html.replace("{gfx}", get_info("gfx"))
	html=html.replace("{audio}", get_info("audio"))
	html=html.replace("{eth}", get_info("eth"))
	html=html.replace("{kernel}", get_info("kernel"))
	html=html.replace("{host}", get_info("host"))
	html=html.replace("{desk}", get_info("desk"))

	html=html.replace("{packs_list}", get_modules("packs"))
	html=html.replace("{system_list}", get_modules("system"))
	html=html.replace("{desktop_list}", get_modules("desktop"))
	html=html.replace("{hardware_list}", get_modules("hardware"))
	html=html.replace("{other_list}", get_modules("other"))
	return html
	

def main():	
	#TODO: تنظيم أفضل لهذه الأوامر
	window = gtk.Window()
	window.connect('destroy', gtk.main_quit)
	window.set_title("debi control center")
	window.set_size_request(774, 540)
	window.set_resizable(False)
	window.set_position(gtk.WIN_POS_CENTER)
	browser = webkit.WebView()
	browser.connect("title-changed", functions)
	browser.load_html_string(frontend_fill(), 'file://%s/frontend/' %(app_dir))
	swindow = gtk.ScrolledWindow()
	window.add(swindow)
	swindow.add(browser)
	window.show_all()
	
main()
gtk.main()

