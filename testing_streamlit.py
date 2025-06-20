import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Set page configuration for a wider layout
st.set_page_config(layout="wide")

st.title("Academic Performance Dashboard -- BPSJC")

st.write("""
This application allows you to visualize student academic performance.
Select academic years and specific admission numbers to generate a chart of their marks.
""")
sm = pd.read_csv('sm.csv',usecols=['ADMNO','STUD_NAME'])
# --- 1. Generate Sample Data ---
# In a real application, you would load this from a database or a file (CSV, Excel, etc.)
@st.cache_data
def load_data():
    # data = {
    #     'academic_year': [2021, 2021, 2021, 2021, 2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023, 2021, 2022, 2023],
    #     'admno':         [1001, 1002, 1003, 1001, 1001, 1002, 1003, 1004, 1001, 1002, 1004, 1003, 1004, 1004, 1001],
    #     'subject':       ['Math', 'Physics', 'Chemistry', 'English', 'Math', 'Physics', 'Chemistry', 'Biology', 'Math', 'Physics', 'Biology', 'English', 'Science', 'Science', 'English'],
    #     'marks_obtained': [85, 78, 92, 65, 90, 80, 88, 70, 95, 85, 72, 68, 75, 80, 90]
    # }
    # df = pd.DataFrame(data)
    df1 = pd.read_csv('2023.csv')
    df2 = pd.read_csv('2024.csv')
    df3 = pd.read_csv('2025.csv')

    df=pd.concat([df1,df2,df3],axis=0)
    return df

df = load_data()

# Get unique academic years and admission numbers for the multiselects
all_academic_years = sorted(df['AY_ID'].unique())
all_adm_numbers = sorted(df['ADMNO'].unique())

# --- 2. Create Multiselect Form Elements ---
st.sidebar.header("Filter Options")

# Multi-select for Academic Years
selected_academic_years = st.sidebar.multiselect(
    "Select Academic Year(s):",
    options=all_academic_years,
    default=all_academic_years# Default to all years
    # default = all_academic_years[-1] #current year
)

# Multi-select for Admission Numbers
selected_adm_numbers = st.sidebar.multiselect(
    "Select Admission Number(s):",
    options=all_adm_numbers,
    default=[] # Default to no students selected
)

# --- 3. Filter Data Based on Selections ---
if not selected_academic_years and not selected_adm_numbers:
    st.info("Please select at least one academic year or admission number to display data.")
    filtered_df = pd.DataFrame() # Empty DataFrame if no selections
elif not selected_academic_years:
    st.warning("Please select at least one academic year.")
    filtered_df = pd.DataFrame()
elif not selected_adm_numbers:
    st.warning("Please select at least one admission number.")
    filtered_df = pd.DataFrame()
else:
    # Filter by academic year
    filtered_df = df[df['AY_ID'].isin(selected_academic_years)]
    filtered_df = df[df['EXAM_ID']=='FINAL']
    # Filter by admission number
    filtered_df = filtered_df[filtered_df['ADMNO'].isin(selected_adm_numbers)]

# Sort the filtered data for better chart readability
# filtered_df = filtered_df.sort_values(by=['AY_ID', 'ADMNO', 'SUB_ID']).reset_index(drop=True)


# --- 4. Generate and Display Chart ---
if not filtered_df.empty:
    filtered_df = filtered_df.sort_values(by=['AY_ID', 'ADMNO', 'SUB_ID']).reset_index(drop=True)
    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df)

    # st.subheader("Marks Obtained Chart")

    # Determine chart type based on the number of selected students/years
#     if len(selected_adm_numbers) <= 5 and len(selected_academic_years) <= 3:
#         # Use a grouped bar chart if the selections are manageable
#         fig = px.bar(
#             filtered_df,
#             x='SUB_ID',
#             y='MARKS_OBTAINED',
#             color='ADMNO',
#             facet_col='AY_ID',
#             facet_col_wrap=2,
#             title='Marks by Subject for Selected Students and Years',
#             labels={'marks_obtained': 'Marks Obtained', 'subject': 'Subject', 'admno': 'Admission Number'},
#             hover_name="ADMNO",
#             hover_data={"AY_ID": True, "SUB_ID": True, "MARKS_OBTAINED": True}
#         )
#         fig.update_layout(
#             height=400 + 200 * (len(selected_academic_years) // 2), # Adjust height dynamically
#             bargap=0.2,
#             margin=dict(t=50, b=0, l=0, r=0)
#         )
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         # For larger selections, a line chart might be clearer or a different aggregation
#         st.info("Large selection detected. Displaying a line chart for clarity. Consider refining your filters for a grouped bar chart.")
#         fig = px.line(
#             filtered_df,
#             x='academic_year',
#             y='marks_obtained',
#             color='admno',
#             line_group="subject", # Group lines by subject for each student
#             title='Marks Trend for Selected Students Across Years',
#             labels={'marks_obtained': 'Marks Obtained', 'academic_year': 'Academic Year', 'admno': 'Admission Number'},
#             hover_name="admno",
#             hover_data={"academic_year": True, "subject": True, "marks_obtained": True}
#         )
#         fig.update_traces(mode='lines+markers')
#         fig.update_layout(hovermode="x unified")
#         st.plotly_chart(fig, use_container_width=True)

else:
    st.write("No data to display based on your current selections.")
for admno in selected_adm_numbers:
    try:
        sname = sm.loc[sm['ADMNO']==admno,'STUD_NAME'].iloc[0]
    except:
        sname = ''
    title = str(admno) + '--' + sname
    st.subheader(f"Marks Obtained Chart - {sname}")
    fdf = filtered_df[filtered_df['ADMNO']==admno]
    fdf = fdf[~fdf['SUB_ID'].isin(['CA','GK'])]
    fdf = fdf[fdf['AY_ID'].isin(selected_academic_years)]
    # filtered_df = df[df['EXAM_ID']=='FINAL']
    fig = px.bar(fdf,x='SUB_ID',y='MARKS_OBTAINED',color='AY_ID',title=title,barmode='group',text_auto=True,
                 labels = {'SUB_ID':'Subject','MARKS_OBTAINED':'Marks'})
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    # fig.show()
    # fig.write_html(str(admno)+' '+sname+".html")
    st.plotly_chart(fig, use_container_width=True, )

st.sidebar.markdown("---")
st.sidebar.info("Adjust the filters above to see different visualizations.")
