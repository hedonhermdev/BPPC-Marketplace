# BPPC Marketplace
BITS Pilani's own e-commerce platform. It lets BITSians buy and sell items like books, cycles, etc. to other students without the hassle of Whatsapp messages on public groups. This repo contains all the code for server-side components of the app. 

## The Idea
BPPC Marketplace let's students with a BITSMail to put up items for sale with an expected price and the negotiability of that price. Other BITSians (with or without a BITSMail) can place offers on the products. Once an offer has been accepted by the seller, the contact details will be shared and they can further complete the deal in person.

It is important to allow users without a BITS mail as there are a number of freshers who buy books from seniors (bookpops/bookmoms) but don't have a BITS mail for a while after coming to campus. But to prevent misuse of the app, it is essential to not let anyone without a BITS mail to sell a product. 

## The Backend
It started as a small learning project between me and a couple of friends with a small backend with a REST API. But as the project grew, we found it increasingly difficult to collaborate with the app team which had their own volatile demands. To encounter these problems, we saw it fit to switch to GraphQL. Currently, the backend infrastructure currently features:

- A Django+GraphQL webapp
- A PostgreSQL Database for primary data storage
- An ElasticSearch Server for indexing and searching products
- Docker containers working in harmony
- A comprehensive test-suite

It is hosted at: https://market.bits-dvm.org/

To test the GraphQL API and learn more about the schema, go to: https://market.bits-dvm.org/api/graphql 


## Roadmap
Currently, we have the following features/improvements in mind: 

- A cache on the server side to further improve performance. 
- Email and push notifications (it is planned to do this using a separate service to keep the business logic clean)
- More comprehensive testing
- Code cleanup

## The Team

Everything in this repo has been written by the following people:

- Tirth Jain (@hedonhermdev)
- Sarthak Choudhary (@sarthak-choudhary)
- Anshal Shukla (@anshalshukla)
- Uday Singla (@uday-singla)
- Darsh Mishra (@darmisblip)
