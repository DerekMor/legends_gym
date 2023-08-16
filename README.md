# Legends Gym

Legends gym is a real gym I am a member of based in Dublin. I recieved full permission from the owner before basing this on our gym. It is a full stack application using django, HTML, CSS, JavaScript and Bootstrap.\

The site is liked together using ElephantSQL for the database, Amazon Web Services for hosting the images and static files and Stripe for taking card payments. All of this is joined together and deployed on Heroku.\
<a href="https://legends-gym-b229ec203712.herokuapp.com/"> Link to the deployed site</a>


## Site features

As an e-commerce site, users are able to search through the contents as well as sort their searches.\
Filtering by category is also available from the main nav bar\
Users can click into the full products to see details and add them to their cart.\
In the shopping cart page users can update or remove items before moving onto the checkout page.\
In the main checkout page users must be logged in to complete their orders\
In this page there is a order details form and card payment using Stripe\
After a successful checkout a success page is rendered for the users as well as a message using django messages.\
Users can also log in and sihn up from the header at any area of the site\
Newsletter sign up form also provided in the footer.\
