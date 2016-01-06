from numpy.random import randn
import numpy as np
import pandas as pd

np.set_printoptions(precision=4)
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from mpl_toolkits.axes_grid1 import make_axes_locatable

import mpld3
from mpld3plugins import FormatTick, RotateTick


def sort_teamgames(game):
    #game['lead'] = game.team1score - game.team2score
    game.loc[:,'lead'] = game.team1score - game.team2score
    team1_perf = game.pivot_table('lead', #index='team2', 
                                  columns='team1', aggfunc=sum)
    #print team1_perf

    #game['lead2'] = game.team2score - game.team1score
    game.loc[:,'lead2'] = game.team2score - game.team1score
    team2_perf = game.pivot_table('lead2', #index='team1', 
                                  columns='team2', aggfunc=sum)
    #print team2_perf

    perf = team1_perf + team2_perf

    perf.sort(ascending=False)
    print perf

    sorted_team = perf.index.values
    df = pd.DataFrame({})
    df2 = pd.DataFrame({})

    # when use group function, all NaN values are stripped
    for groupid, group in game.groupby(['team1']):
        #print groupid, group.lead.values

        #c = group.sort('lead', ascending=False)
        #print groupid, c.lead.values
        #print df[groupid]
        df[groupid] = group.lead.values


    for groupid, group in game.groupby(['team2']):
        #c = group.sort('lead2', ascending=False)
        df2[groupid] = group.lead2.values


    frames = [df, df2]

    result = pd.concat(frames, ignore_index=True)

    sorted_teamgames = pd.DataFrame({})

    for team in sorted_team:
        teamplay = result[team].copy()
        teamplay.sort(ascending=False)
        sorted_teamgames[team] = teamplay.values

    return sorted_team, sorted_teamgames



def plot_team(sorted_team, sorted_teamgames):

    fig = plt.figure(figsize=(12, 12))
    #ax = fig.add_axes([0.15, 0.1, 0.7, 0.7])
    grid = ImageGrid(fig, 
                     (0.2, 0.15, 0.8, 0.8),
                     #111, 
                     nrows_ncols=(1, 1),
                     direction='row', axes_pad=0.05, add_all=True,
                     label_mode='1', share_all=False,
                     cbar_location='right', cbar_mode='single',
                     cbar_size='5%', cbar_pad=0.05)

    ax = grid[0]
    ax.set_title('Game lead (each team is a column)', fontsize=20)
    ax.tick_params(axis='both', direction='out', labelsize=12)
    #im = ax.imshow(df.values, interpolation='nearest', vmax=df.max().max(),
    #               vmin=df.min().min(), cmap='RdBu')
    im = ax.imshow(sorted_teamgames.values, interpolation='nearest', vmax=120, vmin=-120, cmap='RdBu')
    #colorbar
    ax.cax.colorbar(im)
    ax.cax.tick_params(labelsize=12)

    ax.set_xticks(np.arange(sorted_teamgames.shape[1]))
    ax.set_xticklabels(sorted_team, rotation='vertical', fontweight='bold')
    ax.set_yticks(np.arange(sorted_teamgames.shape[0]))
    ax.set_yticklabels(sorted_teamgames.index)

    ax.set_ylabel("Sorted game", size=16)
    #plt.show()
    plotid = mpld3.utils.get_id(ax)


    print sorted_team
    ax_ori = RotateTick(0, sorted_team.tolist(), -90, 1,1)
    mpld3.plugins.connect(fig, ax_ori)
    mpld3.show()

    fightml = mpld3.fig_to_html(fig)
    return plotid, fightml


def plot_summary(game):

    x = game.team1score
    y = game.team2score

    fig, axScatter = plt.subplots(figsize=(12, 12), subplot_kw=dict(axisbg='#EEEEEE'))

    # the scatter plot:
    size = x + y
    color = np.fabs(x - y)
    scatter = axScatter.scatter(x, y, s=size, c=color, alpha=0.5)
    axScatter.set_aspect(1.)
    axScatter.set_xlabel('team1 score', size=20)
    axScatter.set_ylabel('team2 score', size=20)
    axScatter.grid(color='white', linestyle='solid')

    # create new axes on the right and on the top of the current axes
    # The first argument of the new_vertical(new_horizontal) method is
    # the height (width) of the axes to be created in inches.
    divider = make_axes_locatable(axScatter)
    axHistx = divider.append_axes("top", 1.2, pad=0.2, sharex=axScatter, axisbg='#EEEEEE')
    axHisty = divider.append_axes("right", 1.2, pad=0.3, sharey=axScatter, axisbg='#EEEEEE')

    # make some labels invisible
    plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(),
             visible=False)

    # now determine nice limits by hand:
    binwidth = 5
    xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])
    lim = (int(xymax/binwidth) + 1)*binwidth

    binnum = np.arange(0, lim + binwidth, binwidth)
    axHistx.hist(x, bins=binnum)
    axHisty.hist(y, bins=binnum, orientation='horizontal')


    # the xaxis of axHistx and yaxis of axHisty are shared with axScatter,
    # thus there is no need to manually adjust the xlim and ylim of these
    # axis.

    #axHistx.axis["bottom"].major_ticklabels.set_visible(False)
    for tl in axHistx.get_xticklabels():
        tl.set_visible(False)
    axHistx.set_yticks([0, 30])

    #axHisty.axis["left"].major_ticklabels.set_visible(False)
    for tl in axHisty.get_yticklabels():
        tl.set_visible(False)
    axHisty.set_xticks([0, 30])

    #plt.draw()
    #plt.show()
    plotid = mpld3.utils.get_id(axScatter)


    # Define some CSS to control our custom labels
    css = """
    table
    {
      border-collapse: collapse;
    }
    th
    {
      color: #ffffff;
      background-color: #aaa;
    }
    td
    {
      background-color: #cccccc;
    }
    table, th, td
    {
      font-family:Arial, Helvetica, sans-serif;
      border: 1px solid gray;
      text-align: middle;
    }
    """

    #labels = ['Round {}, {} vs. {}, {}:{}'.format(g[1], g[2], g[3], g[4], g[5]) for g in game.itertuples()]
    labels = []
    print game.shape
    for i in range(game.shape[0]):
        label = game.ix[[i],:].T
        label.columns = ['Game Info']
        labels.append(str(label.to_html()))

    tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=labels, voffset=10, hoffset=10, css=css)
    mpld3.plugins.connect(fig, tooltip)
    mpld3.show()

    fightml = mpld3.fig_to_html(fig)
    return plotid, fightml



def request_graph(year, style):
    filename = 'allgames_'+year+'.txt'
    game = pd.read_csv(filename,
                    names=['Round', 'team1', 'team2', 'team1score', 'team2score'])
    #print game[:5]

    ex_finals = game[game.Round != 'Finals']
    finals = game[game.Round == 'Finals']

    if style == 'all':
        st, stgames = sort_teamgames(ex_finals)
        plotid, fightml = plot_team(st, stgames)
    elif style == 'summary':
        plotid, fightml = plot_summary(game)
    return plotid, fightml


if __name__ == '__main__':


    plotid, fightml = request_graph('2013', 'all')#'summary')

    # to save the results
    with open("fig.html", "wb") as fh:
        fh.write(fightml)
