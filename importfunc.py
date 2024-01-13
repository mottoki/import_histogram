import streamlit as st
import pandas as pd
import numpy as np
import difflib

def file_import(lst, error_messages='Upload File'):
    # ------------- IMPORT ----------------------------------
    # Import file
    files = st.sidebar.file_uploader("Upload file", accept_multiple_files=True)

    df = None # Initialise

    for file in files:
        # CSV
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
            selection_cols = df.columns

        # Excel
        elif file.name.endswith('.xlsx'):
            xl = pd.ExcelFile(file)
            sheets = xl.sheet_names
            # Type the sheet number the data is located
            sheetnum = st.sidebar.number_input('Sheet number that contains data',
                min_value=1, value="min")
            df = xl.parse(sheets[sheetnum - 1], header=0)
            selection_cols = df.columns

    # ------------- Columns -----------------------
    if df is not None:
        st.sidebar.title('Select columns')
        cols = []
        for k in lst:
            # Target columns
            target_selection = list(selection_cols)
            # Guess the column
            guess = difflib.get_close_matches(k, target_selection, n=1, cutoff=0.3)
            if guess:
                guess_index = target_selection.index(guess[0])
            else:
                # If there is no guess
                guess_index = 1 # Column number
            # Show the seection box
            target_col = st.sidebar.selectbox(f'Select {k} column',
                target_selection, index=guess_index)

            cols.append(target_col)

        df = df[cols]
    else:
        st.write(error_messages)
    return df


# ------------- FILTER FUNCTIONS ----------------------
def filter_with_all(df, col):
    container = st.container()
    all_sel = st.checkbox("Select all",
        key=f"{col.replace(' ','')}_all_select")
    myselect = sorted(set(df[df[col].notna()][col]))
    if all_sel:
        selected = container.multiselect(f"{col} filter", (myselect), (myselect))
        if selected: df = df[df[col].isin(selected)]
    else:
        selected = container.multiselect(f"{col} filter", (myselect))
        if selected: df = df[df[col].isin(selected)]
    st.write(" ")
    return df
