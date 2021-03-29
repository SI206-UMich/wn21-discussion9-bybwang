from bs4 import BeautifulSoup
import re
import requests
import unittest

# Task 1: Get the URL that links to the Pokemon Charmander's webpage.
# HINT: You will have to add https://pokemondb.net to the URL retrieved using BeautifulSoup
def getCharmanderLink(soup):
    tags = soup.find_all('div', class_='infocard')
    link = ''
    for tag in tags:
        info = tag.find('a', class_='ent-name')
        if info.text == 'Charmander':
            link = info.get('href')
            break

    link = "https://pokemondb.net" + link
    return link

# Task 2: Get the details from the box below "Egg moves". Get all the move names and store
#         them into a list. The function should return that list of moves.
def getEggMoves(pokemon):
    url = 'https://pokemondb.net/pokedex/'+pokemon
    #add code here
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    moves = []
    tag = soup.find('div', class_='grid-col span-lg-6')
    h3 = tag.find_all('h3')
    num = 0
    for i in h3:
        if i.text == 'Egg moves':
            break
        num += 1
    resp_scroll = tag.find_all('div', class_='resp-scroll')
    
    tbody = resp_scroll[num].find('tbody')
    tr = tbody.find_all('tr')
    for i in tr:
        td = i.find('td')
        move = td.find('a').text
        moves.append(move)

    '''    
    move_list = tags[1].find('tr')
    for move in move_list:
        x = move.find('a', class_='ent-name').text
        moves.append(x)'''

    return moves
    
    


# Task 3: Create a regex expression that will find all the times that have these formats: @2pm @5 pm @10am
# Return a list of these times without the '@' symbol. E.g. ['2pm', '5 pm', '10am']
def findLetters(sentences):
    # initialize an empty list
    l = []
    # define the regular expression
    exp = '@(\d{1,2}\s?[ap]m)'

    # loop through each sentence or phrase in sentences
    for line in sentences:

    # find all the words that match the regular expression in each sentence
        x = re.findall(exp, line)

    # loop through the found words and add the words to your empty list
        for word in x:
            l.append(word)

    #return the list of the last letter of all words that begin or end with a capital letter
    return l


def main():
    url = 'https://pokemondb.net/pokedex/national'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    getCharmanderLink(soup)
    getEggMoves('scizor')

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(requests.get('https://pokemondb.net/pokedex/national').text, 'html.parser')

    def test_link_Charmander(self):
        self.assertEqual(getCharmanderLink(self.soup), 'https://pokemondb.net/pokedex/charmander')

    def test_egg_moves(self):
        self.assertEqual(getEggMoves('scizor'), ['Counter', 'Defog', 'Feint', 'Night Slash', 'Quick Guard'])

    def test_findLetters(self):
        self.assertEqual(findLetters(['Come eat lunch at 12','there"s a party @2pm', 'practice @7am','nothing']), ['2pm', '7am'])
        self.assertEqual(findLetters(['There is show @12pm if you want to join','I will be there @ 2pm', 'come at @3 pm will be better']), ['12pm', '3 pm'])

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)