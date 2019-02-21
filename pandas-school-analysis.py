import pandas as pd
data1 = "schools_complete.csv"
data2 = "students_complete.csv"
df1 = pd.read_csv(data1)
df2 = pd.read_csv(data2)

df = pd.merge(df1, df2, how="outer", on=["school_name", "school_name"])
tot_schools = len(df["school_name"].unique())
tot_students = df["school_name"].value_counts().sum()
tot_budget = df["budget"].unique().sum()
avg_math = df["math_score"].mean()
avg_reading = df["reading_score"].mean()
pass_math = len(df[df.math_score >= 70])/len(df)
pass_reading = len(df[df.reading_score >= 70])/len(df)
overall = ((avg_math + avg_reading)/2)/100

district_summary = pd.DataFrame({
"Total Schools" : [tot_schools],
"Total Students" : [tot_students],
"Total Budget" : [tot_budget],
"Average Math Score" : [avg_math],
"Average Reading Score" : [avg_reading],
"% Passing Math": [pass_math],
"% Passing Reading": [pass_reading],
"Overall Passing Rate": [overall]})

district_summary_styled = district_summary.style.format({
"Total Budget": "${:,.0f}", 
"Average Reading Score": "{:.1f}", 
"Average Math Score": "{:.1f}", 
"% Passing Math": "{:.1%}", 
"% Passing Reading": "{:.1%}", 
"Overall Passing Rate": "{:.1%}"})

district_summary_styled

grouped_school = df.set_index('school_name').groupby(['school_name'])
school_type = df1.set_index('school_name')['type']
school_students = grouped_school['Student ID'].count()
school_budget = df1.set_index('school_name')['budget']
school_student_budget = df1.set_index('school_name')['budget']/df1.set_index('school_name')['size']
school_avg_math = grouped_school['math_score'].mean()
school_avg_reading = grouped_school['reading_score'].mean()
school_pass_math = df[df['math_score'] >= 70].groupby('school_name')['Student ID'].count()/school_students 
school_pass_reading = df[df['reading_score'] >= 70].groupby('school_name')['Student ID'].count()/school_students 
school_overall = df[(df['reading_score'] >= 70) & (df['math_score'] >= 70)].groupby('school_name')['Student ID'].count()/school_students 

school_summary = pd.DataFrame({
"School Type" : school_type,
"Total Students" : school_students,
"Total School Budget" : school_budget,
"Per Student Budget" : school_student_budget,
"Average Math Score" : school_avg_math,
"Average Reading Score" : school_avg_reading,
"% Passing Math" : school_pass_math,
"% Passing Reading" : school_pass_reading,
"Overall Passing Rate" : school_overall
})

school_summary_styled = school_summary.style.format({
"Total Students" : "{:,}", 
"Total School Budget" : "${:,}", 
"Per Student Budget" : "${:.0f}",
"Average Math Score" : "{:.1f}", 
"Average Reading Score" : "{:.1f}", 
"% Passing Math" : "{:.1%}", 
"% Passing Reading" : "{:.1%}", 
"Overall Passing Rate" : "{:.1%}"})

school_summary_styled

schools_ranked = school_summary.sort_values("Overall Passing Rate", ascending = False)
top_schools = schools_ranked.head(5)
bottom_schools = schools_ranked.tail(5)
bottom_schools = bottom_schools.sort_values("Overall Passing Rate", ascending = True)

top_schools

bottom_schools

math_9th = df2.loc[df2["grade"] == "9th"].groupby("school_name")["math_score"].mean()
math_10th = df2.loc[df2["grade"] == "10th"].groupby("school_name")["math_score"].mean()
math_11th = df2.loc[df2["grade"] == "11th"].groupby("school_name")["math_score"].mean()
math_12th = df.loc[df2["grade"] == "12th"].groupby("school_name")["math_score"].mean()

math_scores = pd.DataFrame({
"9th" : math_9th,
"10th" : math_10th,
"11th" : math_11th,
"12th" : math_12th
})

math_scores

reading_9th = df2.loc[df2["grade"] == "9th"].groupby("school_name")["reading_score"].mean()
reading_10th = df2.loc[df2["grade"] == "10th"].groupby("school_name")["reading_score"].mean()
reading_11th = df2.loc[df2["grade"] == "11th"].groupby("school_name")["reading_score"].mean()
reading_12th = df.loc[df2["grade"] == "12th"].groupby("school_name")["reading_score"].mean()

reading_scores = pd.DataFrame({
"9th" : reading_9th,
"10th" : reading_10th,
"11th" : reading_11th,
"12th" : reading_12th
})

reading_scores

spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

df['spending_bins'] = pd.cut(df['budget']/df['size'], spending_bins, labels = group_names)
school_spending = df.groupby('spending_bins')

spend_avg_math = school_spending['math_score'].mean()
spend_avg_reading = school_spending['reading_score'].mean()
spend_pass_math = df[df['math_score'] >= 70].groupby('spending_bins')['Student ID'].count()/school_spending['Student ID'].count()
spend_pass_reading = df[df['reading_score'] >= 70].groupby('spending_bins')['Student ID'].count()/school_spending['Student ID'].count()
spend_overall = df[(df['reading_score'] >= 70) & (df['math_score'] >= 70)].groupby('spending_bins')['Student ID'].count()/school_spending['Student ID'].count()
            
school_spending_scores = pd.DataFrame({
"Average Math Score" : spend_avg_math,
"Average Reading Score" : spend_avg_reading,
"% Passing Math" : spend_pass_math,
"% Passing Reading" : spend_pass_reading,
"Overall Passing Rate" : spend_overall    
})

school_spending_scores

size_bins = [0, 1000, 2000, 5000]
size_group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

df['size_bins'] = pd.cut(df['size'], size_bins, labels = size_group_names)
school_size = df.groupby('size_bins')

size_avg_math = school_size['math_score'].mean()
size_avg_reading = school_size['reading_score'].mean()
size_pass_math = df[df['math_score'] >= 70].groupby('size_bins')['Student ID'].count()/school_size['Student ID'].count()
size_pass_reading = df[df['reading_score'] >= 70].groupby('size_bins')['Student ID'].count()/school_size['Student ID'].count()
size_overall = df[(df['reading_score'] >= 70) & (df['math_score'] >= 70)].groupby('size_bins')['Student ID'].count()/school_size['Student ID'].count()
          
school_size_scores = pd.DataFrame({
"Average Math Score" : size_avg_math,
"Average Reading Score" : size_avg_reading,
"% Passing Math" : size_pass_math,
"% Passing Reading" : size_pass_reading,
"Overall Passing Rate" : size_overall       
})

school_size_scores

df = pd.merge(df1, df2, how="outer", on=["school_name", "school_name"])
school_types = df.groupby("type")

type_avg_math = school_types['math_score'].mean()
type_avg_reading = school_types['reading_score'].mean()
type_pass_math = df[df['math_score'] >= 70].groupby('type')['Student ID'].count()/school_types['Student ID'].count()
type_pass_reading = df[df['reading_score'] >= 70].groupby('type')['Student ID'].count()/school_types['Student ID'].count()
type_overall = df[(df['reading_score'] >= 70) & (df['math_score'] >= 70)].groupby('type')['Student ID'].count()/school_types['Student ID'].count()

school_type_scores = pd.DataFrame({
"Average Math Score" : type_avg_math,
"Average Reading Score" : type_avg_reading,
"% Passing Math" : type_pass_math,
"% Passing Reading" : type_pass_reading,
"Overall Passing Rate" : type_overall})

school_type_scores
