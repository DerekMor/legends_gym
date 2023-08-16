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
Successful orders can be viewed in the admin panel.\
Users can also log in and sihn up from the header at any area of the site\
Newsletter sign up using Mailchimp form also provided in the footer.\

### Features not implemented

- As of writing my main image did not transfer from the dev environment to deployment. Debugging is needed
- A profile app and nessessary models were created but an individual profile page i ra out of time to impliment these
- Webhooks is another area that could be improved here but a lot more time would be needed to get a grip on them.
- More testing both manual and code should also be implemnted

## Testing

- Site was greatly tested on dev environment but more testing of models and forms on the deployed site would have been better.
- testing found many bugs with models and views and all that were found were dealt with(most were typos, I will never name my .env file env.py again anyway!)

## Deployment

- Create new Heroku app
- link up AWS, ElephantSql
- Add config vars
- Link Heroku app to Github repo
- Click deploy


## SEO

1. Relevant and Quality Content:
THe site tries to provide the relevent content to what people would come looking for and its name suggests

2. Keyword Optimization:
Keyword optimization is present, certainly in product names, though descpitions could have been longer with more keywords. All the headings are also in order

3. Meta Tags and Descriptions:
Meta tag with a large description provided in the head  

4. Mobile Responsiveness:
The website's responsive design ensures that it displays optimally across various devices, including smartphones and tablets. Search engines prioritize mobile-friendly websites. 

5. Sitemap and Robots.txt:
The website features a well-structured sitemap and robots.txt file, providing clear instructions to search engine crawlers regarding which pages to index and which to exclude. This ensures that search engines discover and index the most relevant and valuable pages.

## Digital Marketing
I had an issue here as the day of writing before the deadline my account was suspended and i know the course said to take screenshots but if i have to redo it i will.
<img src="media/2023-08-15 (2).png" alt="Account suspended screenshot">\
I will link the real gyms facebook page I am unsure about whether my account was flagged because I am part of this and was building one with a similar name and images but <a href="https://www.facebook.com/p/D%C3%BAn-Laoghaire-Martial-Arts-100057563164646/"> here</a> it is.\
My own version wasnt huge but I was focusing on organic growth using humour and replying to comments to try to build a relationship with followers then possibly using posts that work for paid ads in the long run.\
The targeted user was anybody into fitness or looking to join martial arts.\
These users would mostly use facebook or instagram.\
Posts would help people who need inspiration to get started by offers or exclusive gear.\
They would recieve these offers by email or social media.\
The newsletter was also a part of the strategy as users had chosen to be on it.

## Credits
- Bootstraps docs
- Stripes docs
- CodeInstitutes Boutique-Ado (particulary the stripe payments)
