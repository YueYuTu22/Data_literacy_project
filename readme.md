# Unraveling User Behavior and Industry Strategies in the Anime Industry

## Plan

The project is planned to have two main sections:

### Predictive model for Studios

Using data from Popularity, Favourites and other such features, we plan to use a conditional probability table (conditioned on rank or popularity) to help predict features such as
* Genre
* Type
* Release season
  
for studios to suggest the features that are best for the desired rank/popularity.

### Verification of results

For the top 20 most popular animes, we plan to extract the corresponding studios and check their trends to check whether these studios take user trends into account while planning releases.

## Notes from meeting

### 10/01/2024

* Bayesian approach with an uniformative prior: Conditional probability model with a something like a beta binomial prior
* Filter the data to get the conditional densities
