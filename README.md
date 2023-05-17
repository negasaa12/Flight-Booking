# flight-booking




FLIGHT API provided by https://developers.amadeus.com/self-service/category/air/api-doc/flight-offers-search?ref=apilist.fun. You need to sign up and get a token to be able to use the application fully. 




## Title of The App : AeroSerenity

This API contains valuable data such as flight prices, origin and destination locations, and available flights for different airlines.
To implement this functionality, the database schema will consist of several key tables including Users, Flights, Airlines, and potentially Tickets. The main challenge in utilizing the API is ensuring that we extract only relevant data for the app's functionality. In addition, sensitive user information such as passwords must be secured to protect user privacy.
The application will allow users to create profiles that provide a centralized location to store their flight bookings. The app will enable users to view available flights based on their chosen destination and origin, as well as the ability to create or delete multiple orders. To access these features, users must first log in and will be directed to their personal profile page displaying their booked flights. A search bar will be available to enable users to select their desired origin and destination, displaying all available flights for the selected day.



Users we'll land in the home page and will be eager to go to flights on the nav bar but you will need to be logged in. Users will need to sign up and log in to get access to the their profile. After the profile is made they can go and look for flights putting in there state or iatacode  after they choosen their destination and origin the site will take you to see all the flights available (max 5) and you can choose. Users we'll be able to click book flight button and it will take them to their profile page with the flight information all in the "My ticket" section of their profile. Users can also delete flights. 
