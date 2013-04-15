import requests
import re

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('mailchimp-template.html')


def getInfoFromGithub(githubURL):
	"""
	Loads a github URL to extract follower count and location
	  Returns tuple of (followers, location)
	  or (followers, False) if location is not given on profile pag
	"""
	r = requests.get(githubURL)
	followerSection = r.text[r.text.find('/followers">') + len('/followers">') : r.text.find("<span>follower")]

	locationSection = r.text[r.text.find('<dd itemprop="homeLocation">') + len('<dd itemprop="homeLocation">') : r.text.find('<dd itemprop="homeLocation">') + len('<dd itemprop="homeLocation">') + 30]

	followers = int(re.sub("\D", "", followerSection))
	location = locationSection[0: locationSection.find("</dd>")]
	if location == 'ead prefix="og: http://ogp.me':
		location = False 
	return followers, location

def getStarsForks(githubURL):
	"""
	Loads a github URL to extract stars and forks
	  Returns a tuplet of (stars, forks)
	"""
	r = requests.get(githubURL)
	starFinder = '<a class="social-count js-social-count"'
	starSection = r.text[r.text.find(starFinder) + len(starFinder) : r.text.find(starFinder) + len(starFinder) + 75]

	forkFinder = 'class="social-count">'
	forkSection = r.text[r.text.find(forkFinder) + len(forkFinder) : r.text.find(forkFinder) + len(forkFinder) + 24]

	stars = int(re.sub("\D", "", starSection))
	forks = int(re.sub("\D", "", forkSection))

	return stars, forks

def getUpvotes(hnURL):
	"""
	Gets upvotes on HN from a thread URL
	  return int of num upvotes
	"""
	r = requests.get(hnURL)
	upvoteFinder = '<span id=score_'
	upvoteSection = r.text[r.text.find(upvoteFinder) + len(upvoteFinder) + 8 : r.text.find(upvoteFinder) + len(upvoteFinder) + 16]

	return int(re.sub("\D", "", upvoteSection))

class Person(object):
	def __init__(self, name, bio):
		self.name = name
		self.bio = bio

	def addGithub(self, githubURL):
		self.github = githubURL
		followers, location = getInfoFromGithub(githubURL)
		self.followers = followers
		if not location:
			return False
		self.location = location
		return True

	def addLocation(self, location):
		self.location = location

	def addEmail(self, email):
		if email != "":
			self.email = email
		else:
			self.email = False

	def addTwitter(self, twitter):
		if twitter != "":
			self.twitter = twitter
		else:
			self.twitter = False

	def addWebsite(self, website):
		if website != "":
			self.website = website
		else:
			self.website = False

class Project(object):
	def __init__(self, title, summary, hn, github, technology):
		self.title = title
		self.hn = hn
		self.summary = summary
		self.upvotes = getUpvotes(hn)
		self.github = github
		self.stars, self.forks = getStarsForks(github)
		self.score = self.calcScore()
		self.technology = technology

		self.contributors = []

	def addContributor(self, person):
		self.contributors.append(person)

	def calcScore(self):
		return 0.4*self.stars + 0.2*self.forks + 0.4*self.upvotes

def weekendUpdateBuilder():
	projects = []
	print "\nWelcome to weekendUpdateBuilder! Here are some instructions: \
		\n 1) Answer the questions that are asked of you \
		\n 2) If you don't have an answer to a question, just press enter \
		\n 3) There is no 3. \n\n"
	for i in range(1):
		title = raw_input("What is the name of the %sth project?  " % (i+1))
		summary = raw_input("Give a brief and funny description  ")
		hn = raw_input("URL of HN post?  ")
		github = raw_input("URL of GitHub for the project?  ")
		tech = raw_input("Main technology/ies) used in project:  ")

		current = Project(title, summary, hn, github, tech)

		numPeople = int(raw_input("How many people worked on this project?  "))
		for i in range(numPeople):
			print "\n"
			name = raw_input("Person's name?  ")
			bio = raw_input("Short and funny bio for person:  ")
			person = Person(name, bio)
			github = raw_input("What is this person's github URL?  ")
			if not person.addGithub(github):
				location = raw_input("Where do they live? (stalker!)  ")
				person.addLocation(location)
			person.addEmail(raw_input("What's their email?  "))
			person.addTwitter(raw_input("What's their twitter?  "))
			person.addWebsite(raw_input("What's their personal website?  "))

			current.contributors.append(person)

		projects.append(current)	
		print "-----------------------------------"
		print "\n \n"
	return projects

def main():
	a = weekendUpdateBuilder()
	num = raw_input("Last question: what project number is this?  ")
	print "here's your template! \n \n"
	print template.render(project=a[0], number=num)

def test():
	while True:
		url = raw_input("Gimme GitHub URL  ")
		s, f = getStarsForks(url)
		print 'stars', s
		print 'forks', f
		moar = raw_input("Moar? (y/n)  ")
		if moar == "n":
			break

main()
#test()






