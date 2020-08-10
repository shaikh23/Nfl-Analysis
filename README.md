# Nfl-Analysis
Do taller NFL players score more touchdowns and gain more yards than their peers? Do players with a higher body mass index(BMI) obtain more touchdowns and yards than their peers?


For my project I will be going through several datasets and attempting to see whether the taller and heavier players(measured by BMI) are statistically gaining more yards in specific statistics, e.g. QBR/YAC etc., than their shorter/smaller peers. I will be drawing most of my data from pro-football-reference.com and nfl.com.


# Background
Sports has always held a special place for me, with my favorite being football. I grew watching the NFL for many years as fan of the Philadelphia Eagles and enjoyed playing in games at my high school. One thing I noticed in my brief football career was that a large amount of the taller and larger players were scoring more touchdowns and gaining more yards than the rest of our team. So, I wanted to see if there is a similar trend at the professional level.

# Exploratory Data Analysis
Initially I had to clean a large amount of data by removing duplicate players and removing some NAN values. Then I wanted to see how the distributions appeared from a histogram.


# Results
The results from the scatter plot were difficult to interpret and I decided to put the data into a bar chart format with corresponding error bars to indicate any outliers. Now it is much easier visually to interpret the data. 
![WR Height vs Yards](/images/wrbmihtyds.png)

![WR Height vs Touchdowns](wrhtbartd.png)

It should be noted that I have converted traditional height measurement from feet and inches to just inches. For reference 72 inches is six feet tall. It is interesting to see that from both graphs it appears that being physically taller has a correlation to gaining more yards and scoring more touchdowns. I believe this is due to the fact that being taller may make it easier to catch a jump ball, which can lead to more points and yards.

![WR BMI vs Yards](wrbmibaryds.png)

![WR BMI vs Touchdowns](/images/wrbmibartd.png)

It appears from these graphs that there is quite a drastic dropoff in both yards acquired and touchdowns scored with lighter players, those having a lower BMI, are significantly outperforming their heavier counterparts. This is a curious finding which I believe may be explained by the idea that acquiring more mass can slow a player down. There seems to be a tipping point around a BMI of 29 where after that every BMI increase leads to significant diminishing returns. 



# Technologies Utilized
The tech stack I used was Python and Pandas to read and clean the information. Matplotlib along with Seaborn were used to visualize the data in plots and Scipy was used to run the statistical tests and determine the p-values for each test.


# Future Steps
Going forward I would like to analyze other positions to see if there is a trend between height/BMI and that position's key metrics. Specifically I want to see if a similar correlation between height/BMI and performance is clear for other important offensive positions such as the quarterbacks and the running backs.
