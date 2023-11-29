import mysql.connector
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

#sql connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nivya@123",
    database="phonepe",
    autocommit=True)
cursor = mydb.cursor()     

#configuring streamlit page
st.set_page_config(layout='wide')

# Title
st.header(':violet[Phonepe Pulse Data Visualization ]')

# Selection option
option = st.radio('**Select your option**',('All India', 'State wise','top and least category'),horizontal=True)
if option=="All India":
    tab1,tab2=st.tabs(["Transaction","User"])
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            trans_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='trans_year')
        with col2:
            trans_quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='trans_quarter')
        with col3:
            trans_type = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others'),key='trans_type')
        #query to fetch transaction amount
        cursor.execute("select State,transaction_amount from aggregated_transaction where Year= %s and Quarter = %s and transaction_name = %s;",(trans_year,trans_quarter,trans_type))
        trans_res=cursor.fetchall()
        df_trans = pd.DataFrame(trans_res, columns=['State', 'Transaction_amount'])

    #choropleth india map for transaction
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        #converting url to json format
        data=json.loads(response.content)
        state_names = []
        state_names.sort()
        #iterating state name from geojson file and sorting 
        for feature in data['features']:
            state_names.append(feature['properties']['ST_NM'])
        df_state_names=pd.DataFrame(state_names, columns=['State'])
        #dropping the state column from df since state name not matched according to geojson file
        df_trans = df_trans.drop(columns=['State'])
        #combining both dataframe to pass in choropleth map
        df_combined = pd.concat([df_state_names, df_trans], axis=1)
        fig = px.choropleth(
            df_combined,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            width=1000,
            height=800,
            color='Transaction_amount',
            color_continuous_scale='purples',
            title='All India Transaction Analysis'
        )

        fig.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig,use_container_width=True)

    #all india analysis using bar chart
        fig_bar = px.bar(df_combined, x='State',y='Transaction_amount',color_discrete_sequence = ['#9467BD'], text_auto='.2s',title= "All India Analysis On Transaction Amount")
        st.plotly_chart(fig_bar,use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            user_years=st.selectbox("**Select Year**",('2018','2019','2020','2021','2022','2023'),key='user_years')
        with col2:
            user_quarter=st.selectbox("**Select Quarter**",('1','2','3','4'),key='user_quarter')
        
        #all india user query
        cursor.execute("select State,sum(transaction_count) as transaction_count from aggregated_transaction where Year=%s and Quarter=%s group by State;",(user_years,user_quarter))
        user_res=cursor.fetchall()
        df_user=pd.DataFrame(user_res, columns=['State','transaction_count'])

        #choropleth india map for users
        url_path="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response1=requests.get(url_path)
        #converting url to json format
        data1=json.loads(response1.content)
        state=[]
        state.sort()
        #iterating state name from geojson file and sorting 
        for i in data1['features']:
            state.append(i['properties']['ST_NM']) 
        state_df=pd.DataFrame(state,columns=['States'])
        #dropping the state column from df since state name not matched according to geojson file
        df_user=df_user.drop(['State'],axis=1)
        #combining both dataframe to pass in choropleth map
        df_merged=pd.concat([state_df,df_user], axis=1)
        fig1 = px.choropleth(
            df_merged,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='transaction_count',
            color_continuous_scale='purples',
            width=1000,
            height=800,
            title='All India Registered Users'
            )

        fig1.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig1,use_container_width=True)

        #all india user analysis using bar 

        fig_bar1 = px.bar(df_merged, x='States',y='transaction_count',color_discrete_sequence = ['#9467BD'],text_auto='.2s',title= "All India Analysis On UserCount")
        st.plotly_chart(fig_bar1,use_container_width=True)

