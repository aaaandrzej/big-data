# - kazdy rekord ma kod kraju, z każdego wyrzucić kolumnę z innymi nazwami tego miejsca
def filter_positive_population_cities(df):
    return df[(df.population > 0) & (df.featureclass == 'P')]


# - domergować kolumnę z countries info - pełna nazwa kraju po angielsku
def update_df_with_country(df, cc_decoder):
    df.insert(3, column='country', value=df['countrycode'].map(cc_decoder))
    return df


# - w oparciu o listę wszystkich miejsc policzyć ile jest miast w każdym kraju (tabela z nazwą kraju i miasta)
def count_cities_per_country(df, sorted_by_number=False):
    if sorted_by_number:
        return df.groupby('country').count()[['name']].sort_values('name', ascending=False)
    return df.groupby('country').count()[['name']]


# - policzyć histogram dla poszczególnych miast w krajach po ilości mieszkańców (*)
def count_cities_of_provided_population_per_country(df, pop_min, pop_max):
    return df[['country', 'name', 'population']][
        (df.population > pop_min) & (df.population < pop_max)
        ].groupby('country').count()[['population']]


# - znaleźć kraje z najniższą/ najwyższą sumą mieszkańców w swoich miastach (*)
def list_lowest_populated_countries(df, ascending=True):
    if not ascending:
        df.groupby('country').sum()[['population']].sort_values('population', ascending=False)
    return df.groupby('country').sum()[['population']].sort_values('population')
