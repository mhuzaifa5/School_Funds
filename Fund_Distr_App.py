#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import streamlit as st 


# In[2]:

st.title("\tFunds Distribution Project")
st.header("Objective :\n")
st.write("""Determine how the ed-tech company can have the most impact in improving the current
 education situation specifically by analyzing key constraints and allocating the funds based 
 on them .""")
# Loading the dataframe
text="Note :"
st.subheader(text)
st.write("""  We have separated 250 M dollars due to the reason that there were lot of null values
in the dataset that were imputed using relevant imputation , But it is possible that these imputations may have filled cells with wrong data ,
Thus to cater this issue we saved some amount which can later be distributed among the deserving schools affected from imputation issue.After catering the issue the remaining amount would be equally distributed among all schools. """)

Total_Fund='3B $' 
Distributed='2.75B $'
Remaining ='250M $'
st.write("Total_Fund:",Total_Fund)
st.write('Distributed :',Distributed)
st.write('Remaining :',Remaining)


init_df = pd.read_csv(r"SchoolsData.csv")

with st.expander("1.DATA CLEANING"):
    st.write('''If you want to know how the cleaning process is done , take a look on my notebook by clicking on this link ....
    ''')


# DATA CLEANING :

init_df.drop(['drink_water_type_other','upgrade_primary_year','upgrade_middle_year','upgrade_high_year','upgrade_high_sec_year' ],axis=1,inplace=True)


features = ['school_id','district','tehsil','est_year','school_gender','gender_studying','bldg_condition','classes','functional_classrooms','enrollment','Teachers','NonTeachers','electricity','drink_water','toilets','teachers_toilets']

df=init_df[features]

df['bldg_condition'].fillna('Medium Condition',inplace=True)
df['teachers_toilets'].fillna(0,inplace=True)
df['enrollment'].fillna(np.mean(df['enrollment']),inplace=True)


df.sort_values(by='district', ascending=True,inplace=True)

df['Teachers'].interpolate('nearest',inplace=True)
df['NonTeachers'].interpolate('nearest',inplace=True)


df['Teachers'].fillna(np.mean(df['Teachers']),inplace=True)
df['NonTeachers'].fillna(0,inplace=True)

resources=['electricity','drink_water','toilets','teachers_toilets']

def count_missing_resources(row):
  # Count the number of zeros (missing resources) in the resource columns
  return sum(row[resources] == 0)

# Apply the function to each row and add a new 'lack_resource' column
df['lack_resource'] = df.apply(count_missing_resources, axis=1)

# determining functional classes ratio of each school 
df["fnl_class_ratio"]=df['functional_classrooms']/df['classes']

df['bldg_status_code']=df['bldg_condition'].replace(['Satisfying','Needed Minor Repairing','Medium Condition','Partial Building is Dangerous','Complete Building Needs Repairing','Building Is Dangerous'],[1,1.5,2,2.5,4,5])

df['fnl_class_ratio'].replace(np.inf,0.0,inplace=True)

df['fnl_class_ratio'].fillna(0,inplace=True)


