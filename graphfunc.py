import streamlit as st
import numpy as np
import pandas as pd
from math import log
import matplotlib.pyplot as plt
import seaborn as sns

from calcfunc import weighted_average, weighted_median

# ------------------ SEABORN GRAPH ----------------------------------
# Formatting the graph
def graph_neat(plt, col, title, xtitle=True):
    # Add ticks
    plt.xticks(size = 12)
    plt.yticks(size = 12)
    # Add Labels
    if xtitle:
        plt.xlabel(f'{col}', size = 12)

    if title == 'Histogram':
        plt.ylabel('Percentage', size = 12)
    else:
        plt.ylabel('Percentile', size = 12)
    #Title
    plt.title(f'{col}')

def seaborn_histogram(df, col, rotation=45):
    dp = df[col].value_counts(normalize=True, sort=False)*100
    x_dp = dp.index
    fig, ax = plt.subplots()
    y = sns.barplot(x=x_dp, y=dp, gap=0, width=0.9, saturation=0.6,
        color=sns.color_palette("husl",8)[5], edgecolor='black')
    plt.setp(ax.patches, linewidth=1)

    # Number for each histogram
    y.set(xlabel=col)
    labels = [int(v) if v >= 1 else round(v,1) for v in y.containers[0].datavalues]
    labels = [str(v) if v else '' for v in labels]
    # labels = [str(f'{v:.1f}') if v else '' for v in y.containers[0].datavalues]
    y.bar_label(y.containers[0], labels=labels, size=10)

    ax.tick_params(axis='x', rotation=rotation)
    ax.set_xlabel('')

    # XY axis and title function
    graph_neat(plt, col, 'Histogram', False)

    # Display
    st.pyplot(fig)


def seaborn_plot(df, col, log_scale, option, rang, grph, rotation=90):
    # Weighted with interval
    cinterval = df.columns[2]
    intlist = df[cinterval].tolist()
    # xlist is the target column values
    xlist = df[col].tolist()
    # Categorise
    if all(isinstance(e, (int, float)) for e in rang): # Check Number
        if option == "Q" and log_scale==True: # Q
            qrange = [log(r,10) for r in rang]
            bins = qrange
            binrange = [min(qrange),max(qrange)]
            cum_xmin = 10**min(qrange)
            discrete = False
        else: # RQD, RMR
            bins = len(rang)
            binrange = [0, 100]
            cum_xmin = min(xlist)
            discrete = False
    else: # String Category
        bins = len(rang)
        binrange = None
        cum_xmin = min(xlist)
        discrete = True

    # Histogram -----------------------
    if grph == 'Histogram':
        fig, ax = plt.subplots()
        y = sns.histplot(x=xlist, weights=intlist, binrange=binrange,
            bins=bins, stat='percent', legend=False, log_scale=log_scale,
            discrete=discrete)

        y.set(xlabel=col)
        labels = [int(v) if v >= 1 else round(v,1) for v in y.containers[0].datavalues]
        labels = [str(v) if v else '' for v in labels]
        # labels = [str(f'{v:.1f}') if v else '' for v in y.containers[0].datavalues]
        y.bar_label(y.containers[0], labels=labels, size=10)

        # If discrete x-axis
        if discrete == True:
            y.set_xticks(rang)
            ax.tick_params(axis='x', rotation=rotation)
        # XY axis and title function
        graph_neat(plt, col, 'Histogram')

        # Display
        st.pyplot(fig)

    # Cumulative -----------------------
    elif grph == 'Cumulative':
        fig2, ax2 = plt.subplots()
        sns.ecdfplot(data=df, x=col, weights=cinterval,
            linewidth=3, log_scale=log_scale)
        ps = [0.25, 0.5, 0.75] # Percentile values
        for p in ps:
            # Find Percentile exceedance value
            for line in ax2.get_lines():
                x2, y2 = line.get_data()
                ind = np.argwhere(y2 >= p)[0, 0]  # first index where y is larger than percentile value, p
                value = x2[ind]

            # Lines and Texts
            if option == "Q" and log_scale==True: # Q
                # Shift value is for shifting the text slightly
                shiftval = np.log10(value/1.4)
                cum_xshift = 10**shiftval
            else: # RQD or RMR
                cum_xshift = (max(xlist) - min(xlist)) / 12

            plt.hlines(y=p, xmin=cum_xmin, xmax = value,
                linestyles = ':', colors = 'purple', linewidth = 2)

            plt.vlines(x=value, ymin=0, ymax = p,
                linestyles = ':', colors = 'purple', linewidth = 2)

            plt.text(x = cum_xmin, y = p+0.02,
                # transform = ax.transAxes,
                s = f'{int(100*p)}%', size = 12,
                color = 'purple', alpha = 0.7)

            plt.text(x = value - cum_xshift, y = p+0.02, size = 12,
                horizontalalignment = 'left',
                s = f'{value:.0f}', color = 'purple', alpha = 0.8)

        # XY axis and title function
        graph_neat(plt, col, 'Cumulative Plot')

        # Display
        st.pyplot(fig2)

    # Statistics -----------------------
    else:
        length = df[cinterval].sum()
        wmean, wstd = weighted_average(df, col, cinterval)
        wmedian, wlowquant, whighquant = weighted_median(df, col, cinterval)
        stats = {
            'Total Interval': f'{length:.1f}',
            'Average': f'{wmean:.1f}',
            'Std Dev': f'{wstd:.1f}',
            '75th Quant': f'{whighquant:.1f}',
            '50th Quant': f'{wmedian:.1f}',
            '25th Quant': f'{wlowquant:.1f}'}
        dfstats = pd.DataFrame(stats.items(), columns=['Key', 'Value'])

        # Display
        st.write(f"{col} Statistics")
        dfstats = st.data_editor(dfstats,hide_index=True,
            use_container_width=True)
