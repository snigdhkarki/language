import csv
v1list = []
v2list = []
pluralnounlist = []
adjectivelist = []

with open('verbs.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        v1list.append(row['v1'])
        v2list.append(row['v2'])       
    v1list = sorted(v1list)
    v2list = sorted(v2list)

with open('pluralnoun.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        pluralnounlist.append(row['pluralnoun'])
    pluralnounlist = sorted(pluralnounlist)

with open('adjective.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        adjectivelist.append(row['adjective'])
    adjectivelist = sorted(adjectivelist)       

def binary_search(word_list, word):
    #Input: wordlist, word      #any list of word and any word
    #Output: True if word present in wordlist else false
    
    left, right = 0, len(word_list) - 1
    
    while left <= right:        
        mid = (left + right) // 2
        mid_val = word_list[mid]        
       
        if mid_val == word:
            return True    
        elif mid_val > word:
            right = mid - 1    
        else:
            left = mid + 1            
    
    return False

def checkifverb(word):
    #Input: word    #any word
    #Output: true if word is singular(v1) or plural(v2) verb else false  

    if binary_search(v1list, word):
        singular = True
    else:
        singular = False

    if binary_search(v2list, word):
        plural = True
    else:
        plural = False
    
    verb = singular or plural
    return verb

def sentence_to_words(sentence):
    #Input: sentence    #any sentence without fullstop
    #Output: list of word that make the sentence
    words = sentence.split()
    return words

def sentencetoobject(sentence):
    #Input: sentence    #any sentence
    #Output: object with properties subject, verb and object
    wordlist = sentence_to_words(sentence)
    truth = {}
    firsthalf = True
    truth['subject'] = ''
    truth['object'] = ''
    for word in wordlist:    
        if checkifverb(word):
            truth['verb'] = word
            firsthalf = False
            continue
        
        if firsthalf:
            truth['subject'] = truth['subject'] + ' ' + word
        else:
            truth['object'] = truth['object'] + ' ' + word
    truth['subject'] = truth['subject'].strip()
    truth['object'] = truth['object'].strip()
    return truth

def objectrefiner(truth):
    #Input: obj     #An object that describes a sentence
    #Output: an object that has info who,what for subject and how,what,whom,where,when for object

    what = False
    for word in sentence_to_words(truth['subject']):
        if word == 'A' or word == 'An' or word == 'The':
            what = True    
    if binary_search(pluralnounlist, truth['subject']):
        what = True
    if what:
        truth['subject'] = {'what': truth['subject']}
    else:
        truth['subject'] = {'who': truth['subject']}

    how = False
    whom= False
    when = False
    where = False
    whenorwhere = False
    if binary_search(adjectivelist, truth['object']):
        how = True
    objectpronoun = ['me', 'you', 'him', 'her', 'us', 'them', 'whom']
    if truth['object'].istitle() or truth['object'] in objectpronoun:
        whom = True
    for word in sentence_to_words(truth['object']):
        if word == 'at' or word == 'in' or word == 'on':
            whenorwhere = True
    partofday = ['morning', 'evening', 'noon']
    year = []
    for i in range(10001):
        year.append(str(i))
    season = ["spring", "summer", "fall", "winter"]
    month = ["January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"]
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    if whenorwhere:
        for word in sentence_to_words(truth['object']):        
            if word == 'time' or word == 'oclock' or word == 'am' or word == 'pm' or word in partofday or word in year or word in season or word in month or word in day:
                when = True
            else:
                where = True
    if how:
        truth['object'] = {'how': truth['object']}
    elif whom:
        truth['object'] = {'whom': truth['object']}
    elif when:
        truth['object'] = {'when': truth['object']}
    elif where:
        truth['object'] = {'where': truth['object']}
    else:
        truth['object'] = {'what': truth['object']}

    return truth

def answer(data, question):
    #Input: data,question        #sentence that can be processed and question that is to be asked on the processed sentence
    #Output: answer to the question according to data
    truth = sentencetoobject(sentence)
    truth = objectrefiner(truth)
    print(truth)
    questionwordlist = sentence_to_words(question)
    questionobject = sentencetoobject(question)

    if questionwordlist[0] == 'Who':    
        if truth['verb'] == questionobject['verb'] or truth['verb'] == questionobject['verb'] + 's' or truth['verb']+'s' == questionobject['verb'] or (truth['verb']=='is' and questionobject['verb']=='are') or (truth['verb']=='are' and questionobject['verb']=='is'):
            if questionobject['object'] in truth['object'].values():
                if 'who' in truth['subject'].keys():
                    return truth['subject']['who']

    if questionwordlist[0] == 'What':        
        questionwordlist.remove('What')
        question = ' '.join(questionwordlist)
        questionobject = sentencetoobject(question)  
        
        if 'does' in questionwordlist:
            if 'does' in questionwordlist:        
                questionwordlist.remove('does')
            question = ' '.join(questionwordlist)
            questionobject = sentencetoobject(question)               
            if truth['verb'] == questionobject['verb'] or truth['verb'] == questionobject['verb'] + 's' or truth['verb']+'s' == questionobject['verb'] or (truth['verb']=='is' and questionobject['verb']=='are') or (truth['verb']=='are' and questionobject['verb']=='is')  :
                if questionobject['subject'].capitalize() in truth['subject'].values(): 
                    if 'what' in truth['object'].keys():
                        return truth['object']['what']
        
        if 'is' in questionwordlist:
            if truth['verb'] == questionobject['verb'] or truth['verb'] == questionobject['verb'] + 's' or truth['verb']+'s' == questionobject['verb'] or (truth['verb']=='is' and questionobject['verb']=='are') or (truth['verb']=='are' and questionobject['verb']=='is') :
                if questionobject['object'].capitalize() in truth['subject'].values(): 
                    if 'what' in truth['object'].keys():
                        return truth['object']['what']
        
        
        if truth['verb'] == questionobject['verb'] or truth['verb'] == questionobject['verb'] + 's' or truth['verb']+'s' == questionobject['verb'] or (truth['verb']=='is' and questionobject['verb']=='are') or (truth['verb']=='are' and questionobject['verb']=='is'):
            if questionobject['object'] in truth['object'].values():
                if 'what' in truth['subject'].keys():
                    return truth['subject']['what']

        print(questionobject)

    if questionwordlist[0] == 'How':
        questionwordlist.remove('How')
        question = ' '.join(questionwordlist)
        questionobject = sentencetoobject(question)
        print(questionobject)
        if truth['verb'] == questionobject['verb'] or truth['verb'] == questionobject['verb'] + 's' or truth['verb']+'s' == questionobject['verb'] or (truth['verb']=='is' and questionobject['verb']=='are') or (truth['verb']=='are' and questionobject['verb']=='is'):
            if questionobject['object'].capitalize() in truth['subject'].values():  
                if 'how' in truth['object'].keys(): 
                    return truth['object']['how']

    if questionwordlist[0] == 'Whom':
        questionwordlist.remove('Whom')
        if 'being' in questionwordlist:
            questionwordlist.remove('being')
        if 'does' in questionwordlist:
            questionwordlist.remove('does')
        if 'do' in questionwordlist:
            questionwordlist.remove('do') 
        question = ' '.join(questionwordlist)
        questionobject = sentencetoobject(question)
        print(questionobject)       
        if truth['verb'] == questionobject['verb'] or truth['verb'] == questionobject['verb'] + 's' or truth['verb']+'s' == questionobject['verb'] or (truth['verb']=='is' and questionobject['verb']=='are') or (truth['verb']=='are' and questionobject['verb']=='is'):
            if questionobject['object'].capitalize() in truth['subject'].values() or questionobject['subject'].capitalize() in truth['subject'].values():
                if 'whom' in truth['object'].keys(): 
                    return truth['object']['whom']

    if questionwordlist[0] == 'When':
        questionwordlist.remove('When')
        if 'being' in questionwordlist:
            questionwordlist.remove('being')
        if 'does' in questionwordlist:
            questionwordlist.remove('does')
        if 'do' in questionwordlist:
            questionwordlist.remove('do') 
        question = ' '.join(questionwordlist)
        questionobject = sentencetoobject(question)
        print(questionobject) 
        if truth['verb'] == questionobject['verb'] or truth['verb'] == questionobject['verb'] + 's' or truth['verb']+'s' == questionobject['verb'] or (truth['verb']=='is' and questionobject['verb']=='are') or (truth['verb']=='are' and questionobject['verb']=='is'):
            if questionobject['object'].capitalize() in truth['subject'].values() or questionobject['subject'].capitalize() in truth['subject'].values():
                if 'when' in truth['object'].keys():
                    return truth['object']['when']

    if questionwordlist[0] == 'Where':
        questionwordlist.remove('Where')
    if 'being' in questionwordlist:
        questionwordlist.remove('being')
    if 'does' in questionwordlist:
        questionwordlist.remove('does')
    if 'do' in questionwordlist:
        questionwordlist.remove('do') 
    question = ' '.join(questionwordlist)
    questionobject = sentencetoobject(question)
    print(questionobject) 
    if truth['verb'] == questionobject['verb'] or truth['verb'] == questionobject['verb'] + 's' or truth['verb']+'s' == questionobject['verb'] or (truth['verb']=='is' and questionobject['verb']=='are') or (truth['verb']=='are' and questionobject['verb']=='is'):
        if questionobject['object'].capitalize() in truth['subject'].values() or questionobject['subject'].capitalize() in truth['subject'].values():
            if 'where' in truth['object'].keys():
                return truth['object']['where']

sentence = 'I eat in Dolpa'
question = 'Where do I eat'
ans = answer(sentence, question)
print(ans)











                   




                        














        