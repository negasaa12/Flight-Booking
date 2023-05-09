# flight-booking




FLIGHT API provided by https://developers.amadeus.com/self-service/category/air/api-doc/flight-offers-search?ref=apilist.fun. 



This API contains valuable data such as flight prices, origin and destination locations, and available flights for different airlines.
To implement this functionality, the database schema will consist of several key tables including Users, Flights, Airlines, and potentially Tickets. The main challenge in utilizing the API is ensuring that we extract only relevant data for the app's functionality. In addition, sensitive user information such as passwords must be secured to protect user privacy.
The application will allow users to create profiles that provide a centralized location to store their flight bookings. The app will enable users to view available flights based on their chosen destination and origin, as well as the ability to create or delete multiple orders. To access these features, users must first log in and will be directed to their personal profile page displaying their booked flights. A search bar will be available to enable users to select their desired origin and destination, displaying all available flights for the selected day.
