import pandas as pd
import random
import os
import streamlit as st

# Function to load data from an Excel file
def load_data(file):
    df = pd.read_excel(file, header=None)
    df.columns = ['job']
    return df

# Function to save data to an Excel file
def save_data(file, data):
    df = pd.DataFrame(data, columns=['job1', 'job2', 'target'])
    df.to_excel(file, index=False)

# Load the existing pairs if they exist
data_file = '2.xls'
if os.path.exists(data_file):
    data = pd.read_excel(data_file)
    used_pairs = set(zip(data['job1'], data['job2']))
else:
    data = pd.DataFrame(columns=['job1', 'job2', 'target'])
    used_pairs = set()

# Function to handle button click
def on_button_clicked(b):
    global data, used_pairs

    target_value = 1 if b.label == 'Да' else 0

    # Get selected job names
    job1 = st.session_state.left_dropdown
    job2 = st.session_state.right_dropdown

    # Append data to DataFrame and save
    data = data.append({'job1': job1, 'job2': job2, 'target': target_value}, ignore_index=True)
    save_data(data_file, data)

    # Reset dropdowns with new random jobs
    reset_dropdowns()

# Function to reset dropdowns with new random jobs
def reset_dropdowns():
    global used_pairs, jobs

    while True:
        job1, job2 = random.sample(jobs, 2)
        if (job1, job2) not in used_pairs:
            break

    st.session_state.left_dropdown = job1
    st.session_state.right_dropdown = job2
    used_pairs.add((job1, job2))

# Main process
st.title("Job Pair Comparison")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    jobs = df['job'].tolist()

    if 'left_dropdown' not in st.session_state:
        st.session_state.left_dropdown = None
        st.session_state.right_dropdown = None

    if len(jobs) > 1:
        if st.session_state.left_dropdown is None:
            job1, job2 = random.sample(jobs, 2)
            st.session_state.left_dropdown = job1
            st.session_state.right_dropdown = job2

        left_dropdown = st.selectbox('Слева:', jobs, index=jobs.index(st.session_state.left_dropdown), key='left_dropdown')
        right_dropdown = st.selectbox('Справа:', jobs, index=jobs.index(st.session_state.right_dropdown), key='right_dropdown')

        col1, col2 = st.columns(2)
        with col1:
            button_yes = st.button("Да", on_click=on_button_clicked)
        with col2:
            button_no = st.button("Нет", on_click=on_button_clicked)

        st.write(data)