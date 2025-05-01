import pandas as pd
import streamlit as st
import plotly.express as px

# File path and worksheet name
file_path = r"./NBA Picks.xlsx"
worksheet_name = "All_Data"

# Load the Excel file
@st.cache_data
def load_data():
    return pd.read_excel(file_path, sheet_name=worksheet_name)

# Load data
data = load_data()

# Create the navigation menu
st.sidebar.title('Navigation')
page = st.sidebar.radio("Go to", ["Main", "Questions", "Submit Answers", "Awards"])

if page == "Main":
    st.title("NBA Picks 🏀")

    years = list(data['Year'].unique())
    years.append('All')
    selected_year = st.selectbox("Select Year", options=sorted(years))

    if selected_year == 'All':
        filtered_data = data
    else:
        filtered_data = data[data['Year'] == selected_year]

    # Calculate Result % for each user
    user_picks = filtered_data.groupby('User').sum(numeric_only=True)
    total_results = len(filtered_data)
    user_picks['Result %'] = (user_picks['Result'] / total_results) * 100
    user_picks_summary = user_picks[['Result %']].reset_index()

    st.dataframe(user_picks_summary)

    # Line chart for Result % by year
    if selected_year != 'All':
        result_percentage_by_year = data.groupby(['Year', 'User'])['Result'].sum().unstack().fillna(0)
        result_percentage_by_year = result_percentage_by_year.div(data.groupby('Year')['Result'].count(), axis=0) * 100
        plot_df = result_percentage_by_year.sort_index().reset_index()
        plot_df_melted = plot_df.melt(id_vars='Year', var_name='User', value_name='Result %')

        color_map = {user: 'blue' if user == 'Tyler' else 'red' for user in plot_df_melted['User'].unique()}

        fig = px.line(
            plot_df_melted,
            x='Year',
            y='Result %',
            color='User',
            color_discrete_map=color_map
        )

        st.plotly_chart(fig)

elif page == "Questions":
    st.title("Data Overview")

    years = list(data['Year'].unique())
    selected_year = st.selectbox("Select Year to Filter", options=sorted(years))

    if selected_year:
        filtered_data = data[data['Year'] == selected_year]
    else:
        filtered_data = data

    st.dataframe(filtered_data)

elif page == "Submit Answers":
    st.title("Submit Answers")

    with st.form(key='submit_answers_form'):
        answers = []
        for i in range(1, 9):
            st.write(f"Question {i}")
            user = st.text_input(f"User {i}")
            question = st.text_input(f"Question {i}")
            guess = st.text_input(f"Guess {i}")
            answers.append({'User': user, 'Question': question, 'Guess': guess})

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            for i, answer in enumerate(answers, 1):
                st.write(f"**Answer {i}:**")
                st.write(f"User: {answer['User']}")
                st.write(f"Question: {answer['Question']}")
                st.write(f"Guess: {answer['Guess']}")
            # Optional: Save to file or database

elif page == "Awards":
    st.title("🏆 Awards Results")

    awards = {
        "MVP": "Most Valuable Player (MVP)",
        "ROY": "Rookie of the Year (ROY)",
        "DPOY": "Defensive Player of the Year (DPOY)",
        "6th": "6th Man of the Year",
        "NBA Champion": "NBA Champion",
        "Coach of Year": "Coach of the Year",
        "MIP": "Most Improved Player (MIP)"
    }

    for keyword, display_name in awards.items():
        st.subheader(f"🏅 {display_name}")

        award_data = data[data['Question'].str.contains(keyword, case=False, na=False)]

        if not award_data.empty:
            summary = (
                award_data.groupby('User')['Result']
                .agg(['sum', 'count'])
                .reset_index()
            )
            summary['Result %'] = (summary['sum'] / summary['count']) * 100
            summary = summary.rename(columns={'sum': 'Correct', 'count': 'Total'})

            st.dataframe(summary[['User', 'Correct', 'Total', 'Result %']])
        else:
            st.write("No data available for this award.")
