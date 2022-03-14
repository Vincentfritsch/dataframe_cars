import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt

from urllib.error import URLError

def get_data():
    df_cars = pd.read_csv("https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv")
    st.write("### Correlation Map")
    viz_correlation = sns.heatmap(df_cars.corr(), 
								center=0,
								cmap = sns.color_palette("vlag", as_cmap=True)
								)
    st.pyplot(viz_correlation.figure)
    return df_cars.set_index('continent')

try:
    df = get_data()    
    countries = st.multiselect(
        "Choose countries", set(df.index), [" US.", " Europe."]
    )
    categories = st.multiselect(
        "Choose categories", list(df.columns), ["mpg", "year"]
    )
    if not countries:
        st.errors("Please select at least one country.")
    elif not categories:
        st.errors("Please select at least one category.")
        
    else:
        data = df.loc[countries]
        test ="retest"
        st.write(f"### Data from {' and '.join(countries)} with categories \
            {' / '.join(categories)}", data[categories])
        
        if "year" in categories:
            categories.remove('year')
            
        print(categories)
        for cat in categories:
            st.write(f'### Evolution on {cat} thru the years for each country\n')
            chart = (
                alt.Chart(data.reset_index())
                .mark_area(opacity=0.3)
                .encode(
                    x="year:Q",
                    y=cat,
                    color="continent:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )
