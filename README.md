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

(If any of the above features are broken, don't work or you would like to add a feature, please open an issue.)
It is hosted at: https://market.hedonhermdev.tech

To test the GraphQL API and learn more about the schema, go to: https://market.hedonhermdev.tech/api/graphql 


## Roadmap
Currently, we have the following features/improvements in mind: 

- Close open [issues](https://github.com/hedonhermdev/BPPC-Marketplace/issues)
- A cache on the server side to further improve performance. 
- Email and push notifications (it is planned to do this using a separate service to keep the business logic clean)
- More comprehensive testing
- Code cleanup


## Contributing 
To contribute to the project, take a look at the [open issues](https://github.com/hedonhermdev/BPPC-Marketplace/issues). Pick any open issue (or open a new one!) and announce in a comment that you would like to work on an issue. Once assigned, you can start working on it. The documentation is sparse (read: non-existent) so if you have any doubts, come talk to us on the BITS ACM Slack. You'll find us on #backend. 

### Setting Up A Local Development Environment
To contribute to BPPC Marketplace, you will have to set up a development environment on your machine. For that, you'll need Docker.

To install Docker on Ubuntu, you can use the convenience script: 
```bash
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
```

For other operating systems, you can find instructions [here](https://docs.docker.com/get-docker/).

Next, you'll have to install `docker-compose`. You can do that using pip3:
```bash
$ pip3 install docker-compose
```
With the dependencies installed, you are ready to clone the repo run the server. 
```
$ git clone https://github.com/hedonhermdev/BPPC-Marketplace && cd BPPC-Marketplace
$ sudo docker-compose up
```
Open `localost:1337` in a web browser and you should see the server hosted. If you have any issues with the above steps, please file an issue. 

