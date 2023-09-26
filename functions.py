import pandas as pd
import plotly.express as px 
import streamlit as st

def preprocessing(df, geodf):
    """
    returns a dataframe after operations on the column
    Args:
    df (Pandas.dataframe) : data from https://opendata.reseaux-energies.fr
    geodf (Geopandas.dataframe) : geodataframe with the polygons of metropolitan France's regions from https://france-geojson.gregoiredavid.fr/
    """
    geodf['code'] = geodf['code'].apply(lambda x:int(x))
    df.rename(columns={"Code Région":'code'}, inplace=True)
    merged = geodf.merge(df, on='code').set_index('code')
    merged['Date'] = pd.to_datetime(merged['Date'], utc=False).dt.tz_localize(None)
    merged['month'] = merged['Date'].dt.month
    merged['year'] = merged['Date'].dt.year
    merged['day'] = merged['Date'].dt.day
    merged.drop(columns=['Date','Statut', "Secteur d'activité"], inplace=True)

    return merged[merged['Opérateur']=='GRTgaz']

def df_monthly(merged):
    """
    Returns a dataset where for each year and each month of each region, we have the mean of the consumption

    Args:
    merged (pandas.Dataframe) : dataframe from the function preprocessing
    """
    year_month_df = merged.groupby([merged['year'], merged["month"], 'nom' , merged.index, merged['geometry'], merged['Région']])['Consommation journalière (MWh - PCS 0°C)'].mean()
    return year_month_df.reset_index(['year','month','nom','geometry','Région']).set_geometry("geometry")

def df_yearly(merged):
    """
    Returns a dataset where for each year and each region, we have the mean of the consumption

    Args:
    merged (pandas.Dataframe) : dataframe from the function preprocessing
    """
    year_df = merged.groupby([merged['year'], 'nom' , merged.index, merged['geometry'], merged['Région']])['Consommation journalière (MWh - PCS 0°C)'].mean()
    return year_df.reset_index(['year','nom', 'geometry','Région']).set_geometry("geometry")

def plot_consumption_france(dataframe, list_conditions, hour=None):
    """
    returns a chloropleth map of France where we have the consumption for each region according some conditions

    Args:
    dataframe (pandas.dataframe) : a dataframe with the values of consumption and the polygon of the region
    list_conditions (list of str) : list a conditions to filter the rows of the dataframe
    hour (str or None) : to get consumption at a specifique hour, or daily consumption (hour=None)
    """
    
    df = dataframe.query(''.join(list_conditions))

    if hour is None :
        fig = px.choropleth_mapbox(df,
                    geojson=df.geometry,
                    locations=df.index,
                    color="Consommation journalière (MWh - PCS 0°C)",
                    labels = {'Consommation journalière (MWh - PCS 0°C)' : 'Consommation journalière (MWh)'},
                    mapbox_style="carto-positron",
                    center = {"lat": 46.232192999999995, "lon": 2.209666999999996},
                    zoom=4
                    )
        fig.update_geos(fitbounds="locations", visible=True)
        return fig
       

    else :
        fig = px.choropleth_mapbox(df,
                    geojson=df.geometry,
                    locations=df.index,
                    color=hour+':00',
                    mapbox_style="carto-positron",
                    labels={hour+':00':'Consommation (Mwh)'},
                    center = {"lat": 46.232192999999995, "lon": 2.209666999999996},
                    zoom=3
                    )
        fig.update_geos(fitbounds="locations", visible=True)
        return fig
        

