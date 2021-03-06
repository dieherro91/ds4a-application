<!-- ABOUT THE PROJECT -->
## About The Project

_Description_ : 

Not being aware of the travel patterns of people moving within the city can generate logistical problems such as the desynchronization of public transport system schedules and passenger's offer-demand, or buses covering the same route at the same time, causing excessive waiting times for the next available bus and increasing costs for the bus operator. .

That is why solutions are required to Maximize occupancy of the vehicles of the Integrated Public Transport System (SITP) to minimize operational costs.

The project aims to Evaluate passenger demand of the SITP service and predict the number of passengers that should be mobilized for a certain route on a specific day of the week within a given 1 hour time interval.

Some of the questions we attempted to answer are: 
* What is the passenger demand based on day of the week and hour?
* What is the passenger demand by bus stop?
* How many passengers will be mobilized on a specific day of the week for a certain route (in intervals of one hour)?


<Br>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Joseavilez20/ds4a-application.git
   ```
2. Install requirements packages
   ```sh
   pip install -r requirements.txt
   ```
3. Execute on terminal
   ```sh
   python3 index.py
   ```
4. Login
   ```sh
   USER1: team83    PASSWORD1: team-ds4a ;  USER2: masivo-admin    PASSWORD2: !hTW*r8Z0OEV 
   ```


<!-- DOCUMENTATION -->
## Documentation

### __*data folder*__
In this folder are all the files related to the access of the database EC2 in aws.
    
* Folder __trainning_data__ : In this folder are all the .sav files with the random forest predition models for the prediction page, each file corresponds to one route.
    
* __connect_db.py__

  In the connect_db.py is saved all the infomation  the database information, functions:
    - __conn()__ :  Create a new database session and return a new connection object, using psycopg2.connect.

<Br>

* __initial_conditions.py__
  
  In this file are program the functions for the initial conditions for the app so it would accelerate the dropdowns filters that not depend of a date.  
     - __max_date()__:  Search in the database the maximun date available.
     - __min_date()__:  Search in the database the maximun date available.
     - __listZone()__: Search in the database the name of the zone available.
     - __ruta_comercial(__*ZoneValue*__)__: Search in the database the names from the zone ('*ZoneValue*') available and return a list with the names.
     - __data_frame_cluster()__: Return the dataframe of the variables latitude, longitude, zone name, number of passengers, name route, and name of the bus stop.

<Br>

* __list_training_data.py__
  
  The file is used to compared the routes available for the prediction analysis.

  - __list_routes_available_predictc(__*ZoneValue*__)__ : Return a list of dictionaries for the dropdown of route selection, the list was compared the information available in the prediction of the model and the available in the database.

  - __prediction_evaluation(__*df,route*__)__ : Return a list with the predicted passengers from the "df" information for the "route" selected and the return and int value of the deviation of the prediction.
    
    
<Br>

* __models_analysis.py__
  
   The functions in this file are divided in two parts, one of the filters of the user queries and the second for the queries require for the figure plots in the analysis page.

   *Conventions parameters*: 
      
   *start_date*, *end_date* : dates given for the user in the interface that give the delta date for the analysis.
            
   *ZoneValue* : name of the zone of the routes that the user want to make the analysis.
      
   *route* : name of the bus route of the zone that the user want to make the analysis.
      
   *a* : String with the structure ('fecha_trx != '+"\'"+ item +"\'"+' AND ') were item is the token given for the list 'listas' in the function __exclude(__*listas*__)__ in this file.

   - *filters*
     - __exclude(__*listas*__)__ : Return a string that excludes dates in the PostgreSQL query functions, is given in a list (*'listas'*) of dates given for the user in the analysis page.
     - __range_date_postgreSQL(__*start_date,end_date*__)__ : Return a string that modified the dates of the search in the PostgreSQL query functions.
     - __filtro_ruta1(route)__ : Filters the PostgreSQL queries functions, with the route name 'route'.
     - __filtro_ruta2(route)__ : Filters the PostgreSQL queries functions, with the route name 'route'.
     - __filtro_ruta3(route)__ : Filters the PostgreSQL queries functions, with the route name 'route'.
     - __filtro_ruta4(route)__ : Filters the PostgreSQL queries functions, with the route name 'route'.
  
   - *model queries*
   
     - __validaciones_ubication_zone_route(__*start_date,end_date,ZoneValue,route,a*__)__ : Return a data frame with the number of validations with longitude and latitude with the filters and conditions given to the user in the interface page, it will be used to make the map plot with the number of validations.
     - __position_route(__*ZoneValue,route*__)__ : Return a data frame with the longitude and latitude of bus stops, with the filters and conditions given by the user in the interface page, it will be used with the map plot for the number of validations.
     - __scatter_numPasajeros_numBuses_zonal(__*start_date,end_date,ZoneValue,route,a*__)__ : Return a data frame with the number of validations per buses vs number of buses, for all the zones and grouped by day of the week, with the filters and conditions given for the user in the interface page, It will be used to make the scatter plot.
     - __average_number_buses_per_day_per_month_zona_all_routes(__*start_date,end_date,ZoneValue,route,a*__)__ : Return a data frame with the 15 routes with the higher average number of buses per day, with the filters and conditions given by the user in the interface page, it will be used to make the a bar plot.
     - __heatmap_interctive(__*start_date,end_date,ZoneValue,route,a*__)__ : Return a data frame with the total validations for each bus stop and hour of the day, with the filters and conditions given by the user in the interface page, it will be used to make the a Heat map and a bar plot.
     - __average_number_buses_per_hour_route(__*start_date,end_date,ZoneValue,route,a*__)__ : Return a data frame with average number of buses for each hour of the day, with the filters and conditions given by the user in the interface page, it will be used to make a bar plot.
     - __histogram_validations(__*start_date,end_date,ZoneValue,route,a*__)__ : Return a data frame with validations per travel route, with the filters and conditions given by the user in the interface page, it will be used to make the a histogram plot.

<Br>

* __models_prediction.py__
  
   The functions in this file have the queries require for the figure plots in the Prediction page.
   - __measure(__*lat1, lon1, lat2, lon2*__)__ :  Return the distance of 2 bus stop, each one with the pair latude and logitude.
   - __data_frame_cluster(__*ZoneValue*__)__ : Return the dataframe and orders the data from the data frame "homes.df_cluster", which is obtained at the beginning of the page beacause is not depended for the users filters.
   - __get_info_stops_route(__*route,input_date*__)__ : this function make a query to the data base for the information of the 'route' and save the predection date

<Br>

### __views folder__

In this folder are all the files related to make the figure plots for the app.
* __figure_analitic.py__

  The functions in this file make the figures plot for the analysis page.
    - __graph1_validaciones_ubication_zone_route(__*start_date,end_date,ZoneValue,route,a*__)__ : Return the street map figure with the number of validations with longitude and latitude, with the filters and conditions given by the user in the interface page

    - __make_graph_zonal(__*start_date,end_date,ZoneValue,route,a*__)__ : Return a Scatter figure with the number of validations per buses vs num buses, for all the zone and grouped by day of the week, with the filters and conditions given by the user in the interface page

    - __average_number_buses_per_day_per_month_zone_all_routes(__*start_date,end_date,ZoneValue,route,a*__)__ : Return a bar figure with the 15 highest average number of buses per day, with the filters and conditions given by  the user in the interface page.

    - __heat_map_interactivition(__*start_date,end_date,ZoneValue,route,a*__)__: Return a heat map and a bar plot figures with the total validations, for each bus stop and hour of the day,with the filters and conditions given by  the user in the interface page

    - __average_number_buses_per_hour_route(__*start_date,end_date,ZoneValue,route,a*__)__: Return a bar figure with average number of buses for each hour of the day, with the filters and conditions given by the user in the interface page.

    - __histogram_validations(__*start_date,end_date,ZoneValue,route,a*__)__: Return a histogram plot with validations per travel route, with the filters and conditions given by the user in the interface page.

* __figure_prediction.py__

  The functions in this file make the figures plot for the Prediction page.
    - __cluster(__*ZoneValue,n_clusters,route*__)__: Return the cluster for zone:'ZoneValue' and 'route' and the numbers of clusters 'n_clusters' all the routes for a given zone and the dataframe with the clusters.

    - This function return a dictionary with 2 graphs one is a map streep graph with the passengers predictions and tge second is a graph plot with the same information but the user have another point of view.

<Br>

### __lib folder__
In this folder the files are related to the construction, of the navegation bar and the sidebar, for the analysis and predictive page.

* sidebar.py
  
  In this file is the layout for the sidebar in the analysis page, with the dropdowns distribution, and filters.

* sidebar_pred.py

  In this file is the layout for the sidebar in the Prediction page, with the dropdowns distribution, and filters.
* title.py
  
  In this file is the layout for the navegation bar is present in the home, analysis, Prediction and team-83 page, with the links for the navegation between pages and logout buttom.

<Br>

### __pages folder__
In this folder are the files related for the construction of the pages that aren't the pages app.

* homes.py
  
  In the file is made the layout for the home page.

* login-py
  
   In the file is made the layout for the login page.

* team_83.py

   In the file is made the layout for the team-83 page (About Us).

<Br>

### __content_apps folder__
In this folder are the files were the layout of the apps are construct.
* analitics.py
  
  The analitics.py have the layout of the analysis app where are called the figure plots.

* prediction.py
  
  The prediction.py have the layout of the Prediction app where are called the figure plots.














