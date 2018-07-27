import re
with open('stopwords.txt') as f: stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]
devices = ["laptop", "roku", "dad's laptop", "tv"]
def volume_module(msg, check, rest):
	if "volume" in msg and re.findall(r'[0-9]+', msg) and int(re.findall(r'[0-9]+', msg)[0]) and any(device in msg+rest for device in devices):
		if check: return {"out": "action", "inp": "text"}
		print('Changed Volume to ' + re.findall(r'[0-9]+', msg)[0])
	else: return False

def time_module(msg, check, rest):
	if "minute" in msg and int(re.search(r'\d+', msg).group()):
		if check: return {"out": None, "inp": None}
		print('Will run action in ' + re.search(r'\d+', msg).group())
		execute(rest)
	else: return False

def weather_module(msg, check, rest):
	if "weather" in msg:
		if check: return {"out": "text", "inp": None}
		print('Weather ran')
		execute("60"+rest)
	else: return False


def cleanSentence(msg): 
	msg = msg.lower()
	return ' '.join([word for word in msg.split(" ") if word not in stopwords])

modules = [volume_module, time_module, weather_module]
def execute(msg):
	clean = cleanSentence(msg).split(" ")
	j = 0
	for i in range(len(clean) + 1):
		for module in modules:
			if module(" ".join(clean[j:i]), True, " ".join(clean[i:])):
				module(" ".join(clean[j:i]), False, " ".join(clean[i:]))
				j = i
				return
			

phrase = "in 10 minutes change my laptop volume to the current weather"
execute(phrase)
