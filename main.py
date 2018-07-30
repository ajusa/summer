import re, os, urllib.request, urllib.parse 
from weather import Weather, Unit
from win10toast import ToastNotifier
from threading import Timer

with open('stopwords.txt') as f: stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]
devices = ["laptop", "roku", "dad's laptop", "tv"]

def volume_module(msg, check, rest):
	def translate(value):
	    leftSpan = 100
	    rightSpan = 65535
	    valueScaled = float(value - 0) / float(leftSpan)
	    return 0 + (valueScaled * rightSpan)
	if "volume" in msg.lower() and re.findall(r'[0-9]+', msg) and re.findall(r'[0-9]+', msg)[0]:
		if check: return {"out": "action", "inp": "text"}
		os.system("nircmd.exe setsysvolume " + str(translate(int(re.findall(r'[0-9]+', msg)[0]))))
		print('Changed Volume to ' + re.findall(r'[0-9]+', msg)[0])
	else: return False

def time_module(msg, check, rest):
	if "second" in msg.lower() and re.findall(r'[0-9]+', msg) and re.findall(r'[0-9]+', msg)[0]:
		if check: return {"out": None, "inp": "text"}
		t = Timer(int(re.search(r'\d+', msg).group()), lambda: execute(rest))
		t.start()
	else: return False

def weather_module(msg, check, rest):
	if "weather" in msg.lower().split(" "):
		if check: return {"out": "text", "inp": None}
		weather = Weather(unit=Unit.FAHRENHEIT)
		temp = weather.lookup(2436453).condition.temp
		execute("It is "+temp+" degrees"+rest)
	else: return False

def notify_module(msg, check, rest):
	if "notification" in msg.lower().split(" "):
		if check: return {"out": None, "inp": "text"}
		toaster = ToastNotifier()
		toaster.show_toast("Summer", msg.replace("notification", ""))
	else: return False

def youtube_module(msg, check, rest):
	if "youtube" in msg.lower() and not re.findall(r'(https?://[^\s]+)', msg):
		if check: return {"out": "text", "inp": "text"}
		query_string = urllib.parse.urlencode({"search_query" : msg})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		url = "http://www.youtube.com/watch?v=" + search_results[0]
		execute(url + rest)
	else: return False

def play_module(msg, check, rest):
	if "play" in msg.lower().split(" ") and re.findall(r'(https?://[^\s]+)', msg):
		if check: return {"out": None, "inp": "text"}
		url =  re.findall(r'(https?://[^\s]+)', msg)[0]
		os.system('explorer "' + url + '"')
		execute(rest)
	else: return False

def cleanSentence(msg): 
	#msg = msg.lower()
	return msg
	#return ' '.join([word for word in msg.split(" ") if word not in stopwords])

modules = [volume_module, time_module, weather_module, notify_module,play_module, youtube_module]
def execute(msg):
	clean = cleanSentence(msg).split(" ")
	parsed = []
	j = 0
	for i in range(len(clean) + 1):
		for module in modules:
			test = module(" ".join(clean[j:i]), True, " ".join(clean[i:]))
			if test:
				parsed.append({"func": module, "module": test, "msg": " ".join(clean[j:i]), "rest": " ".join(clean).replace(" ".join(clean[j:i]), "")})
				j = i
	print(parsed)
	if(len(parsed) > 0):
		parsed[0]["func"](parsed[0]["msg"], False, parsed[0]["rest"])

def possible(arr):
	if len(arr) == 1 or len(arr) == 0: return True
	for i in range(len(arr) - 1):
		if arr[i]["out"] != arr[i+1]["inp"]: return False
	return True
#print(possible([{"out": "action", "inp": "text"}, {"out": None, "inp": "text"}])) #set volume to 50 in 5 minutes
phrase = "change my laptop volume to the current weather in 10 minutes"
phrase = "set volume to 0 in 1 minute"
phrase = "play youtube take on me in 5 seconds and change volume to 5"
phrase = "play youtube never gonna give you up and change volume to 0"
phrases = phrase.split("and")
for i, text in enumerate(phrases):
	execute(" ".join(text.split(" ")[::-1]))

