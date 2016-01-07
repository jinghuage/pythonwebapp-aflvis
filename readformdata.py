#
# mine the stats data from http://afltables.com/afl/seas/
# downloaded from IPython notebook
#
# coding: utf-8

# In[1]:

import urllib2
import re

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# first let's do some test to confirm the yearly link html, 
# and use regular expression to filter out data we want
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

response = urllib2.urlopen('http://afltables.com/afl/seas/season_idx.html')
print response.info()

html = response.read()
#print html


# find href link '2014.html' for <a href='2014.html'>2014</a>
thelink = ''
lines = html.split('\n')
for line in lines:
    #print line
    if '2014</a>' in line:
        print line
        thelink = re.findall(r'"(.*?)"', line)[0]
        break
    
print thelink
response.close()  # best practice to close the file

#Note: you can also use an URL starting with "ftp:", "file:", etc.).


# In[ ]:

import re
s = '<a href="2014.html">2014</a>'

if s.endswith('2014</a>'):
    print re.findall(r'"(.*?)"', s)
    print re.findall(r'"([^"]*)"', s)


# In[114]:

import re
s1 = '<tr><td width=16%><a href="../teams/collingwood_idx.html">Collingwood</a></td><td nowrap width=20% align=center><tt>&nbsp;&nbsp;2.4 &nbsp;&nbsp;2.8 &nbsp;3.13 &nbsp;5.16 </tt></td><td width=5% align=center> 46</td><td>Fri 14-Mar-2014 7:50 PM (6:50 PM) <b>Att:</b>37,571 <b>Venue:</b> <a href="../venues/docklands.html">Docklands</a></td></tr>'
s2 = '<tr><td width=16%><a href="../teams/fremantle_idx.html">Fremantle</a></td><td nowrap width=20% align=center><tt>&nbsp;&nbsp;2.3 &nbsp;&nbsp;8.7 14.10 17.14 </tt></td><td width=5% align=center> 116</td><td><b>Fremantle</b> won by <b>70 pts </b>[<a href="../stats/games/2014/040820140314.html">Match stats</a>]</td></tr>'
if 'Venue' in s1:
    team1 = re.findall(r'">(.*?)<', s1)[-2]
    print team1
    score = re.findall(r'> (\d+)<', s1)[0]
    print score
if 'Match stats' in s2:
    #print line
    team2 = re.findall(r'">(.*?)<', s2)[-2]
    print team2
    statlink = re.findall(r'"(.*?)"', s2)[-1]
    print statlink
    score = re.findall(r'> (\d+)<', s2)[0]
    print score




#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# provide a year, mine stats data for that year
# step 1: find all games and save their stats link
# step 2: for each game, follow their stats link and download progression data 
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# In[21]:

download_year = 2007
thelink = str(download_year) + '.html'

response = urllib2.urlopen("http://afltables.com/afl/seas/"+thelink)
html = response.read()
response.close()


lines = html.split('\n')

from collections import namedtuple

Game = namedtuple('Game', ['Round', 'Team1','Team2', 'Score1','Score2','Statlink'])
allgames = []


rid = 0
for line in lines:
    if 'Round ' in line: 
        #print line
        rid = re.findall(r'Round (\d+)</td>', line)[0]
    elif 'Finals' in line:
        rid = 'Finals'            
    elif 'Venue' in line:
        team1 = re.findall(r'">(.*?)<', line)[-2]
        #print team1
        score1 = re.findall(r'> (\d+)<', line)[0]
    elif 'Match stats' in line:
        team2 = re.findall(r'">(.*?)<', line)[-2]
        #print team2
        statlink = re.findall(r'"(.*?)"', line)[-1]
        #print statlink
        score2 = re.findall(r'> (\d+)<', line)[0]
        allgames.append(Game(rid, team1, team2, score1, score2, statlink))
        




# In[22]:

allgames_txtfile = 'allgames_' + str(download_year) + '.txt'      
allrounds_txtfile = 'allrounds_' + str(download_year) + '.txt' 
f = open(allgames_txtfile,'w')
fr = open(allrounds_txtfile, 'w')

for game in allgames:
    #print game
    eachgame = ','.join(game[0:-1]) + '\n'
    f.write(eachgame)
    if(game[0] != 'Finals'):
        fr.write(eachgame)

f.close()
fr.close()


# In[23]:


allstats_txtfile = 'allstats_' + str(download_year) + '.txt' 
sf = open(allstats_txtfile,'w')


for game in allgames:
    sf.write(','.join(game[0:-1]) + '\n')
    
    response = urllib2.urlopen("http://afltables.com/afl/seas/" + game[-1])
    html = response.read()
    response.close()
    
    
    lines = html.split('\n')

    scoretext = ''
    for line in lines:
        if '1st quarter' in line: 
            l = line.find('1st')
            r = line.find('Game time:')
            #print l, r
            scoretext = line[l:r]
            break
    #scoretext        
    
    progression = scoretext.split('<tr>')
    for p in progression:
        np1 = p.replace('&nbsp;', '')
        np2 = np1.replace('<b>', '')
        np3 = np2.replace('</b>', '')
        np4 = np3.replace('<i>','')
        np5 = np4.replace('</i>','')
        #print np5

        #''.join(c for c in str1 if not c in str2)

        if 'quarter' in np5:
            score = re.findall(r'\((.*?)\)', np5)
            score[0] += ' quarter '
            #print score
        else:
            score = re.findall(r'>(.*?)</td>', np5)

        sf.write(','.join(score) + '\n')


sf.close()


# In[ ]:



