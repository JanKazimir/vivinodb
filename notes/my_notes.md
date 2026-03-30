# MY NOTES


The point is to create a report : the needed things are in the instructions

uv add ipykernel sqlite3 jupysql streamlit


notes
- watch out for SQL types of data, it's different than python
- no pandas
- needs visualisations
- write requests in .sql files



I'm starting an exercise on SQL. Analysing a db of wines. It's SQLlite.


1/ visualisations: The instructions say we need to create visualisations. any way to do it without pandas? The instructions say to do without it, but maybe that's just for the SQL queries part.
2/ the instruction says to write requests in dedicated .sql files. why? what's the point?

3/ Broadly how should i approach this? 

4/ What libraries are needed? so far i have : uv add ipykernel jupysql streamlit matplotlib
Anything else that seems obvious?





### Must-have features

A complete market analysis report that answers these questions:

- We want to highlight 10 wines to increase our sales. Which ones should we choose and why?
- We have a marketing budget for this year. Which country should we prioritise and why?
- We would like to give awards to the best wineries. Come up with 3 relevant ones. Which wineries should we choose and why? Be creative ;)
- We have detected that a big cluster of customers like a specific combination of tastes. We have identified a few `primary` `keywords` that match this. 
- We have detected that a big cluster of customers like a specific combination of tastes. We have identified a few `primary` `keywords` that match this. We would like you to **find all the wines that have those keywords**. To ensure the accuracy of our selection, ensure that **more than 10 users confirmed those keywords**. Also, identify the `group_name` related to those keywords.

**⚠️ Those keywords are CASE SENSITIVE ⚠️**

	- coffee
	- toast
	- green apple
	- cream
	- citrus

- We would like to select wines that are easy to find all over the world. **Find the top 3 most common `grape` all over the world** and **for each grape, give us the the 5 best rated wines**.
- We would to give create a country leaderboard, give us a visual that shows the **average wine rating for each `country`**. Do the same for the `vintages`.
- Give us any other useful insights you found in our data. **Be creative!**


### Nice-to-have features

- Optimise your solution to have the result as fast as possible.
- Implement visualizations best practices (e.g. data storytelling, nice design, relevancy to the questions asked, etc.). 
- One of our VIP client likes `Cabernet Sauvignon` and would like our top 5 recommendations. Which wines would you recommend to him?
- Can you recommend anything to improve the data, the database schema or the typing?


### Constraints

- You are not allowed to use pandas or similar tools.
- Write your requests in dedicated `.sql` files.
- Use SQL `JOIN` operations to cross-reference tables. You can not do it using Python.