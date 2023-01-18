import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


general_stats_df = pd.DataFrame(columns=['Random'])
country_vaccines_df = pd.DataFrame(columns=['Random'])



# Extracting Data
filename = "owid-covid-data.csv"
df = pd.read_csv(filename)
filename2 = "vaccine_locations.csv"
df_vaccine_locations = pd.read_csv(filename2)


df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d')
df['location'] = df['location'].str.lower()

df_vaccine_locations['location'] = df_vaccine_locations['location'].str.lower()

# General DataFrame for a country
general_stats_df = df[["location", "date", "total_cases", "new_cases", "total_deaths", "new_deaths", "total_tests", "total_vaccinations", "positive_rate"]]

# General DataFrame for a country's vaccines
country_vaccines_df = df_vaccine_locations[["location", "vaccines"]]



def get_general_stats(country_name):
  country_name = country_name.lower()
  country_stats = general_stats_df[(general_stats_df['location'] == country_name) & (general_stats_df['date'] == '2021-04-30')]

  if (country_stats.empty):
    return("Stats not available for this country")

  country_stats = country_stats.replace(np.nan, 'Stats not available', regex=True)

  ret_country_name = country_stats.location.to_string(index=False).title()
  date = country_stats.date.to_string(index=False)
  total_cases = country_stats.total_cases.to_string(index=False)
  new_cases = country_stats.new_cases.to_string(index=False)
  total_deaths = country_stats.total_deaths.to_string(index=False)
  new_deaths = country_stats.new_deaths.to_string(index=False)
  total_tests = country_stats.total_tests.to_string(index=False)
  total_vaccinations = country_stats.total_vaccinations.to_string(index=False)
  positive_rate = country_stats.positive_rate.to_string(index=False)

  ret_string = ("**Country: **" + ret_country_name + "\n" + 
                "**Stats Last Updated: **" + date + "\n" +
                "**Total Cases: **" + total_cases + "\n" +
                "**New Cases: **" + new_cases + "\n" +
                "**Total Deaths: **" + total_deaths + "\n" +
                "**New Deaths: **" + new_deaths + "\n" +
                "**Total Tests: **" + total_tests + "\n" +
                "**Total Vaccinations: **" + total_vaccinations + "\n"
                "**Positive Rate: **" + positive_rate)
  return(ret_string)



def get_vaccines_of_country(country_name):
  country_name = country_name.lower()
  local_country_vaccines_df = country_vaccines_df[(country_vaccines_df['location'] == country_name)]
  
  if (local_country_vaccines_df.empty):
    return("Stats not available for this country")

  local_country_vaccines_df = local_country_vaccines_df.replace(np.nan, 'Stats not available', regex=True)

  vaccines = local_country_vaccines_df.vaccines.to_string(index=False)

  ret_string = ("Vaccines available in **" + country_name.title() + "** include: " + vaccines + "\n")

  return (ret_string)