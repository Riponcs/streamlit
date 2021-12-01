import streamlit as st
import time
import numpy as np
import os
import pandas as pd

data_file = st.file_uploader("Upload Scintillometer Log", type=["CSV", "log"])
if data_file is not None:
    # st.write(type(data_file))
    # st.write(data_file)
    file_details = {"filename": data_file.name, "filetype": data_file.type, "filesize": data_file.size}
    st.write(file_details)
    df = pd.read_csv(data_file, sep=r'\t', engine='python', encoding= 'unicode_escape')
    st.write(""" # Unprocessed Log file """)
    st.dataframe(df)

    # Data Cleanup
    df = df.iloc[1:, :]
    to_drop = ['StatusFlags', "StatusFlags", "Udemod", "UdemodSig", "RecordNo", "Srt"]    
    df.drop([x for x in to_drop if x in df.columns], inplace=True, axis=1)
    
    df = df[df["Cn2"].astype(float)!=0]
    # df = df[df['Cn2'] < 0e-20]
    st.write(""" # Processed Log file """)
    st.dataframe(df)



    st.write(""" # Plot Cn2 """)
    stPoint = st.slider(label='Select Start Position', min_value=0, max_value=len(df), value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None)

    cnClip1 = np.array(df['Cn2'][stPoint:], dtype=float)
    cnClip2 = np.array(df['Cn2Min'][stPoint:], dtype=float)
    cnClip3 = np.array(df['Cn2Max'][stPoint:], dtype=float)
    
    
    cnClip = np.transpose(np.array([cnClip1, cnClip2, cnClip3]))
    cnDf = pd.DataFrame(cnClip, columns = ['Cn2', 'Cn2 Min', 'Cn2 Max'])
    # st.write(cnClip)
    st.line_chart(data=cnDf, width=0, height=0, use_container_width=True)




# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# # Streamlit widgets automatically run the script from top to bottom. Since
# # this button is not connected to any other logic, it just causes a plain
# # rerun.
# st.button("Re-run")