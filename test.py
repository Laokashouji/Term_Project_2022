wordlist = ['asdf', 'Wow', "WERWER", "We"]
for word in wordlist.copy():
    if not word.islower():
        wordlist.remove(word)
print(wordlist)
