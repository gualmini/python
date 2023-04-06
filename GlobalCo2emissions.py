import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# PLEASE READ: the person who compiled the table mixed commas and periods. Why would you ask us to work on something like this?

available_tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions")

def find_relevant_table(list_of_table):
    for available_table in available_tables:
        if "Fossil CO2 emissions (Mt CO2)" in available_table.columns:
            return available_table

target_table = find_relevant_table(available_tables)

# Eliminate multi -index
current_labels = target_table.columns.to_flat_index()

# Create new column labels by joining the first and second rows of the multi-index and assign new column labels
labels = []
for col in target_table.columns:
    if col[0] != col[1]:
        labels.append(f"{col[0]} {col[1]}")
    else:
        labels.append(col[0])
target_table.columns = labels

#eliminate non_countries
non_countries = ["World", "World – International Aviation", "World – International Shipping", "European Union"]
target_table_only_countries = target_table[~target_table["Country[20]"].isin(non_countries)]

#eliminates all wrongly entered data, why did you do this, really
target_table_only_countries = target_table_only_countries.replace("\,", "", regex=True)
target_table_only_countries = target_table_only_countries.replace("2.397.048", "2397.048", regex=True)
target_table_only_countries = target_table_only_countries.replace("10.877.218", "10877.218", regex=True)
target_table_only_countries = target_table_only_countries.replace("6.263.064", "6263.064", regex=True)
target_table_only_countries = target_table_only_countries.replace("12,466.320", "12466.320", regex=True)
target_table_only_countries = target_table_only_countries.replace("1.018.097", "1018.097", regex=True)
target_table_only_countries = target_table_only_countries.replace("1.210.754", "1210.754", regex=True)
target_table_only_countries = target_table_only_countries.replace("2.454.774", "2454.774", regex=True)
target_table_only_countries = target_table_only_countries.replace("2,648.78", "2648.78", regex=True)
target_table_only_countries = target_table_only_countries.replace("1.149.400", "1149.400", regex=True)
target_table_only_countries = target_table_only_countries.replace("1.276.863", "1276.863", regex=True)
target_table_only_countries = target_table_only_countries.replace("1.320.776", "1320.776", regex=True)
target_table_only_countries = target_table_only_countries.replace("2.378.921", "2378.921", regex=True)
target_table_only_countries = target_table_only_countries.replace("1.733.950", "1733.950", regex=True)
target_table_only_countries = target_table_only_countries.replace("1.764.866", "1764.866", regex=True)
target_table_only_countries = target_table_only_countries.replace("1,942.54", "1942.54", regex=True)
target_table_only_countries = target_table_only_countries.replace("5.085.897", "5085.897", regex=True)
target_table_only_countries = target_table_only_countries.replace("5.971.571", "5971.571", regex=True)
target_table_only_countries = target_table_only_countries.replace("5.107.393", "5107.393", regex=True)
target_table_only_countries = target_table_only_countries.replace("4,752.08", "4752.08", regex=True)



# selects first 5 columns, and changes data to numeric
emission_df = target_table_only_countries.iloc[:,0:5]

def change_data_to_numeric(dataframe, first_column, last_column):
    for column in range (first_column, last_column +1):
        relevant_column = dataframe.columns[column]
        dataframe[relevant_column] = pd.to_numeric(dataframe[relevant_column], errors="coerce")
    return dataframe

emission_df = change_data_to_numeric(emission_df, 1, 4)


# selects 5 largest based on last measurement
most_recent_measurement_column = emission_df.columns[4]
top_emission_df = emission_df.nlargest(5, columns=most_recent_measurement_column)


#this part creates the dataframe for worst and best changers

relative_change_in_emission_df = emission_df
relative_change_in_emission_df["1990"] = 100
relative_change_in_emission_df["2005"] = ""
relative_change_in_emission_df["2017"] = ""
relative_change_in_emission_df["2021"] = ""

if not relative_change_in_emission_df.empty:
    relative_change_in_emission_df = relative_change_in_emission_df.reset_index(drop=True)
    for i in range(len(relative_change_in_emission_df)):
        relative_change_in_emission_df.at[i, "2005"] = round((relative_change_in_emission_df.at[i, relative_change_in_emission_df.columns[2]] / relative_change_in_emission_df.at[i, relative_change_in_emission_df.columns[1]] - 1)* 100, 2)
        relative_change_in_emission_df.at[i, "2017"] = round((relative_change_in_emission_df.at[i, relative_change_in_emission_df.columns[3]] / relative_change_in_emission_df.at[i, relative_change_in_emission_df.columns[1]] - 1)* 100, 2)
        relative_change_in_emission_df.at[i, "2021"] = round((relative_change_in_emission_df.at[i, relative_change_in_emission_df.columns[4]] / relative_change_in_emission_df.at[i, relative_change_in_emission_df.columns[1]] - 1) * 100, 2)


#chosing best and worst 3
relative_change_in_emission_in_decending_order = relative_change_in_emission_df.sort_values(by="2021", ascending=False)
worst_3_relative_change_in_emission_df =relative_change_in_emission_in_decending_order.head(3)
best_3_relative_change_in_emission_df =relative_change_in_emission_in_decending_order.tail(3)
best_3_and_worst_3_relative_change_in_emission_df = pd.concat([best_3_relative_change_in_emission_df, worst_3_relative_change_in_emission_df])
best_3_and_worst_3_relative_change_in_emission_df = best_3_and_worst_3_relative_change_in_emission_df.sort_values(by="2021", ascending=False)