elif option=="State wise":
    tab1,tab2=st.tabs(["Transaction","User"])
    with tab1:
        col1, col2,col3 = st.columns(3)
        with col1:
            state=st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='state')
        with col2:
            year=st.selectbox('**select year**',('2018','2019','2020','2021','2022','2023'),key='year')
        with col3:
            quarter=st.selectbox('**select quarter**',('1','2','3','4'),key='quarter')

        #joining two tables

        query='''select transaction_name,transaction_amount,avg(transaction_amount) as average_transaction 
        from aggregated_transaction 
        where State = %s and Year=%s and Quarter=%s group by State,transaction_name,transaction_amount'''

        cursor.execute(query,(state,year,quarter))
        res=cursor.fetchall()
        df=pd.DataFrame(res,columns=['Transaction_Type','Transaction_amount','Average_Transaction'])

        fig_bar2 = px.bar(df, x='Transaction_Type',y='Transaction_amount',color='Transaction_amount',color_continuous_scale = 'magma',text_auto='.2s',title= "State Wise Transaction Analysis",height=500)
        st.plotly_chart(fig_bar2,use_container_width=True)
    
    with tab2:
        col1, col2,col3 = st.columns(3)
        with col1:
            U_state=st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='U_state')
        with col2:
            U_year=st.selectbox('**select year**',('2018','2019','2020','2021','2022','2023'),key='U_year')
        with col3:
            U_quarter=st.selectbox('**select quarter**',('1','2','3','4'),key='U_quarter')
        query2='''select Brand,Transaction_Count, avg(Transaction_Count) as Average_count
        from aggregated_users
        where State = %s and Year=%s and Quarter=%s group by State,Brand,Transaction_Count'''

        cursor.execute(query2,(U_state,U_year,U_quarter))
        res1=cursor.fetchall()
        df1=pd.DataFrame(res1, columns=['Brand','Transaction_Count','Average_count'])

        fig_bar3=px.bar(df1,x='Brand',y='Transaction_Count',color='Transaction_Count',color_continuous_scale='magma',text_auto='.2s',title= "State Wise User Count Analysis",height=500)
        st.plotly_chart(fig_bar3,use_container_width=True)  
else:
    tab1,tab2=st.tabs(['Trasansaction','User'])
    with tab1:
        year_trans=st.selectbox('**Select Year**',('2018','2019','2020','2021','2022','2023'),key='year_trans')

        cursor.execute("select State,sum(transaction_amount) as Transaction_amount from aggregated_transaction where Year =%s group by State order by Transaction_amount limit 10;",(year_trans,))
        max_trans=cursor.fetchall()
        df_max_trans=pd.DataFrame(max_trans,columns=['State','Max_Transaction_Amount'])
     

        fig_trans=px.pie(df_max_trans,names='State',values='Max_Transaction_Amount', title='Top 10 Maximum Transaction Amount')
        st.plotly_chart(fig_trans,use_container_width=True)

        cursor.execute("select State,sum(transaction_amount) as Transaction_amount from aggregated_transaction where Year =%s group by State order by Transaction_amount desc limit 10;",(year_trans,))
        least_trans=cursor.fetchall()
        df_least_trans=pd.DataFrame(least_trans,columns=['State','Transaction_Amount'])
       

        fig_trans_least=px.pie(df_least_trans,names='State',values='Transaction_Amount',title='Least 10 Transaction Amount')
        st.plotly_chart(fig_trans_least,use_container_width=True)

    with tab2:

        year_user=st.selectbox('**Select Year**',('2018','2019','2020','2021','2022','2023'),key='year_user')

        cursor.execute("select State,sum(Transaction_Count) as Transaction_Count from aggregated_users where Year =%s group by State order by Transaction_Count limit 10;",(year_user,))
        max_user=cursor.fetchall()
        df_max_user=pd.DataFrame(max_user,columns=['State','Max_Transaction_Count'])

        fig_user=px.pie(df_max_user,names='State',values='Max_Transaction_Count', title='Top 10 Maximum Transaction Count')
        st.plotly_chart(fig_user,use_container_width=True)

        cursor.execute("select State,sum(Transaction_Count) as Transaction_Count from aggregated_users where Year =%s group by State order by Transaction_Count desc limit 10;",(year_user,))
        least_user=cursor.fetchall()
        df_least_user=pd.DataFrame(least_user,columns=['State','Transaction_Count'])

        fig_least_user=px.pie(df_least_user,names='State',values='Transaction_Count', title='Least 10 Transaction Count')
        st.plotly_chart(fig_least_user,use_container_width=True)

        cursor.execute("select State,sum(Registered_User) as Registered_User from map_user where Year =%s group by State order by Registered_User limit 10;",(year_user,))
        max_reg_user=cursor.fetchall()
        df_max_reg_user=pd.DataFrame(max_reg_user,columns=['State','Max_Registered_User'])

        fig_reg_user=px.pie(df_max_reg_user,names='State',values='Max_Registered_User', title='Top 10 Registered User Count')
        st.plotly_chart(fig_reg_user,use_container_width=True)

        cursor.execute("select State,sum(Registered_User) as Registered_User from map_user where Year =%s group by State order by Registered_User desc limit 10;",(year_user,))
        least_reg_user=cursor.fetchall()
        df_least_reg_user=pd.DataFrame(least_reg_user,columns=['State','Registered_User'])

        fig_reg_user1=px.pie(df_least_reg_user,names='State',values='Registered_User', title='Least 10 Registered User Count')
        st.plotly_chart(fig_reg_user1,use_container_width=True)










    

    

                                 