with st.expander("2.EXPLORATORY DATA ANALYSIS "):
    st.write("Here are some visuals to give you know-how about the data . \n")
    
    st.text("1st Plot\n")
    district_counts = df.groupby('district')['school_id'].count()
    plt.figure(figsize=(15,7))
    # Extract district names and counts for plotting
    districts = district_counts.index.to_numpy()  # Get district names as NumPy array
    counts = district_counts.to_numpy()  # Get counts as NumPy array
    
    # Create the bar chart
    plt.bar(districts, counts)
    for i, v in enumerate(counts):
        y_val = v + 0.1  # Add a small offset for better visibility
        plt.text(districts[i], v+0.1, int(v), ha='center', va='bottom', fontsize=9) 
    
    # Add labels and title
    plt.xlabel('District')
    plt.ylabel('Number of Schools')
    plt.xticks(rotation=75)
    plt.title('Number of Schools by District')
    
    # Display the plot
    st.pyplot(plt)

    st.text("2nd Plot\n")
    fig, ax = plt.subplots()  # Create a single figure with an Axes object
    plt.pie(df.groupby("school_gender")["enrollment"].sum(), autopct='%1.1f%%', colors=["blue", "orange"])  # Plot data on the Axes
    
    # Add title and legend within the Axes object
    ax.set_title('Schools Distribution Based on Genders')
    ax.legend(labels=['Female', 'Male'])
    
    # Display the plot in Streamlit
    st.pyplot(fig)  # Pass the entire figure object (fig)
    
    
    st.text("3rd Plot\n")
    district_counts = df.groupby('district')['enrollment'].sum()
    plt.figure(figsize=(17,7))
    # Extract district names and counts for plotting
    districts = district_counts.index.to_numpy()  # Get district names as NumPy array
    counts = district_counts.to_numpy()  # Get counts as NumPy array
    
    # Create the bar chart
    plt.bar(districts, counts)
    for i, v in enumerate(counts):
        y_val = v + 0.1  # Add a small offset for better visibility
        plt.text(districts[i], v+0.1, int(v), ha='center', va='bottom', fontsize=6.5) 
    
    # Add labels and title
    plt.xlabel('District')
    plt.ylabel('Number of Enrollments')
    plt.xticks(rotation=75)
    plt.title('Number of Enrollments by District')
    
    # Display the plotBlockingIOError
    st.pyplot(plt)

    st.text("4th Plot\n")
    bldg_cond = df["bldg_condition"].value_counts()
    condition=bldg_cond.index.to_numpy()
    plt.figure(figsize=(15,7))
    
    counts = bldg_cond.to_numpy()  # Get counts as NumPy array
    
    # # Create the bar chart
    plt.barh(condition, counts)
    for i, count in enumerate(counts):
        plt.annotate(str(count), xy=(count, condition[i]), ha='left', va='center')

    # Add labels and title
    plt.xlabel('No of Buidings')
    plt.ylabel('Buildings Condition')
    plt.title('Distribution of Buildings  Conditions')
    plt.grid()
    
    
    st.pyplot(plt)



    st.text("5th Plot\n")
    gender_studying = df['gender_studying'].value_counts()
    plt.figure(figsize=(8, 6))
    gender_studying.plot(kind='bar')
    
    # Add count values on top of the bars
    for i, count in enumerate(gender_studying):
        plt.text(i, count, str(count), ha='center', va='bottom')
    
    plt.title("Distribution of Gender Specific Schools")
    plt.xlabel("Gender")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    st.pyplot(plt)


    st.text("6th Plot\n")
    bldg_cond = df["lack_resource"].value_counts()
    condition=bldg_cond.index.to_numpy()
    plt.figure(figsize=(15,7))
    
    counts = bldg_cond.to_numpy()  # Get counts as NumPy array
    
    # # Create the bar chart
    plt.bar(condition, counts)
    for i, v in enumerate(counts):  # Loop through bars and counts
      plt.text(i, v + 0.1, str(v), ha='center', va='bottom', fontsize=12)
    # Add labels and title
    plt.xlabel('No of Resources')
    plt.ylabel('Count of Lackness')
    plt.xticks(rotation=75)
    plt.title('Distribution of Resource Lackness')
    plt.grid()
    
   
    st.pyplot(plt)


def both_gender_fund(row):
        if row['gender_studying']=='Both':
            return 6098
        else :
            return 0

    # funds for building condition       
def calculate_bldg_fund(row):
    if row['bldg_status_code'] == 1.0:
        return 8500
    elif row['bldg_status_code'] == 1.5:
        return 15000     
    elif row['bldg_status_code'] == 2.0:
        return 25000
    elif row['bldg_status_code'] == 2.5:
        return 50237.9
    elif row['bldg_status_code'] == 4.0:
        return 75420
    elif row['bldg_status_code'] == 5.0:
        return 150000

# function to allocate resource fund 
def resources_fund(row):
    if row['lack_resource']==0:
        return 0
    elif row['lack_resource']==1:
        return 11957
    elif row['lack_resource']==2:
        return 2*11957
    elif row['lack_resource']==3:
        return 3*11957    
    elif row['lack_resource']==4:
        return 4*11957    
def classes_fund(row):
    if (row['fnl_class_ratio']<=10.2) & (row['fnl_class_ratio']>=0.75):
        return 3069.9
    elif (row['fnl_class_ratio']<0.75) & (row['fnl_class_ratio']>=0.50):
        return 2*3069.9
    elif (row['fnl_class_ratio']<0.50) & (row['fnl_class_ratio']>=0.25):
        return 3*3069.9
    elif (row['fnl_class_ratio']<0.25) & (row['fnl_class_ratio']>=0.0):
        return 4*3069.9    
# funds for old buildings 
def old_bldg_fund(row):
    if row['building_age']>=50:
        return 4274
    elif row['building_age']<50:
        return 0

with st.expander("3.ALLOCATED FUNDS DATASET ",expanded=True):
    st.write("Dataset showing the Funds Allocated to Schools")
    
    df['building_age']=2024-df['est_year']
    
    formula =  (df.apply(old_bldg_fund, axis=1)) +20750 + (df['enrollment']*16.7) + (df['Teachers']*204.1)+(df['NonTeachers']*196)+(df.apply(calculate_bldg_fund, axis=1))+(df.apply(both_gender_fund, axis=1))+(df.apply(resources_fund, axis=1))+(df.apply(classes_fund, axis=1))
   
    df['funds']=formula
    st.dataframe(df)
 

with st.expander("4. DETAILS OF ALLOCATED FUNDS ",expanded=True):
    
    id=int(st.text_input("Enter the school id :"))
    
    if id in df['school_id'].values:
        new=(df[df['school_id'] == id])
        st.write(new)

        
        # variables for details of funds allocation
        base_fund=20750
        enrollment_alloc=int(new['enrollment'])*16.7
        teacher_alloc=int(new['Teachers'])*204.1
        non_teacher_alloc=int(new['NonTeachers'])*196
        bldg_age_alloc=float(new.apply(old_bldg_fund, axis=1))
        bldg_alloc=float(new.apply(calculate_bldg_fund, axis=1))
        classes_alloc=float(new.apply(classes_fund, axis=1))
        resources_alloc=float(new.apply(resources_fund, axis=1))
        dual_gender=float(new.apply(both_gender_fund, axis=1))
        class_fnl_alloc =float(new.apply(classes_fund, axis=1))


        st.write("Here are the details of fund alloted :")
        
        col1, col2, col3 = st.columns(3)  # Create three columns
      
        col1.write(f"Base Fund :{base_fund}")
        col2.write(f"Enrollment Fund :{enrollment_alloc}")
        col3.write(f"Teacher Fund Portion :{teacher_alloc}")
        
        col1, col2, col3 = st.columns(3)  
        col1.write(f"Non Teachers Fund Portion :{non_teacher_alloc}")
        col2.write(f"Resources Lackness Fund : {resources_alloc}")
        col3.write(f"Dual Gender School Fund :{dual_gender}")

        col1, col2,col3 = st.columns(3)  
        col2.write(f"Building Old Age Fund(>50) :{bldg_age_alloc}")
        col1.write(f"Building Renovation Fund :{bldg_alloc}") 
        col3.write(f"Class Resources Fund :{class_fnl_alloc}")

        total= base_fund + enrollment_alloc + teacher_alloc + non_teacher_alloc + bldg_age_alloc + bldg_alloc + classes_alloc + resources_alloc + dual_gender

        st.write("Total Fund :",total)
    else:
        st.text(f"No school with id {id} found")
       

   