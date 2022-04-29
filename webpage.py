import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from mpl_toolkits import mplot3d

sns.set()
# the write function takes markdown as input if you use """   """
df=pd.DataFrame()
def customer_segmentation(df):
    age_18_25=df.Age[(df.Age<=25) & (df.Age>=18)]
    age_26_30=df.Age[(df.Age<=30) & (df.Age>=26)]
    age_31_35=df.Age[(df.Age<=35) & (df.Age>=31)]
    age_36_40=df.Age[(df.Age<=40) & (df.Age>=41)]
    age_46_50=df.Age[(df.Age<=50) & (df.Age>=46)]
    age_51_55=df.Age[(df.Age<=55) & (df.Age>=51)]
    age_56_60=df.Age[(df.Age<=60) & (df.Age>=56)]
    age_61_65=df.Age[(df.Age<=65) & (df.Age>=61)]
    age_66_70=df.Age[(df.Age<=70) & (df.Age>=66)]
    age_71_75=df.Age[(df.Age<=75) & (df.Age>=71)]
    age_76_80=df.Age[(df.Age<=80) & (df.Age>=76)]
    age_81_85=df.Age[(df.Age<=85) & (df.Age>=81)]
    age_86_90=df.Age[(df.Age<=90) & (df.Age>=86)]
    age_91_95=df.Age[(df.Age<=95) & (df.Age>=90)]
    age_96_100=df.Age[(df.Age<=100) & (df.Age>=96)]

    agex=np.array(['18-25','26-30','31-35','36-40','41-50','50-55','56-60','61-65','66-70','71-75','76-80','81-85','86-90','91-95','96-100'])
    agey=np.array([len(age_18_25.values),len(age_26_30.values),len(age_31_35.values),len(age_36_40.values),len(age_46_50.values),len(age_51_55.values),len(age_56_60.values),len(age_61_65.values),len(age_66_70.values),len(age_71_75.values),len(age_76_80.values),len(age_81_85.values),len(age_86_90.values),len(age_91_95.values),len(age_96_100.values)])
    X1=df.loc[:,['Age','Annual Income (k$)','Spending Score (1-100)']]
    
    fig = plt.figure(figsize = (10, 5))
    sns.distplot(df['Spending Score (1-100)'])
    st.pyplot(fig)

    fig = plt.figure(figsize = (10, 5))
    sns.distplot(df['Age'])
    st.pyplot(fig)

    fig = plt.figure(figsize = (10, 5))
    sns.distplot(df['Annual Income (k$)'])
    st.pyplot(fig)

    fig = plt.figure(figsize = (15, 5))
    sns.histplot(data=df,x='Annual Income (k$)',hue='Age')
    st.pyplot(fig)

    fig=sns.lmplot(data=df,x='Age',y='Spending Score (1-100)')
    st.pyplot(fig)
    
    fig = plt.figure(figsize = (10, 5))
    sns.countplot(data=df,x='Gender')
    st.pyplot(fig)

    fig = plt.figure(figsize = (10, 5))
    sns.histplot(data=df,x='Age',hue='Gender')
    st.pyplot(fig)

    
    fig=sns.lmplot(data=df,x='Spending Score (1-100)',y='Annual Income (k$)',hue='Gender')
    st.pyplot(fig)
    #checking for the ideal number of clusters
    kmlist=[]
    for k in range(1,15):
        k_means=KMeans(n_clusters=k,init='k-means++')
        k_means.fit(X1)
        kmlist.append(k_means.inertia_)

    fig = plt.figure(figsize = (10, 5))
    plt.plot(range(1,15),kmlist)
    plt.xlabel("Number of clusters")
    plt.ylabel("Variance")
    st.pyplot(fig)
    plt.show()
    st.write("""
    Select a number from where there is no significant variance
    """)
    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter number of clusters')
        submit_button = st.form_submit_button(label='Submit')
    
    if submit_button:
        k_means=KMeans(n_clusters=int(text_input))
        l=k_means.fit_predict(X1)
        print(X1)
        df['label']=l
        fig = plt.figure(figsize = (10, 5))
        ax=plt.axes(projection='3d')
        ax.scatter(df.Age[df.label==0],df['Annual Income (k$)'][df.label==0],df['Spending Score (1-100)'][df.label==0],c='red')
        ax.scatter(df.Age[df.label==1],df['Annual Income (k$)'][df.label==1],df['Spending Score (1-100)'][df.label==1],c='blue')
        ax.scatter(df.Age[df.label==2],df['Annual Income (k$)'][df.label==2],df['Spending Score (1-100)'][df.label==2],c='yellow')
        ax.scatter(df.Age[df.label==3],df['Annual Income (k$)'][df.label==3],df['Spending Score (1-100)'][df.label==3],c='green')
        ax.scatter(df.Age[df.label==4],df['Annual Income (k$)'][df.label==4],df['Spending Score (1-100)'][df.label==4],c='purple')
        plt.xlabel('Age')
        plt.ylabel('Annual Income (k$)')
        ax.set_zlabel('Spending Score (1-100')
        st.pyplot(fig)

plt.show()
st.write("""
# Customer Segmentation System
""")

try:
    type_of_file=st.radio(

        'Select Type of File',
        ('Excel(.xlsx)','Comma Seprated Value(.csv)')
    )
    label="Enter the file"
    file=st.file_uploader(label)
except ValueError:
    pass

if type_of_file=='Excel(.xlsx)':
    try:
        df=pd.read_excel(file)
    except ValueError:
        st.write("""
        ## Enter an excel file
        """)
        
elif type_of_file=='Comma Seprated Value(.csv)':
    try:   
        df=pd.read_csv(file)

    except ValueError:
        st.write("""
        ## Enter an CSV file
        """)

try:
    customer_segmentation(df)
except AttributeError:
    pass

