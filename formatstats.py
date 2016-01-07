#
# format stats line into csv tuples and save 
# example stats line: Scott Pendlebury goal,2m 4s,1.0.6 - 0.0.0,,
# example csv tuples: Scott Pendlebury,6,124,None,0,Collingwood,Fremantle,1,1
# columns=['player1','score1', 'time', 'player2', 'score2','team1','team2','round', 'game']
#


import re,os,math


def splitplay(action):
    score = {'behind':1, 'goal':6}
    for act in score:
        #print act, score[act]
        if(act in action):
            ai = action.index(act)
            return [action[0:ai-1], score[act]]
    return [None, 0]

def timeinsec(timetxt):
    timearr = map(int, re.findall(r'\d+', timetxt))
    return timearr[0] * 60 + timearr[1]
    

def format_stats(year):
    filename = "allstats_"+year+".txt"
    exfinals_filename = "allstats_ex_finals_"+year+".csv"
    finals_filename = "allstats_finals_"+year+".csv"

    print filename, exfinals_filename, finals_filename

    exfinals_file = open(exfinals_filename, "w")
    finals_file = open(finals_filename, "w")

    gameround=''
    team1=''
    team2=''
    score1=''
    score2=''

    gameid = 0
    timestart = 0
    timeend = 0
    with open(filename, "r") as ins:
        for line in ins:
            line = line.rstrip('\n')
            if line==',':
                continue

            items = line.split(',')


            if (items[0].isdigit()) or ('Finals' in line):
                timestart = timeend = 0

                if(gameround != items[0]):
                    gameround = items[0]
                    gameid = 1
                else:
                    gameid += 1

                team1 = items[1]
                team2 = items[2]
                score1 = items[3]
                score2 = items[4]
                continue

            if 'quarter' in line:
                timestart = timeend
                sec = timeinsec(line)
                timeend = timestart + sec
                continue

            newitems = []
            team1action = items[0]
            if team1action == '':
                newitems.extend([None, 0])
            else:
                newitems.extend(splitplay(team1action))

            team1time = items[1]
            if team1time != '':
                newitems.append(timeinsec(team1time) + timestart)

            team2time = items[3]
            if team2time != '':
                newitems.append(timeinsec(team2time) + timestart)

            team2action = items[4]
            if team2action == '':
                newitems.extend([None, 0])
            else:
                newitems.extend(splitplay(team2action))        

            newitems.extend([team1, team2, gameround, gameid])#, str(timestart)])

            newline = ','.join(str(item) for item in newitems) + '\n'
            if gameround == 'Finals':
                finals_file.write(newline)
            else:
                exfinals_file.write(newline)

    finals_file.close()
    exfinals_file.close()


if __name__ == '__main__':
    import sys
    format_stats(sys.argv[1])
