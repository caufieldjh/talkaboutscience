#!/usr/bin/python
#talkaboutscience.py
'''
Generates things that sound like science,
but in most cases are not.

Planned additions:
Add a simulated Science or PLOS headline like on the PDFs
I made a mockup (see graphics folder)
 - it should include a graphical header, the title,
and some randomly generated authors and institutions.
Should just build it with Wand or something.
  The PLOS logo font is Brandon Grotesque Black.
'''

import random, re, string, sys, time, tweepy, webbrowser

#Contants and Setup

#The Twitter OAuth consumer token and consumer secret go here,
#like auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth = tweepy.OAuthHandler("","")

auth.secure = True

#Methods
def get_words():
	adjs = []
	nouns = []
	with open("sciencewords.txt") as wordfile:
		for line in wordfile:
			splitline = (line.rstrip()).split("\t")
			if splitline[1] == "adj":
				adjs.append(splitline[0])
			elif splitline[1] == "noun":
				nouns.append(splitline[0])
	words = [adjs, nouns]
	return words
	
def get_intros():
	intros = []
	with open("introphrases.txt") as introfile:
		for line in introfile:
			cleanline = (line.rstrip())
			intros.append(cleanline)
	return intros
	
def get_names():
	names = []
	with open("lastnames.txt") as namesfile:
		for line in namesfile:
			cleanline = (line.rstrip())
			names.append(cleanline)
	return names
	
def get_softintros():
	softintros = []
	with open("softintros.txt") as softintrofile:
		for line in softintrofile:
			cleanline = (line.rstrip())
			softintros.append(cleanline)
	return softintros
	
def get_softmods():
	softmods = []
	with open("softmods.txt") as softmodfile:
		for line in softmodfile:
			cleanline = (line.rstrip())
			softmods.append(cleanline)
	return softmods
	
def get_software_name(softmods):
	name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(3,7)))
	if random.randint(0,7) == 0:
		mod_choice = random.randint(0,2)
		if mod_choice == 0:	#Prefix letter
			name = name + random.choice(string.ascii_lowercase)
		elif mod_choice == 1: #Postfix letter
			name = random.choice(string.ascii_lowercase) + name
		elif mod_choice == 2: #Other additions from softmods
			softmod = random.choice(softmods)
			if random.randint(0,4) > 0:
				if random.randint(0,8) == 0:
					softmod = softmod + " "
				name = softmod + name
			else:
				if random.randint(0,8) == 0:
					softmod = " " + softmod
				name = name + softmod
	
	if random.randint(0,6) == 0:
		version_num = random.randint(2,12)
		if random.randint(0,1) == 0:
			name = name + " %s" % version_num
		else:
			name = name + " v%s" % version_num
	
	if random.randint(0,5) == 0:
		name = name.upper()
	return name
	
def title_this(s):
	return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
		lambda mo: mo.group(0)[0].upper() +
			mo.group(0)[1:].lower(), s)

#Main
def main():
	
	mode = raw_input('Operating mode:\n 1 for testing\n 3 for posting.\n')
	mode = int(mode)
	generating = True
	
	
	# For twitter OAuth
	try:
		tweepy_file = open("tw_auth.txt")
		print("Found Twitter auth values.")
		tw_auths = []
		for line in tweepy_file:
			#print(line)
			tw_auths.append(line.rstrip())
		auth.set_access_token(tw_auths[0], tw_auths[1])
		need_auth = False
	except IOError as e:
		print("Could not find Twitter auth values - need to authorize.")
		need_auth = True
	
	if need_auth:
		try:
		    redirect_url = auth.get_authorization_url()
		    webbrowser.open(redirect_url, new =0)
		    verifier = raw_input('Verifier:')
		except tweepy.TweepError:
		    print('Error! Failed to get request token.')
		    
		try:
		    auth.get_access_token(verifier)
		except tweepy.TweepError:
		    print('Error! Failed to get access token.')
		except UnboundLocalError:
			print('You may not have specified the consumer token and secret.')
			print('Please specify them in the code.')
			print('See http://docs.tweepy.org/en/v3.6.0/auth_tutorial.html')
			sys.exit()
		    
		auth.set_access_token(auth.access_token, auth.access_token_secret)
		tweepy_file = open("tw_auth.txt", 'w')
		tweepy_file.write(auth.access_token + "\n")
		tweepy_file.write(auth.access_token_secret + "\n")
		tweepy_file.close()
		
	api = tweepy.API(auth)
	
	if mode == 1: 	#So we're in testing mode.
		print("Testing mode. Won't post.")
	
	words = get_words()
	intros = get_intros()
	names = get_names()
	
	while generating == True:
		linechoice = random.randint(1,10)
		adj1 = random.choice(words[0])
		adj2 = random.choice(words[0])
		if random.randint(0,49) == 0:
		#Use a gene/protein name sometimes
			if random.randint(0,2) == 0:
				#Human/mammal gene - or at least a fun acronym
				noun1 = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
			else:
				#Bacterial gene
				noun1 = ''.join(random.choice(string.ascii_lowercase) for _ in range(3))
				if random.randint(0,1) == 0:
					noun1 = noun1.title()
				noun1 = noun1 + random.choice(string.ascii_uppercase)
		else:
			noun1 = random.choice(words[1])
		
		if adj1 == adj2:
			adj1 = "dual " + adj1
			adj2 = "" 
			
		if linechoice == 1:
			if random.randint(0,1) == 0:
				lineout = "%s %s" % (adj1, noun1)
				phrase = lineout
			else:
				lineout = "%s %s %s" % (adj1, adj2, noun1)
				phrase = lineout
			
		elif linechoice == 2:
			#Questions
			choice = random.randint(0,4)
			if choice == 0:
				lineout = "How is %s %s %s" % (adj1, noun1, adj2)
				phrase = "%s %s" % (adj2, noun1)
			elif choice == 1:
				lineout = "How can we make %s more %s" % (noun1, adj1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 2:
				lineout = "A %s rationale for %s" % (adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 3:
				noun2 = random.choice(words[1])
				lineout = "If %s could be %s, could %s as well?" % (noun1, adj1, noun2)
				phrase = "%s %s" % (adj1, noun2)
			elif choice == 4:
				noun2 = random.choice(words[1])
				lineout = "How can we increase %s within %s?" % (noun1, noun2)
				phrase = "%s" % (noun2)
			
		elif linechoice == 3:
			noun2 = random.choice(words[1])
			conj1 = random.choice(["in","as","for","with","using","from"])
			choice = random.randint(0,2)
			if choice == 0:
				if random.randint(0,1) == 0:
					lineout = "%s %s %s %s" % (adj1, noun1, conj1, noun2)
				else:
					lineout = "%s %s %s %s %s" % (adj1, noun1, conj1, adj2, noun2)
			elif choice == 1:
				if random.randint(0,1) == 0:
					lineout = "%s %s %s" % (noun1, conj1, noun2)
				else:
					lineout = "%s %s %s %s" % (noun1, conj1, adj2, noun2)
			elif choice == 2:
				if random.randint(0,1) == 0:
					lineout = "%s, %s %s %s %s" % (adj1, adj2, noun1, conj1, noun2)
				else:
					adj3 = random.choice(words[0])
					lineout = "%s %s %s %s %s %s" % (adj1, noun1, conj1, adj2, adj3, noun2)
			phrase = lineout
			
		elif linechoice == 4: #Intro phrase
			intro = random.choice(intros)
			lineout = "%s %s %s" % (intro, adj1, noun1)
			phrase = "%s %s" % (adj1, noun1)
			if random.randint(0,2) == 0:
				lineout = lineout.replace(" the "," ")
			if random.randint(0,3) == 0:
				lineout = lineout.replace(" of "," for ")
			if intro[-1:] == "\"":
				lineout = lineout + "\""
			
		elif linechoice == 5: #Posessive, i.e. Darwin's finch
			this_name = random.choice(names).capitalize()
			if random.randint(0,1) == 0:
				lineout = "%s's %s" % (this_name, noun1)
				phrase = "%s %s" % (this_name, noun1)
			else:
				lineout = "%s's %s %s" % (this_name, adj1, noun1)
				phrase = "%s %s %s" % (this_name, adj1, noun1)
			
		elif linechoice == 6: #Informatics
			softmods = get_softmods()
			soft = get_software_name(softmods)
			softintros = get_softintros()
			softintro = random.choice(softintros)
			choice = random.randint(0,5)
			if choice == 0:
				lineout = "%s: %s %s %s" % (soft, softintro, adj1, noun1)
			elif choice == 1:
				lineout = "%s: %s %s %s %s" % (soft, softintro, adj2, adj1, noun1)
			elif choice == 2:
				noun2 = random.choice(words[1])
				lineout = "%s: %s %s %s and %s %s" % (soft, softintro, adj2, noun2, adj1, noun1)
			elif choice == 3:
				lineout = "%s: %s %s %s data" % (soft, softintro, adj1, noun1)
			elif choice == 4:
				noun2 = random.choice(words[1])
				mod1 = random.choice(["with", "caused by", "using", "without"])
				lineout = "%s: %s %s %s %s %s" % (soft, softintro, adj1, noun1, mod1, noun2)
			elif choice == 5:
				lineout = "%s %s %s" % (softintro, adj1, noun1)
			phrase = "%s %s" % (adj1, noun1)
		
		elif linechoice == 7: #More phrases
			noun2 = random.choice(words[1])
			noun3 = random.choice(words[1])
			choice = random.randint(0,13)
			if choice == 0:
				lineout = "%s %s: Using %s %s to study %s" % (adj1, 
												noun1, adj2, 
												noun2, noun3)
				phrase = "%s" % (noun3)
			elif choice == 1:
				lineout = "%s requires %s %s with %s %s" % (noun1, 
												adj1, noun2, 
												adj2, noun3)
				phrase = "%s %s" % (adj2, noun3)
			elif choice == 2:
				lineout = "The \"%s %s\"" % (adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 3:
				lineout = "%s %s: an emerging industry" % (adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 4:
				lineout = "Next generation of %s %s faces daunting hurdles" % (adj1, noun1)
				phrase = "%s %s faces daunting hurdles" % (adj1, noun1)
			elif choice == 5:
				lineout = "%s %s promote development of %s %s" % (adj1, noun1, 
												adj2, noun2)
				phrase = "%s %s" % (adj2, noun2)
			elif choice == 6:
				lineout = "Major %s %s study reignites %s debate" % (adj1, noun1, 
												noun2)
				phrase = "%s debate" % (noun2)
			elif choice == 7:
				lineout = "%s %s just got even weirder (and even more confusing)" % (adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 8:
				lineout = "Does %s %s drive %s" % (adj1, noun1, noun2)
				phrase = "%s" % (noun2)
			elif choice == 9:
				lineout = "How %s %s reveal the future of %s %s" % (adj1, noun1, adj2, noun2)
				phrase = "%s %s" % (adj2, noun2)
			elif choice == 10:
				lineout = "The %s nature of %s" % (adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 11:
				lineout = "This raises questions on how %s can be %s" % (noun1, adj1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 12:
				lineout = "%s is not related to %s" % (noun1, noun2)
				phrase = "%s" % (noun2)
			elif choice == 13:
				lineout = "%s contributes to %s formation" % (noun1, noun2)
				phrase = "%s" % (noun2)
								
		if linechoice == 8:
			#This used to just be Nanopore but that got tiresome
			#So now it's just more nouns
			noun2 = random.choice(words[1])
			if random.randint(0,1) == 0:
				lineout = "It's either %s or %s" % (noun1, noun2)
				phrase = noun1
			else:
				guess = random.choice(["guess","suppose","assume",
							"conclude","reckon","suspect","think",
							"imagine","figure","believe","gather"])
				lineout = "%s %s, I %s" % (adj1, noun1, guess)
				phrase = "%s %s" % (adj1, noun1)
		
		if linechoice == 9:
			#National Science News
			nation = random.choice(["Chinese","Japanese","American","British",
										"German","Italian","Brazilian","Indian",
										"Australian","South African","Canadian",
										"European","Mexican","Korean","Swiss",
										"Russian","Swedish","Spanish"])
			entity = random.choice(["NIH","CDC","WHO","DOE","ARPA-E",
										"DARPA","FDA","HRA","Ministry of Health"])
			noun2 = random.choice(words[1])
			choice = random.randint(0,9)
			if choice == 0:
				lineout = "%s scientists to pioneer first %s %s trial" % (nation, adj1, noun1)
				phrase = "%s %s trial" % (adj1, noun1)
			elif choice == 1:
				lineout = "New %s government makes an about-face on %s %s research" % (nation, adj1, noun1)
				phrase = "%s %s research" % (adj1, noun1)
			elif choice == 2:
				lineout = "%s %s: focus on %s" % (nation, noun1, noun2)
				phrase = "focus on %s" % (noun2)
			elif choice == 3:
				lineout = "%s moves to lift moratorium on %s %s research" % (entity, adj1, noun1)
				phrase = "%s %s research" % (adj1, noun1)
			elif choice == 4:
				lineout = "%s-funded study supports use of %s %s" % (entity, adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 5:
				lineout = "%s scientists shocked by %s %s" % (nation, adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 6:
				lineout = "%s researchers explore how to implement %s %s" % (nation, adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 7:
				lineout = "%s economists contemplate %s %s" % (nation, adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
			elif choice == 8:
				lineout = "Capitalize on %s %s" % (nation, noun1)
				phrase = "%s %s" % (nation, noun1)
			elif choice == 9:
				lineout = "Fears rise after %s report on %s %s" % (nation, adj1, noun1)
				phrase = "%s %s" % (adj1, noun1)
		
		if linechoice == 10:
			#Methods
			choice = random.randint(0,2)
			noun2 = random.choice(words[1])
			if choice == 0:
				lineout = "%s-based method for %s %s" % (noun1, adj1, noun2)
				phrase = "%s %s" % (adj1, noun2)
			elif choice == 1:
				lineout = "An approach to %s using %s %s" % (noun1, adj1, noun2)
				phrase = "%s %s" % (adj1, noun2)
			elif choice == 2:
				lineout = "Methods to study %s using %s %s" % (noun1, adj1, noun2)
				phrase = "%s %s" % (adj1, noun2)
				
		if random.randint(0,6) == 0:
			lineout = title_this(lineout)
			
		if random.randint(0,7) == 0:
			acronym = ""
			for i in title_this(phrase).split():
				if i == "in":
					acronym += "i"
				else:
					acronym += i[0]
			lineout = "%s (%s)" % (lineout, acronym)
			
		if random.randint(0,19) == 0:
			com_choice = random.randint(0,4)
			if com_choice == 0:
				lineout = "Correction: " + lineout
			elif com_choice == 1:
				lineout = "Response to: \"%s\"" % lineout
			elif com_choice == 2:
				lineout = "Comment on: \"%s\"" % lineout
			elif com_choice == 3:
				lineout = "Response to Comment on: \"%s\"" % lineout
			elif com_choice == 4:
				lineout = "Erratum for the Research Article: \"%s\"" % lineout
			
		if random.randint(0,5) == 0:
			if random.randint(0,1) == 0:
				lineout = lineout + "."
			else:
				lineout = lineout + "?"
		
		print(lineout)
	
		if mode == 3:
			try:
				api.update_status(status=lineout)
				print("Posted.")
			except tweepy.TweepError as te:
				#api.update_status(status="Listen to the world around you.") #Throws TweepError usu. if message is >140 char, so just post something else rather than messing around with truncation
				print(te)
				print("Text longer than 140 chars or some other Twitter problem came up. Didn't post.")
		else:
			print("This one wasn't posted.")
			
		if mode == 1:
			generating = False
			wait_time = random.randint(60,1200)	#Wait up to 20 minutes
			minutes, seconds = divmod(wait_time, 60)
			hours, minutes = divmod(minutes, 60)
			print("Would have posted again in %02d minutes, %02d seconds." % (minutes, seconds))
			sys.exit("Exiting...")
		if mode == 3:
			wait_time = random.randint(60,1200)	#Wait up to 20 minutes
			minutes, seconds = divmod(wait_time, 60)
			hours, minutes = divmod(minutes, 60)
			print("Posting again in %02d minutes, %02d seconds." % (minutes, seconds))
			time.sleep(wait_time)

if __name__ == "__main__":
	main()
	
sys.exit(0)