def consumption_part(dataframe, options):
    """
    returns a plotly map figure in the website for the framework Streamlit

    Args:
    dataframe (pandas.dataframe) : a dataframe with the values of consumption and the polygon of the region
    options (str) : 'Tout' --> chloropeth map of the consumption depending on year, month, day and hour
                    'Mensuel' --> chloropeth map of the mean consumption depending on year and month
                    'Annuel' --> chloropeth map of the mean consumption depending on year 
    """

    if options == 'Tout' :
        with st.container():
            col1, col2 = st.columns(2)
            with col2:
                year = st.number_input(label='Année',
                                        min_value=2018,
                                        max_value=2023,
                                        step=1,
                                        value=2018)
                month = st.number_input(label='Mois',
                                        min_value=1,
                                        max_value=12,
                                        step=1,
                                        value=8)

                day = st.number_input(label='Jour',
                                        min_value=1,
                                        max_value=31,
                                        step=1,
                                        value=16)

                hour = st.selectbox('Heure',
                                    ['0'+str(i) for i in range(10)]+[str(i) for i in range(10,24)]+[None])
                
            with col1:
                list_conditions = [f"year=={year} and ",f"month=={month} and ", f"day=={day}" ]
                st.plotly_chart(plot_consumption_france(dataframe = dataframe, 
                                                list_conditions= list_conditions, 
                                                hour=hour))
    elif options == 'Mensuel' :
        with st.container():
            col1, col2 = st.columns(2)
            with col2:
                year = st.number_input(label='Année',
                                        min_value=2018,
                                        max_value=2023,
                                        step=1,
                                        value=2018)
                month = st.number_input(label='Mois',
                                        min_value=1,
                                        max_value=12,
                                        step=1,
                                        value=8)
                
                with col1:

                    list_conditions = [f"year=={year} and ",f"month=={month}"]
                    st.plotly_chart(plot_consumption_france(dataframe = dataframe, 
                                                list_conditions=list_conditions,  
                                                hour=None))
    elif options == 'Annuel' :
        with st.container():
            col1, col2 = st.columns(2)
            with col2:
                year = st.number_input(label='Année',
                                        min_value=2018,
                                        max_value=2023,
                                        step=1,
                                        value=2018)
                with col1:
                    list_conditions = [f"year=={year}"]
                    st.plotly_chart(plot_consumption_france(dataframe = dataframe, 
                                                list_conditions=list_conditions,  
                                                hour=None))


def horizontal_barplots(dataframe, list_conditions, title, hour=None):
    """
    Returns a horizontal barplots representing the consumption for each region 

    Args:
    dataframe (pandas.dataframe) : a dataframe with the values of consumption and the polygon of the region
    list_conditions (list of str) : list a conditions to filter the rows of the dataframe
    title (str) : part of the title of the horizontal barplots
    hour (str or None) : to get consumption at a specifique hour, or daily consumption (hour=None)
    """
    df = dataframe.query(''.join(list_conditions))
    if hour is None :
        fig = px.bar(df, 
                     x="Consommation journalière (MWh - PCS 0°C)", 
                     y="Région",
                     title=f"Consommation journalière de gaz (MWh) pour chaque région --" + title,
                     labels={"Consommation journalière (MWh - PCS 0°C)": 'Consommation journalière (MWh)'}, 
                     orientation='h')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        return fig
        
    else :
        fig = px.bar(df, 
                     x=hour+':00', 
                     y="Région",
                     title = "Consommation de gaz (MWh) pour chaque région -- " + title,
                     labels = {hour+':00':'Consommation (MWh)'}, 
                     orientation='h')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        return fig


def barplots_part(dataframe, options):
    """
    returns a horizontal barplots representing the consumption for each region in the website for the framework Streamlit

    Args:
    dataframe (pandas.dataframe) : a dataframe with the values of consumption and the polygon of the region
    options (str) : 'Tout' --> chloropeth map of the consumption depending on year, month, day and hour
                    'Mensuel' --> chloropeth map of the mean consumption depending on year and month
                    'Annuel' --> chloropeth map of the mean consumption depending on year 
    """
    if options == 'Tout' :
        with st.container():
            col1, col2 = st.columns(2)
            with col2:
                year = st.number_input(label='Année2',
                                        min_value=2018,
                                        max_value=2023,
                                        step=1,
                                        value=2018)
                month = st.number_input(label='Mois2',
                                        min_value=1,
                                        max_value=12,
                                        step=1,
                                        value=8)

                day = st.number_input(label='Jour2',
                                        min_value=1,
                                        max_value=31,
                                        step=1,
                                        value=16)

                hour = st.selectbox('Heure2',
                                    ['0'+str(i) for i in range(10)]+[str(i) for i in range(10,24)]+[None])
                                
            with col1:
                list_conditions = [f"year=={year} and ",f"month=={month} and ", f"day=={day}" ]
                st.plotly_chart(horizontal_barplots(dataframe, 
                                                    list_conditions, 
                                                    title = f"{year}/{month}/{day}  {hour}", 
                                                    hour=hour))
    elif options == 'Mensuel' :
        with st.container():
            col1, col2 = st.columns(2)
            with col2:
                year = st.number_input(label='Année2',
                                        min_value=2018,
                                        max_value=2023,
                                        step=1,
                                        value=2018)
                month = st.number_input(label='Mois2',
                                        min_value=1,
                                        max_value=12,
                                        step=1,
                                        value=8)
                
                with col1:

                    list_conditions = [f"year=={year} and ",f"month=={month}"]
                    st.plotly_chart(horizontal_barplots(dataframe, 
                                                    list_conditions, 
                                                    title = f"{year}/{month}", 
                                                    hour=None))
    elif options == 'Annuel' :
        with st.container():
            col1, col2 = st.columns(2)
            with col2:
                year = st.number_input(label='Année2',
                                        min_value=2018,
                                        max_value=2023,
                                        step=1,
                                        value=2018)
                with col1:
                    list_conditions = [f"year=={year}"]
                    st.plotly_chart(horizontal_barplots(dataframe, 
                                                    list_conditions, 
                                                    title = f"{year}", 
                                                    hour=None))

