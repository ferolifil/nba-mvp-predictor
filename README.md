# nba-mvp-predictor

The project consists in 4 steps.

1. Scrapping
2. Standardizing
3. Analysis
4. App

--------------------------------------------
### Scrapping
* All the data was scrapped from [basketball reference](https://www.basketball-reference.com/).
* It was then stored at the <basketball_reference_dbs> folder.

--------------------------------------------
### Standardizing
* The files needed some adjustments, like removing null lines, resolving some duplicates(players' transfers).
* The correct files were stored in <data> folder.

--------------------------------------------
### Analysis
* Here's the complete analysis and model selection.
* In the first try, my dataframe didn't had stats about the teams' performance. I saw that this was an important data so I had to get back to steps 1-2 and add the teams' information.
--------------------------------------------
### App
* After the three the steps I've created an simple app just to show the prediction for 2021 NBA MVP. Needs improvement. 
--------------------------------------------
To produce this application I've used data from 41 different seasons, between 1981 and 2021. I've chosen this dates because in 1981 the league changed the mvp election process.</br>
In the analysis we can see a number of abbreviations, the <b>Glossary.txt</b> file cover them all.</br>


To run the application.

```python
streamlit run app.py
```
