# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 13:56:36 2022

@author: oshav
"""
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

#revenue_by_family=pd.pivot_table(data=orders_compl,index='Snack_type',values=['total','discount','order_id'],aggfunc={'total':'sum','discount':'sum','order_id':'count'},margins=True)
orders=pd.read_csv(r'/app/projects/Monthly Orders for snacks.csv') 
orders['datetime']=pd.to_datetime(orders['created_at'])
orders['year']=pd.DatetimeIndex(orders['datetime']).year
orders['month']=pd.DatetimeIndex(orders['datetime']).month

#non_num_cols = orders.select_dtypes(include=object).columns
#column = st.selectbox("Select column to generate wordcloud", non_num_cols)
#column = orders['order_id']
 
# Build table
#st.markdown('***Counts in selected column for generating WordCloud***')
#unique_values = column.value_counts()
#st.write(unique_values)
#defining snack type selebox
families=list(orders["Snack_type"].unique())
families.append("All")


snack_type = st.sidebar.selectbox("Select a Snack Type",families)
year = st.sidebar.selectbox("Year",("2021","2020"))
month = st.sidebar.selectbox("Month",(orders['month'].unique()))
df_family_compl=orders[(orders['status']=='Completed')&(orders["Snack_type"]==snack_type)&(orders["year"]==float(year))&(orders["month"]==float(month))]
df_compl=orders[(orders['status']=='Completed')&(orders["year"]==float(year))&(orders["month"]==float(month))]
missed_opportunity=orders[(orders['status']!='Completed')&(orders["year"]==float(year))&(orders["month"]==float(month))]
missed_revenue=missed_opportunity['total'].sum()

PoS=list(orders["name"].unique())
type(PoS)
PoS.append("All")
st.title("Finance and operational metrics")
if snack_type=="All":
    revenue_metric=df_compl['total'].sum()
    orders_qty=df_compl['order_id'].value_counts().sum()
    Avg_Order=df_compl['total'].mean()
    Discount_rate=(df_compl['discount'].sum()/df_compl['total'].sum())
    avg_rating=df_compl['rating'].mean()
    
else:
    revenue_metric=df_family_compl['total'].sum()
    orders_qty=df_family_compl['order_id'].value_counts().sum()
    Avg_Order=round(df_family_compl['total'].mean(),0)
    Discount_rate=df_family_compl['discount'].sum()/df_compl['total'].sum()
    avg_rating=round(df_family_compl['rating'].mean(),1)



print(orders_qty)
col1,col2,col3,col4,col5,col20=st.columns(6)
col1.metric(label="Monthly Revenue",value=str(float(round(revenue_metric/1000,0)))+'K')
col2.metric(label="Nb of orders",value=str(float(orders_qty)))
col3.metric(label="Avg Order (€)",value=round(Avg_Order,0))
col4.metric(label="Discount rate",value='{:.1%}'.format(Discount_rate))
col5.metric(label="Avg rating",value=round(avg_rating,1))
col20.metric(label="Missed opportunity",value=str(float(round(missed_opportunity["total"].sum()/1000,0)))+'K')

piechart_base1=df_compl.pivot_table(index=['name'],values=['total'],aggfunc='sum',margins=False)


container1 = st.container()
col6, col7 = st.columns(2)

with container1:
    with col6:
        st.markdown("Average monthly revenue")
        chart_data3 = orders.pivot_table(index='month',values="total",aggfunc='mean').dropna()
        st.line_chart(chart_data3)
    
    with col7:
        st.markdown("Total monthly revenue")
        chart_data = orders.pivot_table(index='month',values="total",aggfunc='sum')
        st.line_chart(chart_data)

container2 = st.container()
col8, col9 = st.columns(2)
with container2:
    with col8:
        st.markdown("Nb. of Orders per snack type")
        chart_data2 = df_compl.pivot_table(index='Snack_type',values="order_id",aggfunc='count')
        st.bar_chart(chart_data2)
    with col9:
        st.markdown("Revenue per Point of Sail")
       #chart_data4 = orders.pivot_table(index='accepted_at',values="total",aggfunc='count')
       #st.line_chart(chart_data4)
       
        #fig,ax6= plt.subplots(figsize=(6,4))
        #ax6=plt.pie(piechart_base1['total'],colors=colors, autopct="%1.0f%%",shadow=False, startangle=90,textprops={'size':'3','color':'grey','weight':'bold'},wedgeprops = {'linewidth': 3},pctdistance=0.8)
        #plt.show()
        #st.pyplot()
        chart_data6 =df_compl.pivot_table(index='Snack_type',values="total",aggfunc='mean')
        st.bar_chart(chart_data6)
col10,col11=st.columns(2)
with col10:
    st.markdown("Split by order status")
    colors = ["wheat", "lavender", "lightblue",'#FE53BB','thistle','paleturquoise','palevioletred']
    fig,ax6= plt.subplots(figsize=(5,3))
    piechart_base2=orders.pivot_table(index='status',values='total',aggfunc='sum')
    ax6=plt.pie(piechart_base2['total'],colors=colors,labels=piechart_base2.index, autopct="%1.0f%%",shadow=False, startangle=90,textprops={'size':'8','color':'grey','weight':'bold'},wedgeprops = {'linewidth': 3},pctdistance=0.8)
    plt.show()
    st.pyplot()
with col11:
      st.markdown("Revenue per Point of Sail")
       #chart_data4 = orders.pivot_table(index='accepted_at',values="total",aggfunc='count')
       #st.line_chart(chart_data4)
       
      
        #fig,ax6= plt.subplots(figsize=(6,4))
        #ax6=plt.pie(piechart_base1['total'],colors=colors, autopct="%1.0f%%",shadow=False, startangle=90,textprops={'size':'3','color':'grey','weight':'bold'},wedgeprops = {'linewidth': 3},pctdistance=0.8)
        #plt.show()
        #st.pyplot()
      chart_data5 = df_compl.pivot_table(index='name',values="total",aggfunc='sum')
      st.bar_chart(chart_data5)