def pie_charts(dataframe, list_conditions, title, hour=None):
    """
    Returns a pie charts of the consumption for each region 

    Args:
    dataframe (pandas.dataframe) : a dataframe with the values of consumption and the polygon of the region
    list_conditions (list of str) : list a conditions to filter the rows of the dataframe
    title (str) : part of the title of the horizontal barplots
    hour (str or None) : to get consumption at a specifique hour, or daily consumption (hour=None)
    """
    df = dataframe.query(''.join(list_conditions))
    if hour is None :
        fig = px.pie(df, 
                     values="Consommation journalière (MWh - PCS 0°C)", 
                     names="Région",
                     title="Répartition de la consommation selon les Régions" + title)
        return fig
        
    else :
        fig = px.pie(df, 
                     values=hour+':00', 
                     names="Région",
                     title=f"Répartition de la consommation selon la Région " + title)
        return fig
    
def piechart_part(dataframe, options):
    """
    returns a pie charts of the consumption for each region in the website for the framework Streamlit

    Args:
    dataframe (pandas.dataframe) : a dataframe with the values of consumption and the polygon of the region
    options (str) : 'Tout' --> chloropeth map of the consumption depending on year, month, day and hour
                    'Mensuel' --> chloropeth map of the mean consumption depending on year and month
                    'Annuel' --> chloropeth map of the mean consumption depending on year 
    """
    if options == 'Tout' :
        with st.container():
            col1, col2 = st.columns(2)
            with col2:
                year = st.number_input(label='Année3',
                                        min_value=2018,
                                        max_value=2023,
                                        step=1,
                                        value=2018)
                month = st.number_input(label='Mois3',
                                        min_value=1,
                                        max_value=12,
                                        step=1,
                                        value=8)

                day = st.number_input(label='Jour3',
                                        min_value=1,
                                        max_value=31,
                                        step=1,
                                        value=16)

                hour = st.selectbox('Heure3',
                                    ['0'+str(i) for i in range(10)]+[str(i) for i in range(10,24)]+[None])
                                
            with col1:
                list_conditions = [f"year=={year} and ",f"month=={month} and ", f"day=={day}" ]
                st.plotly_chart(pie_charts(dataframe, 
                                                    list_conditions, 
                                                    title = f"{year}/{month}/{day}  {hour}", 
                                                    hour=hour))
    elif options == 'Mensuel' :
        with st.container():
            col1, col2 = st.columns(2)

            with col2:
                year = st.number_input(label='Année3',
                                        min_value=2018,
                                        max_value=2023,
                                        step=1,
                                        value=2018)
                month = st.number_input(label='Mois3',
                                        min_value=1,
                                        max_value=12,
                                        step=1,
                                        value=8)
                
                with col1:
                    list_conditions = [f"year=={year} and ",f"month=={month}"]
                    st.plotly_chart(pie_charts(dataframe, 
                                                    list_conditions, 
                                                    title = f"{year}/{month}", 
                                                    hour=None))
    elif options == 'Annuel' :
        with st.container():
            col1, col2 = st.columns(2)
            with col2:
                year = st.number_input(label='Année3',
                                        min_value=2018,
                                        max_value=2023,
                                        step=1,
                                        value=2018)
                with col1:
                    list_conditions = [f"year=={year}"]
                    st.plotly_chart(pie_charts(dataframe, 
                                                    list_conditions, 
                                                    title = f"{year}", 
                                                    hour=None))