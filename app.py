import pandas as pd
import streamlit as st

file_path = "./NBA Picks.xlsx"
worksheet_name = "All_Data"

# Load the Excel file
@st.cache_data
def load_data():
    return pd.read_excel(file_path, sheet_name=worksheet_name)

# Load data
data = load_data()

# Create the navigation menu
st.sidebar.title('Navigation')
page = st.sidebar.radio("Go to", ["Main", "Questions", "Submit Answers"])

if page == "Main":
    # Page for displaying chart and summary
    st.title("NBA Picks 🏀")

    # Dropdown to select year
    years = list(data['Year'].unique())
    years.append('All')
    selected_year = st.selectbox("Select Year", options=sorted(years))

    # Filter data based on the selected year
    if selected_year == 'All':
        filtered_data = data
    else:
        filtered_data = data[data['Year'] == selected_year]

    # Calculate Result % for each user
    user_picks = filtered_data.groupby('User').sum()
    total_results = len(filtered_data)
    user_picks['Result %'] = (user_picks['Result'] / total_results) * 100
    user_picks_summary = user_picks[['Result %']].reset_index()

    # Display the result in Streamlit
    st.dataframe(user_picks_summary)

    # Calculate Result % for each user by year for chart
    if selected_year != 'All':
        result_percentage_by_year = data.groupby(['Year', 'User'])['Result'].sum().unstack().fillna(0)
        result_percentage_by_year = result_percentage_by_year.div(data.groupby('Year')['Result'].count(), axis=0) * 100
        
        # Plot the chart with lines for each user
        st.line_chart(result_percentage_by_year.sort_index())

elif page == "Questions":
    # Page for displaying the dataframe and filtering
    st.title("Data Overview")

    # Dropdown to select year
    years = list(data['Year'].unique())
    selected_year = st.selectbox("Select Year to Filter", options=sorted(years))

    # Filter data based on the selected year
    if selected_year:
        filtered_data = data[data['Year'] == selected_year]
    else:
        filtered_data = data

    # Display the dataframe
    st.dataframe(filtered_data)

elif page == "Submit Answers":
    # Page for submitting answers
    st.title("Submit Answers")

    with st.form(key='submit_answers_form'):
        # Form inputs for 8 questions
        answers = []
        for i in range(1, 9):
            st.write(f"Question {i}")
            user = st.text_input(f"User {i}")
            question = st.text_input(f"Question {i}")
            guess = st.text_input(f"Guess {i}")
            answers.append({'User': user, 'Question': question, 'Guess': guess})

        # Submit button
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            # Handle form submission
            for i, answer in enumerate(answers, 1):
                st.write(f"**Answer {i}:**")
                st.write(f"User: {answer['User']}")
                st.write(f"Question: {answer['Question']}")
                st.write(f"Guess: {answer['Guess']}")
            # Here you can add code to save the data to a file or database if needed
