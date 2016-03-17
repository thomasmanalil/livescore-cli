import requests
from bs4 import BeautifulSoup



def extractTag(tree, tag, cssClass):
	return [t.extract() for t in tree.findAll(tag, class_=cssClass)]



def parseTree(subtree):
	subtree = [t for t in subtree if t!=' ' and t!='']
	for i in range(len(subtree)):
		name = getattr(subtree[i], "name", None)
		if name is not None:
			subtree[i] = parseTree(subtree[i])
	return subtree

#Request html from the site using http get
response = requests.get("http://www.livescore.com/england/premier-league/")

#Parse the response text using html parser and BeautifulSoup library
soup = BeautifulSoup(response.text, 'html.parser')

#Select only the require content subtree from the website
[content] = soup.select('body > div.wrapper > div.content')
#Extract the table part into table variable
#The extracted part is removed from the original content.
#So the content now only contains the score
table = extractTag(content, 'div','ltable')
#Remove the some not required tags
extractTag(content, 'div', 'cal-wrap')
extractTag(content, 'div', 'star')
extractTag(content, 'div', 'row mt4 bb bt')

table = parseTree(table)
print(table)
score = parseTree(content)
print(score)