#now we create the dataframe of sizable changers and we get the tree extremes on each side
sizeable_relative_change_in_emission_df = relative_change_in_emission_df[relative_change_in_emission_df.iloc[:,1] >=5]
sizeable_relative_change_in_emission_in_decending_order = sizeable_relative_change_in_emission_df.sort_values(by="2021", ascending=False)
worst_3_sizeable_relative_change_in_emission_df = sizeable_relative_change_in_emission_in_decending_order.head(3)
best_3_sizeable_relative_change_in_emission_df = sizeable_relative_change_in_emission_in_decending_order.tail(3)
best_3_and_worst_3_sizeable_relative_change_in_emission_df = pd.concat([best_3_sizeable_relative_change_in_emission_df, worst_3_sizeable_relative_change_in_emission_df])
best_3_and_worst_3_sizeable_relative_change_in_emission_df = best_3_and_worst_3_sizeable_relative_change_in_emission_df.sort_values(by="2021", ascending=False)

# Graph Part using top_emission_df

countries = ["United States", "China", "Russia", "India", "Japan"]
years = [1990, 2005, 2017, 2021]

emissions = []
for country in countries:
    row = top_emission_df[top_emission_df["Country[20]"] == country]
    country_emissions = [row[f"Fossil CO2 emissions (Mt CO2) {year}"].item() for year in years]
    emissions.append(country_emissions)

# Create the plot
for _ in range(1,5):
    plt.plot(years, emissions[_], label=countries[_])

# Labels, legend, title and so on
plt.xlabel("Year")
plt.ylabel("Fossil CO2 emissions (Mt CO2)")
plt.title("Top 5 CO2 Emission Countries")

plt.legend()
plt.xticks(years)

# Show the plot
plt.show()


# Graph Part using best_3_and_worst_3_relative_change_in_emission_df
fig, ax = plt.subplots()

# Plot the positive and negative values using different colors and labels
pos_bars = ax.bar(best_3_and_worst_3_relative_change_in_emission_df["Country[20]"], best_3_and_worst_3_relative_change_in_emission_df["2021"].where(best_3_and_worst_3_relative_change_in_emission_df["2021"] > 0), color='b', label='Positive')
neg_bars = ax.bar(best_3_and_worst_3_relative_change_in_emission_df["Country[20]"], best_3_and_worst_3_relative_change_in_emission_df["2021"].where(best_3_and_worst_3_relative_change_in_emission_df["2021"] < 0), color='r', label='Negative')

# Set the y-limits for each axis
ax.set_ylim(bottom=-2000, top=16000)
ax2 = ax.twinx()
ax2.set_ylim(bottom=-2000, top=16000)


# Add value labels to each bar
for rect in pos_bars + neg_bars:
    height = rect.get_height()
    if not np.isnan(height):
        ax.annotate(f"{int(height)}", xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8)

# Labels, legend, title and so on
plt.xlabel("Countries")
plt.ylabel("Fossil CO2 emissions change 2021-1990")
plt.title("Best and worst emission reducers")

plt.show()

# graph using the sizeable_relative_change_in_emission_df

fig, ax = plt.subplots()

# Plot the positive and negative values using different colors and labels
pos_bars = ax.bar(sizeable_relative_change_in_emission_df["Country[20]"], sizeable_relative_change_in_emission_df["2021"].where(sizeable_relative_change_in_emission_df["2021"] > 0), color='b', label='Positive')
neg_bars = ax.bar(sizeable_relative_change_in_emission_df["Country[20]"], sizeable_relative_change_in_emission_df["2021"].where(sizeable_relative_change_in_emission_df["2021"] < 0), color='r', label='Negative')

# Set the y-limits for each axis
ax.set_ylim(bottom=-2000, top=16000)
ax2 = ax.twinx()
ax2.set_ylim(bottom=-2000, top=16000)


# Add value labels to each bar
for rect in pos_bars + neg_bars:
    height = rect.get_height()
    if not np.isnan(height):
        ax.annotate(f"{int(height)}", xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8)

# Labels, legend, title and so on
plt.xlabel("Countries")
plt.ylabel("Fossil CO2 emissions change 2021-1990")
plt.title("Change in emission per country")

plt.show()


# graph using the extreme_sizeable_relative_change_in_emission_df

fig, ax = plt.subplots()

# Plot the positive and negative values using different colors and labels
pos_bars = ax.bar(best_3_and_worst_3_sizeable_relative_change_in_emission_df["Country[20]"], best_3_and_worst_3_sizeable_relative_change_in_emission_df["2021"].where(best_3_and_worst_3_sizeable_relative_change_in_emission_df["2021"] > 0), color='b', label='Positive')
neg_bars = ax.bar(best_3_and_worst_3_sizeable_relative_change_in_emission_df["Country[20]"], best_3_and_worst_3_sizeable_relative_change_in_emission_df["2021"].where(best_3_and_worst_3_sizeable_relative_change_in_emission_df["2021"] < 0), color='r', label='Negative')

# Set the y-limits for each axis
ax.set_ylim(bottom=-2000, top=16000)
ax2 = ax.twinx()
ax2.set_ylim(bottom=-2000, top=16000)


# Add value labels to each bar
for rect in pos_bars + neg_bars:
    height = rect.get_height()
    if not np.isnan(height):
        ax.annotate(f"{int(height)}", xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8)

# Labels, legend, title and so on
plt.xlabel("Countries")
plt.ylabel("Fossil CO2 emissions change 2021-1990")
plt.title("Highest and lowest increase in emissions")

plt.show()
