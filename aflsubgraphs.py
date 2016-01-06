from numpy.random import randn
import numpy as np
import pandas as pd

np.set_printoptions(precision=4)

import matplotlib
import matplotlib.pyplot as plt 

import mpld3
from mpld3plugins import FormatTick, RotateTick
from matplotlib.ticker import FuncFormatter

def minsec(x,pos):
    'The two args are the value and tick position'
    return '$%2dm:$%2ds' % (x/60, x%60)

formatter = FuncFormatter(minsec)

def polyfit(order, group):
    team1score = group.score1.cumsum()
    team2score = group.score2.cumsum()
    s1 = team1score.values[-1]
    s2 = team2score.values[-1]
    #print s1-s2
    
    gametimes = group.time
    gameframe = pd.DataFrame({'gametime': gametimes, 'lead':team1score-team2score,'team1score':team1score, 'team2score':team2score})
    
    z = np.polyfit(gametimes.values, (team1score-team2score).values, order)
    #print z

    p = np.poly1d(z)
    #print p(0)
    #print p(7200)
    print '{:.0f}:{:.0f}'.format(p(0), p(7200))
    

def plotfit(axes, df, order):
    ax = sns.regplot(ax=axes, 
                x="gametime", y="lead", data=gameframe,
                order=order, ci=None)
                #label=label + str('--') + str(s1)+':'+str(s2))#+':'+str(p(0))+':'+str(p(7200)))
    
    
    #colors: b: blue g: green r: red c: cyan m: magenta y: yellow k: black w: white
    ax.hlines(0, 0, 7200, color='c', linewidth=2)


def plotgame(axes, team1, team2, title, group):
    team1score = group.score1.cumsum()
    team2score = group.score2.cumsum()
    
    s1 = team1score.values[-1]
    s2 = team2score.values[-1]
    #print s1, s2
    
    gametimes = group.time# + group.qstart
    gameframe = pd.DataFrame({'gametime': gametimes, 'lead':team1score-team2score,team1:team1score, team2:team2score})
    ax = gameframe.plot(ax=axes, 
                        x='gametime', 
                        y=[team1, team2], 
                        ylim=(0,120),
                        xlim=(0,7200),
                        xticks=[0,1800, 3600, 5400, 7200],
                        linewidth=2,
                        legend=True, 
                        sharex=True, sharey=True,
                        title=title)
    
    #ax.get_xaxis().set_major_formatter(formatter)
    ax.set_xlabel('')
    ax.legend(loc='upper left')



    
def plot_data(df, subcolumn=3):

    # id of row and col of a subgraph
    pcol = 0
    prow = 0

    grouped = df.groupby(['round','game'])
    total = len(grouped)
    nrows = total/subcolumn
    if total % subcolumn:
        nrows+=1


    graphtogether = False

    fig = plt.figure(figsize=(12,12))
    #ax = fig.add_subplot(2,1,1) # two rows, one column, first plot
    axes = fig.add_axes([0.15, 0.1, 0.7, 0.7])


    for groupid, group in grouped:
        print groupid, group.team1.unique()[0], group.team2.unique()[0]
        gameround = groupid[0]
        gameid = groupid[1]
        team1 = group.team1.unique()[0]
        team2 = group.team2.unique()[0]

        #ax = axes[prow, pcol] if not graphtogether else axes
        ax = plt.subplot2grid((nrows,subcolumn),(prow, pcol)) if not graphtogether else axes
        title = (team1+' vs. '+team2) if not graphtogether else 'Score'
        plotgame(ax, team1, team2, title, group)

        pcol+=1
        if pcol == subcolumn:
            pcol=0
            prow+=1


    #plt.show()
    plotid = mpld3.utils.get_id(axes)

    #xticklabels = map(lambda x:'%2dm:%2ds' % (x/60, x%60), [0,1800, 3600, 5400, 7200])
    xticklabels = map(lambda x:'%2dm' % (x/60), [0,1800, 3600, 5400, 7200])
    print xticklabels

    ax_ori = RotateTick(0, xticklabels, 0, total, subcolumn)
    mpld3.plugins.connect(fig, ax_ori)
    #mpld3.show(fig)

    fightml = mpld3.fig_to_html(fig)
    return plotid, fightml


def request_graph(year, style, exarg):

    filename = "allstats_ex_finals_"+year+".csv"
    allstats = pd.read_csv(filename,
                           names=['player1','score1', 'time', 'player2', 'score2','team1','team2','round', 'game'])
    print allstats[:5]
    allrounds = np.unique(allstats.round.values)
    allteams = np.unique(allstats.team1.values)
    print allrounds
    print allteams

    final_filename = "allstats_finals_"+year+".csv"
    final_stats = pd.read_csv(final_filename,
                           names=['player1','score1', 'time', 'player2', 'score2','team1','team2','round', 'game'])

    
    plotid=''
    fightml=''

    if style=='round':
        plotround = allrounds[int(exarg)]
        print '-- round:', plotround
        thisroundgames = allstats[allstats.round == plotround]
        plotid, fightml = plot_data(thisroundgames)
    elif style=='team1':
        plotteam = exarg #allteams[teamid]
        print '-- team1:', plotteam
        thisteam1games = allstats[allstats.team1 == plotteam]
        plotid, fightml = plot_data(thisteam1games)
    elif style=='team2':
        plotteam = exarg
        print '-- team2:', plotteam
        thisteam2games = allstats[allstats.team2 == plotteam]
        plotid, fightml = plot_data(thisteam2games)
    elif style == 'final':
        print '-- finals:'
        plotid, fightml = plot_data(final_stats)

    return plotid, fightml



if __name__ == '__main__':


    roundid = 0
    plotid, fightml = request_graph('2011', 'round', roundid)
    #plotid, fightml = request_graph('2011', 'team1', 'Sydney')


    # to save the results
    with open("fig.html", "wb") as fh:
        fh.write(fightml)
