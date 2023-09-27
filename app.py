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

 
