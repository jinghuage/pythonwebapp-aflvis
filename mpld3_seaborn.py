

# http://stackoverflow.com/questions/31480921/how-to-make-mpld3-work-with-seaborn-interactive-tooltips
# https://mpld3.github.io/_modules/mpld3/plugins.html


import matplotlib.pyplot as plt
import mpld3
import pandas as pd
import numpy as np
import seaborn as sns


N=10
data = pd.DataFrame({"x": np.random.randn(N),
                     "y": np.random.randn(N), 
                     "size": np.random.randint(20,200, size=N),
                     "label": np.arange(N)
                     })


scatter_sns = sns.lmplot("x", "y", 
           scatter_kws={"s": data["size"]},
           robust=False, # slow if true
           data=data, size=8)
fig = plt.gcf()

ax = plt.gca()
pts = ax.get_children()[3]


#data_tip_points = ax.scatter(x_points, y_points, alpha=0.001)
#tooltip = plugins.PointLabelTooltip(data_tip_points, labels)

tooltip = mpld3.plugins.PointLabelTooltip(pts, labels=list(data.label))
mpld3.plugins.connect(fig, tooltip)

mpld3.show(fig)
