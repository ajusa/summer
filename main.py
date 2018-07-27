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
		if check: return {"out": "action", "inp": "action"}
		print('Will run action in ' + re.search(r'\d+', msg).group())
		execute(rest)
	else: return False

def cleanSentence(msg): 
	msg = msg.lower()
	return ' '.join([word for word in msg.split(" ") if word not in stopwords])

modules = [volume_module, time_module]
def execute(msg):
	clean = cleanSentence(msg).split(" ")
	for i in range(len(clean)):
		for module in modules:
			if module(" ".join(clean[:i]), True, " ".join(clean[i:])):
				module(" ".join(clean[:i]), False, " ".join(clean[i:]))
			

phrase = "change volume to 50 percent on my laptop in 10 minutes"
execute(phrase)
