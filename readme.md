# Unraveling User Behavior and Industry Strategies in the Anime Industry

## Data cleaning

All files required for data cleaning are present in the [**DataClean** folder](/DataClean). 
Refer to the following table which shows which python script generates which cleaned dataset.

| Cleaned datasets      | Python Script |
| ----------- | ----------- |
| cleaned_dataset2023.csv       | [dataset2023_Cleaning_A.py](/DataClean/dataset2023_Cleaning_A.py)     |
| cleaned_dataset2023_unknown.csv    | [dataset2023_Cleaning_B.py](/DataClean/dataset2023_Cleaning_B.py)       |

- cleaned_dataset2023.csv: All NaN values removed from all numeric and non-numeric columns.
- cleaned_dataset2023_unknown.csv: NaN values removed only for columns corresponding to numeric values.

## Research

All files required for the models and plots are present in the [**DataProcess** folder](/DataProcess).

### Predictive model for Studios

Using data from Popularity, Favourites and other such features, we plan to use a conditional probability table (conditioned on rank or popularity) to help predict features such as
* Genre
* Type
* Release season
  
for studios to suggest the features that are best for the desired rank/popularity.

Find the predictive model in [here](/DataProcess/prediction_models.py).

### Verification of results through plots

For the top 20 most popular animes, we plan to extract the corresponding studios and check their trends to check whether these studios take user trends into account while planning releases.

Find the code for all the verification plots [here](/DataProcess/verification_plots.py).

