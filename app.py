# to run use in cmd....streamlit run app.py

import streamlit as st
import pandas as pd
import plotly.express as px

#ui config
st.set_page_config(
    page_title='Pokemon app',
    page_icon="😁",
    layout='wide',
)

#load data
@st.cache_data
def load_data():
    return pd.read_csv("pokemon.csv",index_col='#')

#ui integration
with st.spinner("loading dataset...."):
    df=load_data()
    #st.balloons()

st.title("Pokemon data analytics")
st.subheader("A simple data app to analyse Pokemon data")


st.sidebar.title("Menu")
choice= st.sidebar.radio("options", ["view data","visualization",'Column analysis'])

if choice=='view data':
    st.header("view dataset")
    st.dataframe(df)

    
elif choice=='visulaize data':    
    st.header("visualization")
    cat_cols=df.select_dtypes(include='object').columns.tolist()
    num_cols=df.select_dtypes(include='object').columns.tolist()
    num_cols.remove('Name')
    num_cols.append('Generation')
    num_cols.append('Legendary')
    cat_cols.append('Generation')
    cat_cols.append('Legendary')
    
    
    snum_col= st.sidebar.selectbox("select a numeric colum",num_cols)
    scat_col= st.sidebar.selectbox("select a catagorical colum",cat_cols)
    
    c1,c2= st.columns(2)
    #visualalize numerical column
    fig1=px.histogram(df,
                      x=snum_col,
                      title=f'distribution  of {snum_col}'
                      )
    
    #visualize catagorical column
    fig2= px.pie(df,
                   names=scat_col,
                    title=f'distribution of {scat_col}',
                       hole=0.3
                       )
    
    c1.plotly_chart(fig1)
    c2.plotly_chart(fig2)

    fig3=px.box(df,x=scat_col,y=snum_col,title=f'{snum_col} by {scat_col}')
    st.plotly_chart(fig3)

    fig4=px.treemap(
        df,
        path=['Generation','Type 1'],
        title=f'pokemon type distribution'
    )
    
    st.plotly_chart(fig4)

elif choice=="Column analysis" :
    columns=df.columns.tolist()
    scol=st.sidebar.selectbox("select a column",columns)
    if df[scol].dtype =="object":
        vc=df[scol].value_counts()
        most_common=vc.idxmax()
        c1,c2=st.columns([3,1])
        #visualize
        fig=px.histogram(df,x=scol,title=f'distribution of {scol}') #type of graph funnel or histogram, etc
        c1.plotly_chart(fig)
        
        #value counts
        c2.subheader('total data')
        c2.dataframe(vc,use_container_width=True)
        c2.metric("most common",most_common,int(vc[most_common]))
        c1,c2=st.columns(2)
        fig2=px.pie(df,names=scol,title=f'percentage wise of {scol}',
                    hole=0.3)
        c1.plotly_chart(fig2)
        fig3=px.box(df,x=scol,title=f'{scol} by {scol}')
        c2.plotly_chart(fig3)
        fig4=px.funnel_area(names=vc.index,
                            values=vc.values,
                            title=f'{scol} funnel area',
                            height=600)
        st.plotly_chart(fig4,use_container_width=True)
    else:
        tab1,tab2=st.tabs(["univariate","bivariate"])
        with tab1:
            score=df[scol].describe()
            fig1=px.histogram(df,x=scol,title=f'distribution of  {scol}')
            fig2=px.box(df,x=scol,title=f'{scol} by {scol}')
            c1,c2,c3=st.columns([1,3,3,])
            c1.dataframe(score)
            c2.plotly_chart(fig1)
            c3.plotly_chart(fig2)
        with tab2:
            c1,c2=st.columns(2)
            col2=c1.selectbox("select a column",
                              df.select_dtypes(include='number').columns.tolist())
            color=c2.selectbox("select a color",
                               df.select_dtypes(exclude='number').columns.tolist())
            fig3=px.scatter(df,x=scol,y=col2,
                            color=color,
                            title=f'{scol} vs {col2}', height=600)
        st.plotly_chart(fig3,use_container_width=True)
            
            
    





