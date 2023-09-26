import streamlit as st
import pandas as pd
import geopandas as gpd
import functions
st.set_page_config(layout="wide")

st.title('Consommation quotidienne de gaz par région en France métropolitaine')

df = pd.read_csv('courbe-de-charge-eldgrd-regional-grtgaz-terega.csv', sep=';')
map_geo = gpd.read_file("regions.geojson")
merged_df = functions.preprocessing(df, map_geo)
df_monthly = functions.df_monthly(merged_df)
df_yearly = functions.df_yearly(merged_df)

# with st.container():
#     col1, col2 = st.columns(2)

#     with col2:
#         year = st.number_input(label='Année',
#                                 min_value=2018,
#                                 max_value=2023,
#                                 step=1,
#                                 value=2018)
#         month = st.number_input(label='Mois',
#                                 min_value=1,
#                                 max_value=12,
#                                 step=1,
#                                 value=8)

#         day = st.number_input(label='Jour',
#                                 min_value=1,
#                                 max_value=31,
#                                 step=1,
#                                 value=16)

#         hour = st.selectbox('Heure',
#                             ['0'+str(i) for i in range(10)]+[str(i) for i in range(10,24)]+[None])
                           

#     with col1:
#         st.plotly_chart(functions.plot_consumption_france(dataframe = merged_df, 
#                                           year = year, 
#                                           month = month, 
#                                           day=day, 
#                                           hour=hour))

options = st.selectbox('options',
                   ['Tout', 'Mensuel', 'Annuel'])
if options == 'Tout' :
    functions.consumption_part(dataframe=merged_df,
                            options='Tout')
elif options == 'Mensuel' :
    functions.consumption_part(dataframe=df_monthly,
                            options='Mensuel')
elif options == 'Annuel' :
    functions.consumption_part(dataframe=df_yearly,
                            options='Annuel')
    
options2 = st.selectbox('options2',
                   ['Tout', 'Mensuel', 'Annuel'])
if options2 == 'Tout' :
    functions.barplots_part(dataframe=merged_df,
                            options='Tout')
elif options2 == 'Mensuel' :
    functions.barplots_part(dataframe=df_monthly,
                            options='Mensuel')
elif options2 == 'Annuel' :
    functions.barplots_part(dataframe=df_yearly,
                            options='Annuel')
    
options3 = st.selectbox('options3',
                   ['Tout', 'Mensuel', 'Annuel'])
if options3 == 'Tout' :
    functions.piechart_part(dataframe=merged_df,
                            options='Tout')
elif options3 == 'Mensuel' :
    functions.piechart_part(dataframe=df_monthly,
                            options='Mensuel')
elif options3 == 'Annuel' :
    functions.piechart_part(dataframe=df_yearly,
                            options='Annuel')


# with st.container():
#     col1, col2 = st.columns(2)

#     with col2:
#         year = st.number_input(label='Année2',
#                                 min_value=2018,
#                                 max_value=2023,
#                                 step=1,
#                                 value=2018)
#         month = st.number_input(label='Mois2',
#                                 min_value=1,
#                                 max_value=12,
#                                 step=1,
#                                 value=8)

#         day = st.number_input(label='Jour2',
#                                 min_value=1,
#                                 max_value=31,
#                                 step=1,
#                                 value=16)

#         hour = st.selectbox('Heure2',
#                             ['0'+str(i) for i in range(10)]+[str(i) for i in range(10,24)]+[None])
                           

#     with col1:
#         st.plotly_chart(functions.horizontal_barplots(dataframe = merged_df, 
#                                           year = year, 
#                                           month = month, 
#                                           day=day, 
#                                           hour=hour))       

# with st.container():
#     col1, col2 = st.columns(2)

#     with col2:
#         year = st.number_input(label='Année3',
#                                 min_value=2018,
#                                 max_value=2023,
#                                 step=1,
#                                 value=2018)
#         month = st.number_input(label='Mois3',
#                                 min_value=1,
#                                 max_value=12,
#                                 step=1,
#                                 value=8)

#         day = st.number_input(label='Jour3',
#                                 min_value=1,
#                                 max_value=31,
#                                 step=1,
#                                 value=16)

#         hour = st.selectbox('Heure3',
#                             ['0'+str(i) for i in range(10)]+[str(i) for i in range(10,24)]+[None])
                           

#     with col1:
#         st.plotly_chart(functions.pie_charts(dataframe = merged_df, 
#                                           year = year, 
#                                           month = month, 
#                                           day=day, 
#                                           hour=hour))       
