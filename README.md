# README
######################################################

**Pokemon API - https://pokemontcg.io/**

This project requires a `.env` file in the root directory.
Please copy the env.example file with 

```
cp .env.example .env

```

and ensure you have created an API key from their website, setting POKEMON_API_KEY={your api key here}


Please also find the objects at the endpoint:

 **customer-api/objects/**





######################################################
## Setup

For development environment setup, project commands, and usage instructions, please see [HELP.md](HELP.md).

## The test

### Description Of Problem

At Elixir we often have to work with third party apis and ingest data into our system, we write bespoke programs that we call `biz_rules` to perform this integration. This test is a scale model of the sort of work we do quite frequently and is quite reflective of what a typical day might look like, the system uses [django rest framework](https://www.django-rest-framework.org/) to create a viewable api in the browser.

It is designed as a way to learn the mechanics of iTraX, if you are successful in your application you will be working on a system similar to this (but on a much larger scale).

We have selected some apis and you may choose whichever one you like and write the code in the matching `core/biz_rule.py` file (please see the `Services` section below for details).

Your task can be broken down into three parts:

* Study the api docs of the _one_ service you have chosen.
* Write a biz_rule that consumes data from one of the api end points.
* Ingests that into our test system using the provided models.

To be clear; you will not need to write your own models, or edit existing models, nor are you expected to consume all the data the end point returns, some of these end points contain hundreds of megabytes of data, you can ingest as much data as you want to, but you do not have to consume everything.

### The Services

- https://pokemontcg.io/
- https://scryfall.com/docs/api
- https://developer.marvel.com/
- https://rapidapi.com/omgvamp/api/hearthstone


### Running your biz_rule

Running your integration (ingesting the data into the system) is as simple as `just bizrule`
