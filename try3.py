import bi_project
import streamlit as st

your_name = st.text_input("Enter your name")
st.write("Hello", your_name)

import pandas as pd
st.subheader("Dataset")
df=pd.DataFrame()



data_file = st.file_uploader("Upload CSV",type=["csv"])
		
if data_file is not None:
    file_details = {"filename":data_file.name, "filetype":data_file.type,
                            "filesize":data_file.size}
			
    st.write(file_details)
    df = pd.read_csv(data_file)
    st.write(df.shape)
    st.dataframe(df)
    st.subheader("Forecasted ECG signal")
    p=bi_project.clean(df)
    st.pyplot(fig=p)
