import streamlit as st
import pandas as pd
import numpy as np

from importfunc import file_import, filter_with_all
from graphfunc import seaborn_plot

# ------------- CONFIG ----------------------------------

st.set_page_config(page_title='import file', page_icon=None, layout="wide")

# hide_table_row_index = """
#     <style>
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     </style>
#     """

# st.markdown(hide_table_row_index, unsafe_allow_html=True)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# ------------- SETTINGS --------------------------------------
st.subheader('ROCKMASS HISTOGRAM', divider='grey')

# ------------- IMPORT FUNCTION --------------------------------

# Set the column names to import
option = st.sidebar.radio(
    'Method', ('RMR', 'Q'), horizontal=True)
if option == 'RMR':
    lst = ['BHID', 'Lithology', 'Interval', 'RQD', 'RMR', 'Weathering',
        'Strength', 'Spacing', 'Roughness', 'Infill']
else:
    lst = ['BHID', 'Lithology', 'Interval', 'RQD', 'Q', 'JN', 'JR', 'JA']
df = None
# Set error message (initial page)
error_message = f'''
    **Step 1:** Select method \n
    **Step 2:** Import excel or csv file \n
    **Step 3:** Select the correct columns for the histogram'''

df = file_import(lst, error_message) # file_import function under importfunc.py

if df is not None:
    cols = df.columns
    # ------------- FILTERS --------------------------------
    col1, col2 = st.columns(2, gap="medium")
    # Filter with Lithology: column number = 1
    with col1:
        df = filter_with_all(df, cols[1])
    # Filter with BHID: column number = 0
    with col2:
        df = filter_with_all(df, cols[0])
    # ------------- GRAPHING --------------------------------
    # RQD: column number = 3 ------------
    rqdlist = np.linspace(0, 100, 10)
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        seaborn_plot(df,cols[3], False, option, rqdlist, 'Histogram')
    with col2:
        seaborn_plot(df,cols[3], False, option, rqdlist, 'Cumulative')
    with col3:
        seaborn_plot(df,cols[3], False, option, rqdlist, 'Statistics')

    if option == 'RMR':
        # RMR: column number = 4 --------------
        rmrlist = np.linspace(0, 100, 10)
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            seaborn_plot(df,cols[4], False, option, rmrlist, 'Histogram')
        with col2:
            seaborn_plot(df,cols[4], False, option, rmrlist, 'Cumulative')
        with col3:
            seaborn_plot(df,cols[4], False, option, rmrlist, 'Statistics')
        # Other key inputs ---------------
        col1, col2, col3 = st.columns(3, gap="medium")
        # Weathering: column number = 5
        tgtlist = ('Decomposed', 'Highly W.', 'Moderately W.', 'Slightly W.', 'Fresh') # Set list
        ctgt = cols[5]
        df.loc[(df[ctgt] <= 0), 'temp'] = tgtlist[0]
        df.loc[(df[ctgt] > 0) & (df[ctgt] <= 1), 'temp'] = tgtlist[1]
        df.loc[(df[ctgt] > 1) & (df[ctgt] <= 3), 'temp'] = tgtlist[2]
        df.loc[(df[ctgt] > 3) & (df[ctgt] <= 5), 'temp'] = tgtlist[3]
        df.loc[(df[ctgt] > 5), 'temp'] = tgtlist[4]
        df[ctgt] = df['temp']
        df[ctgt] = pd.Categorical(values=df[ctgt], categories=tgtlist)
        df.sort_values([ctgt], inplace=True)
        with col1:
            seaborn_plot(df,ctgt, False, option, tgtlist, 'Histogram', 45)
        # Strength: column number = 6
        tgtlist = ('R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6') # Set list
        ctgt = cols[6]
        df.loc[(df[ctgt] <= 0), 'temp'] = tgtlist[0]
        df.loc[(df[ctgt] > 0) & (df[ctgt] <= 1), 'temp'] = tgtlist[1]
        df.loc[(df[ctgt] > 1) & (df[ctgt] <= 2), 'temp'] = tgtlist[2]
        df.loc[(df[ctgt] > 2) & (df[ctgt] <= 4), 'temp'] = tgtlist[3]
        df.loc[(df[ctgt] > 4) & (df[ctgt] <= 7), 'temp'] = tgtlist[4]
        df.loc[(df[ctgt] > 7) & (df[ctgt] <= 12), 'temp'] = tgtlist[5]
        df.loc[(df[ctgt] > 12), 'temp'] = tgtlist[6]
        df[ctgt] = df['temp']
        df[ctgt] = pd.Categorical(values=df[ctgt], categories=tgtlist)
        df.sort_values([ctgt], inplace=True)
        with col2:
            seaborn_plot(df,ctgt, False, option, tgtlist, 'Histogram', 0)
        # Spacing: column number = 7
        tgtlist = ('< 0.06', '0.06-0.2', '0.2-0.6', '0.6-2', '> 2') # Set list
        ctgt = cols[7]
        df.loc[(df[ctgt] <= 0.06), 'temp'] = tgtlist[0]
        df.loc[(df[ctgt] > 0.06) & (df[ctgt] <= 0.2), 'temp'] = tgtlist[1]
        df.loc[(df[ctgt] > 0.2) & (df[ctgt] <= 0.6), 'temp'] = tgtlist[2]
        df.loc[(df[ctgt] > 0.6) & (df[ctgt] <= 2.0), 'temp'] = tgtlist[3]
        df.loc[(df[ctgt] > 2), 'temp'] = tgtlist[4]
        df[ctgt] = df['temp']
        df[ctgt] = pd.Categorical(values=df[ctgt], categories=tgtlist)
        df.sort_values([ctgt], inplace=True)
        with col3:
            seaborn_plot(df,ctgt, False, option, tgtlist, 'Histogram', 0)
        col1, col2, col3 = st.columns(3, gap="medium")
        # Roughness: column number = 8
        tgtlist = ('PK', 'PS', 'PR', 'UR', 'SR') # Set list
        ctgt = cols[8]
        df.loc[(df[ctgt] <= 0), 'temp'] = tgtlist[0]
        df.loc[(df[ctgt] > 0) & (df[ctgt] <= 1), 'temp'] = tgtlist[1]
        df.loc[(df[ctgt] > 1) & (df[ctgt] <= 3), 'temp'] = tgtlist[2]
        df.loc[(df[ctgt] > 3) & (df[ctgt] <= 5), 'temp'] = tgtlist[3]
        df.loc[(df[ctgt] > 5), 'temp'] = tgtlist[4]
        df[ctgt] = df['temp']
        df[ctgt] = pd.Categorical(values=df[ctgt], categories=tgtlist)
        df.sort_values([ctgt], inplace=True)
        with col1:
            seaborn_plot(df,ctgt, False, option, tgtlist, 'Histogram', 0)
        # Infill: column number = 9
        tgtlist = ('Soft > 5mm', 'Soft < 5mm', 'Hard > 5 mm', 'Hard < 5mm', 'None') # Set list
        ctgt = cols[9]
        df.loc[(df[ctgt] <= 0), 'temp'] = tgtlist[0]
        df.loc[(df[ctgt] > 0) & (df[ctgt] <= 2), 'temp'] = tgtlist[1]
        df.loc[(df[ctgt] > 2) & (df[ctgt] <= 3), 'temp'] = tgtlist[2]
        df.loc[(df[ctgt] > 3) & (df[ctgt] <= 4), 'temp'] = tgtlist[3]
        df.loc[(df[ctgt] > 4), 'temp'] = tgtlist[4]
        df[ctgt] = df['temp']
        df[ctgt] = pd.Categorical(values=df[ctgt], categories=tgtlist)
        df.sort_values([ctgt], inplace=True)
        with col2:
            seaborn_plot(df,ctgt, False, option, tgtlist, 'Histogram', 45)
        # Lith: column number = 1
        lithlst = df[cols[1]].unique().tolist()
        df.sort_values([cols[1]], inplace=True)
        with col3:
            seaborn_plot(df,cols[1], False, option, lithlst, 'Histogram')
    else:
        # Q: column number = 4 ----------------
        qlist = [0.0001, 0.001, 0.01, 0.1, 1, 4, 10, 40, 100, 400, 1000]
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            seaborn_plot(df,cols[4], True, option, qlist, 'Histogram')
        with col2:
            seaborn_plot(df,cols[4], True, option, qlist, 'Cumulative')
        with col3:
            seaborn_plot(df,cols[4], True, option, qlist, 'Statistics')

        col1, col2, col3 = st.columns(3, gap="medium")
        # JN: column number = 5
        jnlst = ('1 js', '2 js', '2 js + rand.', '3 js')
        cjn = cols[5]
        df.loc[(df[cjn] <= 2), 'JN new'] = jnlst[0]
        df.loc[(df[cjn] > 2) & (df[cjn] <= 4), 'JN new'] = jnlst[1]
        df.loc[(df[cjn] > 4) & (df[cjn] <= 6), 'JN new'] = jnlst[2]
        df.loc[(df[cjn] > 6), 'JN new'] = jnlst[3]
        df[cjn] = df['JN new']
        df[cjn] = pd.Categorical(values=df[cjn], categories=jnlst)
        df[cjn] = df[cjn].cat.remove_unused_categories()
        df.sort_values([cjn], inplace=True)
        with col1:
            seaborn_plot(df,cjn, False, option, jnlst, 'Histogram', 45)

        # JR: column number = 6
        jrlst = ['PP', 'PS', 'PR', 'US', 'UR', 'Disc.']
        cjr = cols[6]
        df.loc[(df[cjr] <= 0.5), 'JR new'] = jrlst[0]
        df.loc[(df[cjr] > 0.5) & (df[cjr] <= 1.0), 'JR new'] = jrlst[1]
        df.loc[(df[cjr] > 1.0) & (df[cjr] <= 1.5), 'JR new'] = jrlst[2]
        df.loc[(df[cjr] > 1.5) & (df[cjr] <= 2.0), 'JR new'] = jrlst[3]
        df.loc[(df[cjr] > 2.0) & (df[cjr] <= 3.0), 'JR new'] = jrlst[4]
        df.loc[(df[cjr] > 3.0) & (df[cjr] <= 4.0), 'JR new'] = jrlst[5]
        df[cjr] = df['JR new']
        df[cjr] = pd.Categorical(values=df[cjr], categories=jrlst)
        df.sort_values([cjr], inplace=True)
        with col2:
            seaborn_plot(df,cjr, False, option, jrlst, 'Histogram', 0)

        # JA: column number = 7
        jalst = ['Unaltered', 'Non-softening', 'Low Friction']
        cja = cols[7]
        df.loc[(df[cja] <= 1.0), 'JA new'] = jalst[0]
        df.loc[(df[cja] > 1.0) & (df[cja] <= 2.0), 'JA new'] = jalst[1]
        df.loc[(df[cja] > 2.0), 'JA new'] = jalst[2]
        df[cja] = df['JA new']
        df[cja] = pd.Categorical(values=df[cja], categories=jalst)
        df.sort_values([cja], inplace=True)
        with col3:
            seaborn_plot(df,cja, False, option, jalst, 'Histogram', 45)

        col1, col2, col3 = st.columns(3, gap="medium")
        # Lith: column number = 1
        lithlst = df[cols[1]].unique().tolist()
        df.sort_values([cols[1]], inplace=True)
        with col1:
            seaborn_plot(df,cols[1], False, option, lithlst, 'Histogram')

