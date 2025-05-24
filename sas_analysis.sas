/* SAS Project */

/* -> creating SAS datasets from external files */

proc import datafile='/home/u64202849/Proiect/Casa_Timis_Monthly_Activity_3Y.csv'
	out=work.activity
	dbms=csv
	replace;
	getnames=yes;
run;

proc import datafile='/home/u64202849/Proiect/Casa_Timis_Customer_Reviews_3Y.csv'
	out=work.reviews
	dbms=csv
	replace;
	getnames=yes;
run;

proc contents data=activity;
run;

proc contents data=reviews;
run;


/* -> creating and applying user-defined formats */

*1 - Custom format for review scores: Low, Medium, High;
proc format;
	value score_fmt
		low -< 8 = 'Low'
		8 -< 9 = 'Medium'
		9 - high = 'High';
run;

data reviews_fmt;
	set work.reviews;
	format Average_Review_Score score_fmt.;
run;

*2 - Format for number of guests: Few, Medium, Many;
proc format;
	value guests_fmt
		low -< 500 = 'Few'
		500 -< 1000 = 'Medium'
		1000 - high = 'Multi';
run;

data activity_fmt;
	set activity;
	format Number_of_Guests guests_fmt.;
run;


/* -> iterative and conditional data processing */

*1 - Complaint level classification: None, Low, High;
data complaints_flag;
	set reviews;
	length Complaint_Level $10;
	if Complaints_Count = 0 then Complaint_Level = "None";
	else if Complaints_Count <= 3 then Complaint_Level = "Low";
	else Complaint_Level = "High";
run;

*2 - Monthly classification based on occupancy rate;
data high_occupancy_flag;
	set activity;
	length Occupancy_Level $10;
	if Occupancy_Rate_Percent >= 80 then Occupancy_Level = "High";
	else if Occupancy_Rate_Percent >= 50 then Occupancy_Level = "Medium";
	else Occupancy_Level = "Low";
run;


/* -> creating data subsets */

*1 - Subset of reviews with score below 9;
data low_scores;
	set reviews;
	if Average_Review_Score < 9;
run;

*2 - Subset of months with total revenue below 100000 EUR;
data low_revenue;
	set activity;
	if Total_Revenue_EUR < 100000;
run;


/* -> using SAS functions */

* Calculating revenue per guest and log of spa revenue;
data activity_extended;
	set activity;
	Revenue_per_Guest = Total_Revenue_EUR / Number_of_Guests;
	Log_Spa_Revenue = log(Spa_Revenue_EUR);
run;


/* -> combining datasets using SAS procedures and SQL */

*1 - Join activity and reviews based on month;
proc sql;
	create table combined_sql as
	select A.*, B.Average_Review_Score, B.Number_of_Reviews	
	from activity A join reviews B
	on A.Month_Year = B.Month_Year;
quit;

*2 - Filtered join: only months with score below 9;
proc sql;
	create table combined_low as
	select A.*, B.Average_Review_Score
	from activity A inner join reviews B
	on A.Month_Year = B.Month_Year
	where B.Average_Review_Score < 9;
quit;


/* -> using arrays */

*1 - Revenue normalization using array (scaling to thousands);
data normalize_revenues;
	set activity;
	array revs[3] Total_Revenue_EUR Spa_Revenue_EUR Restaurant_Revenue_EUR;
	array norm[3] norm_Total norm_Spa norm_Rest;
	do i = 1 to 3;
		norm[i] = revs[i] / 1000;
	end;
	drop i;
run;

*2 - Converting percentages to decimals using array;
data normalize_rates;
	set activity;
	array rates[2] Occupancy_Rate_Percent Repeat_Guest_Rate;
	array decimals[2] Occ_Rate_Decimal Repeat_Rate_Decimal;
	do i = 1 to 2;
		decimals[i] = rates[i] / 100;
	end;
	drop i;
run;


/* -> using procedures for reporting */

*1 - Display months with review score below 9;
proc print data=combinat_sql;
	where Average_Review_Score < 9;
	title "Months with Review Scores below 9";
run;

*2 - Display months with more than 1000 guests;
proc print data=activity;
	where Number_of_Guests > 1000;
	var Month_Year Number_of_Guests Total_Revenue_EUR;
	title "Months with More Than 1000 Guests";
run;


/* -> using statistical procedures */

*1 - Descriptive statistics for revenue and occupancy;
proc means data=activity mean std min max;
	var Total_Revenue_EUR Occupancy_Rate_Percent;
run;

*2 - Statistics for Spa and Restaurant revenues;
proc means data=activity mean median std maxdec=2;
	var Spa_Revenue_EUR Restaurant_Revenue_EUR;
	title "Statistics for Spa and Restaurant Revenues";
run;


/* -> generating charts */

*1 - Monthly total revenue evolution;
proc sgplot data=activity;
	series x=Month_Year y=Total_Revenue_EUR;
	title "Monthly Revenue Evolution";
run;

*2 - Monthly occupancy rate evolution;
proc sgplot data=activity;
	series x=Month_Year y=Occupancy_Rate_Percent;
	title "Monthly Occupancy Rate Evolution";
run;

*3 - Bar plot: guest numbers per year grouped by season (without date conversion);
data activity_season;
	set activity;
	length Season $10;
	length MonthName $15;
    * Splitting components of Month_Year into text format;
	MonthName = scan(Month_Year, 1, ' ');
	Year = input(scan(Month_Year, 2, ' '), 4.);
	* Matching the month name with the season;
	select (MonthName);
		when ('December', 'January', 'February')   Season = 'Winter';
		when ('March', 'April', 'May')             Season = 'Spring';
		when ('June', 'July', 'August')            Season = 'Summer';
		when ('September', 'October', 'November')  Season = 'Autumn';
		otherwise Season = 'Unknown';
	end;
run;

*Grouped bar chart;
proc sgplot data=activity_season;
	styleattrs datacolors=(red green gold blue);
	vbar Year / response=Number_of_Guests group=Season stat=sum groupdisplay=cluster;
	title "Total Number of Guests per Year by Season";
run;


/* -> SAS ML - Basic Machine Learning (Regression Example)*/

*1 - Linear regression: predicting revenue based on occupancy, guests, and Spa revenue;
proc reg data=activity;
	model Total_Revenue_EUR = Occupancy_Rate_Percent Number_of_Guests Spa_Revenue_EUR;
	title "Linear Regression: Revenue vs. Occupancy, Guests, and Spa Revenue";
run;

*2 - Multiple linear regression with diagnostics;
proc reg data=activity;
	model Total_Revenue_EUR = Occupancy_Rate_Percent Number_of_Guests 
	                          Spa_Revenue_EUR Restaurant_Revenue_EUR;
	plot student.*predicted. / cframe=ligr;
	title "Multiple Linear Regression: Predicting Total Revenue";
run;
quit;
		
		
		
		
		
		
		