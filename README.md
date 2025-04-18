# BLOCKSTAK NEWS API

## Table of Contents

- [Project description](#project-description)
    - [Codebase improvements](#codebase-improvements)
- [Setup instructions](#setup-instructions)
    - [FastAPI Setup](#fastapi-setup)
    - [Database Setup](#database-setup)
- [How to run the server](#how-to-run-the-server)
- [How to run tests](#how-to-run-tests)
- [How to use Docker](#how-to-use-docker)
- [How to generate access tokens and use secured endpoints](#how-to-generate-access-tokens-and-use-secured-endpoints)
- [API usage examples and descriptions for all 5 endpoints above](#api-usage-examples-and-descriptions-for-all-5-endpoints-above)
    - [/news](#news)
    - [/news/save-latest](#newssave-latest)
    - [/news/headlines/country/{country_code}](#newsheadlinescountrycountry_code)
    - [/news/headlines/source/{source_id}](#newsheadlinessourcesource_id)
    - [/news/headlines/filter](#newsheadlinesfilter)

## Project description

### Codebase improvements

## Setup instructions

### FastAPI Setup

1. Create a virtual environment using the following command

    **MacOS / Linux**

    ```bash
    python3 -m venv env
    ```

    **Windows**

    ```powershell
    python -m venv env
    ```

2. Activate the virtual environment using the following command

    **MacOS / Linux**

    ```bash
    source env/bin/activate
    ```

    **Windows**

    ```powershell
    env/Scripts/activate
    ```

3. Install all the required packages using the following command

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file on the project root, then copy the contents from the `.env.example` file and paste them to this file. Fill the variables with the values for your system.

### Database Setup

1. Create a Postgres database on `psql` using the following command

    ```sql
    CREATE DATABASE news_api_db;
    ```

2. On the project root, run the following command to create the database tables and apply the migrations

    ```bash
    aerich upgrade
    ```

## How to run the server

**Development**

To run the server in development mode, run the following command

```bash
fastapi dev main.py
```

**Production**

To run the server in production mode, run the following command

```bash
fastapi run --host 0.0.0.0 main.py
```

## How to run tests
To run the tests, run the following command

```bash
pytest -v
```

## How to use Docker

## How to generate access tokens and use secured endpoints

The project uses code based OAuth2 authorisation. For that, a client ID and client secret are required. For the purposes of this project, the client ID and client secret have been fixed to the following -

```
CLIENT_ID=demo-client
CLIENT_SECRET=C51D80D50A15DF7D
```

Use the following steps to acquire a token to access the secured endpoints

1. Make a `GET` request to the `/code` endpoint with the _CLIENT_ID_ as a query parameter. In the response, there will be a temporary code sent. Copy the code and proceed to the next step.

    An example request and response of the endpoint is given below -

    **_Request_**
    ```bash
    curl --location --request GET 'http://localhost:8000/code?client_id=demo-client' \
    --header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
    --header 'Accept: */*' \
    --header 'Host: localhost:8000' \
    --header 'Connection: keep-alive'
    ```

    **_Response_**
    ```json
    {
        "success": true,
        "message": "Request Success",
        "data": {
            "code": "QR1kPwY9L"
        }
    }
    ```

2. Make a `GET` request to the `/token` endpoint with the _CLIENT_ID_, _CLIENT_SECRET_ and the _code_ acquired in the previous step as a query parameters. In the response, the token will be sent. Copy the token and use it as a _Bearer_ authorisation header when making the requests on the `/news` endpoints.

    An example request and response of the endpoint is given below -

    **_Request_**
    ```bash
    curl --location --request GET 'http://localhost:8000/token?client_id=demo-client&client_secret=C51D80D50A15DF7D&code=QR1kPwY9L' \
    --header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
    --header 'Accept: */*' \
    --header 'Host: localhost:8000' \
    --header 'Connection: keep-alive'
    ```

    **_Response_**
    ```json
    {
        "success": true,
        "message": "Request Success",
        "data": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vLWNsaWVudCIsImV4cCI6MTc0NDk4NTc3OC41MzE2M30.V-_Bkux53_6owIYxLUBTI5Spz8ev4a-Yb0RcdoyiQ0k"
        }
    }
    ```

## API usage examples and descriptions for all 5 endpoints above

All the APIs with example requests and responses, as well as full API documentation can be found in the following Apidog docs

[Blockstak News API Documentation](https://apidog.com/apidoc/shared-aef2ed00-bbf0-4b31-bb83-f08ee1c98020?pwd=GH7Z9tLL)

1. `/news`

    **_Request_**
    ```bash
    curl --location --request GET 'http://localhost:8000/news?search=bitcoin&page=1&limit=3' \
    --header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vLWNsaWVudCIsImV4cCI6MTc0NDk4NTc3OC41MzE2M30.V-_Bkux53_6owIYxLUBTI5Spz8ev4a-Yb0RcdoyiQ0k' \
    --header 'Accept: */*' \
    --header 'Host: localhost:8000' \
    --header 'Connection: keep-alive'
    ```

    **_Response_**
    ```json
    {
        "success": true,
        "message": "Request Success",
        "totalCount": 10033,
        "page": 1,
        "limit": 3,
        "nextPage": 2,
        "prevPage": null,
        "pageCount": 3345,
        "data": [
            {
                "source": {
                    "id": null,
                    "name": "BBC News"
                },
                "author": null,
                "title": "Bitcoin in the bush - the crypto mine in remote Zambia",
                "description": "Bitcoin miners will go to remote locations to take advantage of cheap electricity.",
                "url": "https://www.bbc.com/news/articles/cly4xe373p4o",
                "urlToImage": "https://ichef.bbci.co.uk/news/1024/branded_news/583f/live/26541af0-0628-11f0-b773-ddd19e96af91.jpg",
                "publishedAt": "2025-03-25T05:53:55Z",
                "content": "Joe TidyCyber correspondent, BBC World Service\r\nEngineers from Gridless create makeshift computer labs to maintain their bitcoin mines\r\nThe roar of the Zambezi is deafening as millions of gallons of … [+8832 chars]"
            },
            {
                "source": {
                    "id": "the-verge",
                    "name": "The Verge"
                },
                "author": "Gaby Del Valle",
                "title": "Trump’s DOJ will no longer prosecute cryptocurrency fraud",
                "description": "The Trump administration is disbanding a Department of Justice unit dedicated to enforcing cryptocurrency fraud, ending what it calls âregulation by prosecution.â  In a memo obtained by The Washington Post, deputy attorney general Todd Blanche directed fe…",
                "url": "https://www.theverge.com/policy/645399/trump-doj-cryptocurrency-fraud-prosecutions-memo",
                "urlToImage": "https://platform.theverge.com/wp-content/uploads/sites/2/chorus/uploads/chorus_asset/file/25461724/STK432_Government__CVirginia_B.jpg?quality=90&strip=all&crop=0%2C10.732984293194%2C100%2C78.534031413613&w=1200",
                "publishedAt": "2025-04-08T18:57:35Z",
                "content": "An internal memo ordered prosecutors to no longer target virtual currency exchanges.\r\nAn internal memo ordered prosecutors to no longer target virtual currency exchanges.\r\nThe Trump administration is… [+2061 chars]"
            },
            {
                "source": {
                    "id": "business-insider",
                    "name": "Business Insider"
                },
                "author": "Kwan Wei Kevin Tan",
                "title": "Cathie Wood says people are going to learn the hard way that meme coins are the worst",
                "description": "Wood, who has been bullish about cryptocurrencies like bitcoin, said her private funds are not investing in meme coins.",
                "url": "https://www.businessinsider.com/cathie-wood-people-buying-meme-coins-learn-a-hard-lesson-2025-3",
                "urlToImage": "https://i.insider.com/67da328fb8b41a9673fb0acb?width=1200&format=jpeg",
                "publishedAt": "2025-03-19T05:04:25Z",
                "content": "Ark Invest's Cathie Wood, who has been bullish about cryptocurrencies like bitcoin, said her private funds are not investing in meme coins.Joe Raedle via Getty Images\r\n<ul><li>Cathie Wood said most m… [+3159 chars]"
            }
        ]
    }
    ```

2. `/news/save-latest`

    **_Request_**
    ```bash
    curl --location --request POST 'http://localhost:8000/news/save-latest' \
    --header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vLWNsaWVudCIsImV4cCI6MTc0NDk4NTc3OC41MzE2M30.V-_Bkux53_6owIYxLUBTI5Spz8ev4a-Yb0RcdoyiQ0k' \
    --header 'Accept: */*' \
    --header 'Host: localhost:8000' \
    --header 'Connection: keep-alive'
    ```

    **_Response_**
    ```json
    {
        "success": true,
        "message": "Saved latest three headlines successfully",
        "data": [
            {
                "id": 1,
                "title": "Michelle Trachtenberg cause of death: Star died of complications from diabetes, medical examiner finds - Yahoo",
                "author": "Taryn Ryder",
                "description": "The actress was found dead in her New York City apartment on Feb. 26, and at the time, the cause and manner of her death was unclear. Her family reportedly...",
                "published_at": "2025-04-17T12:24:47+00:00",
                "created_at": "2025-04-18T15:05:50.338644+00:00",
                "updated_at": "2025-04-18T15:05:50.338651+00:00"
            },
            {
                "id": 2,
                "title": "Lebanon’s Government Arrests Militants, Asserting Its Authority - WSJ",
                "author": "WSJ",
                "description": null,
                "published_at": "2025-04-17T11:18:00+00:00",
                "created_at": "2025-04-18T15:05:50.343789+00:00",
                "updated_at": "2025-04-18T15:05:50.343794+00:00"
            },
            {
                "id": 3,
                "title": "Trump again calls for Fed to cut rates, says Powell’s ‘termination cannot come fast enough’ - CNBC",
                "author": "Fred Imbert",
                "description": "President Donald Trump on Thursday again called for the Federal Reserve to lower rates and even hinted at the \"termination\" of Chair Jerome Powell.",
                "published_at": "2025-04-17T10:56:22+00:00",
                "created_at": "2025-04-18T15:05:50.344604+00:00",
                "updated_at": "2025-04-18T15:05:50.344607+00:00"
            }
        ]
    }
    ```

3. `/news/headlines/country/{country_code}`

    **_Request_**
    ```bash
    curl --location --request GET 'http://localhost:8000/news/headlines/country/us' \
    --header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vLWNsaWVudCIsImV4cCI6MTc0NDk5NDUzOC45NTQyODJ9.jn9qGVFm9NqPOvivNKW91Ks8OCdjWjZOxULCkchkBtM' \
    --header 'Accept: */*' \
    --header 'Host: localhost:8000' \
    --header 'Connection: keep-alive'
    ```

    **_Response_**
    ```json
    {
        "success": true,
        "message": "Fetched headlines successfully",
        "data": [
            {
                "source": {
                    "id": null,
                    "name": "Barron's"
                },
                "author": "Barron's",
                "title": "AMD, Micron, Broadcom Stocks Hit by AI Rules and Tariff Uncertainty - Barron's",
                "description": null,
                "url": "https://www.barrons.com/articles/amd-micron-broadcom-stock-rebound-chips-ai-aba25fef",
                "urlToImage": null,
                "publishedAt": "2025-04-17T14:26:00Z",
                "content": null
            },
            {
                "source": {
                    "id": "the-wall-street-journal",
                    "name": "The Wall Street Journal"
                },
                "author": "WSJ",
                "title": "UnitedHealth Shares Tumble After Earnings Fall Short Due to Medicare Issues - WSJ",
                "description": null,
                "url": "https://www.wsj.com/business/earnings/unitedhealth-group-unh-q1-earnings-report-2025-93629e9d",
                "urlToImage": null,
                "publishedAt": "2025-04-17T13:45:00Z",
                "content": null
            },
            {
                "source": {
                    "id": "the-verge",
                    "name": "The Verge"
                },
                "author": "Ash Parrish",
                "title": "Nintendo shows off Mario Kart World’s new courses, items, and open world features - The Verge",
                "description": "Nintendo has held a Mario Kart World direct showing off more gameplay of the Switch 2 launch title.",
                "url": "https://www.theverge.com/news/649138/mario-kart-world-direct-nintendo-switch-2-gameplay",
                "urlToImage": "https://platform.theverge.com/wp-content/uploads/sites/2/2025/04/NintendoSwitch2_MarioKartWorld_SCRN_GrandPrix_01_a1f79d.png?quality=90&strip=all&crop=0%2C3.4613147178592%2C100%2C93.077370564282&w=1200",
                "publishedAt": "2025-04-17T13:38:47Z",
                "content": "Its Mario Karts world and were all driving in it.\r\nIts Mario Karts world and were all driving in it.\r\nNintendo is possibly hoping to steer the narrative regarding the Switch 2 back in a positive dire… [+2280 chars]"
            },
            {
                "source": {
                    "id": "associated-press",
                    "name": "Associated Press"
                },
                "author": "Aamer Madhani, Josh Boak",
                "title": "Trump says Federal Reserve Chair Powell’s ‘termination cannot come fast enough’ - AP News",
                "description": "President Donald Trump has slammed Federal Reserve Chair Jerome Powell, reiterating his frustration the Fed has not aggressively cut interest rates and saying the central bank leader’s “termination cannot come fast enough.” Trump hinted in a social media post…",
                "url": "https://apnews.com/article/trump-powell-federal-reserve-fed-termination-b6148c8048dda538a6ca3b5a270fd09e",
                "urlToImage": "https://dims.apnews.com/dims4/default/c6f2526/2147483647/strip/true/crop/5616x3159+0+293/resize/1440x810!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2F24%2F48%2Fcb87c2296c8f8900cc9b261d43bf%2F6d2ee855d6b3471a8ab2b06937792747",
                "publishedAt": "2025-04-17T12:14:00Z",
                "content": "WASHINGTON (AP) President Donald Trump slammed Federal Reserve Chair Jerome Powell on Thursday, reiterating his frustration that the Fed has not aggressively cut interest rates and saying that the ce… [+5298 chars]"
            },
            {
                "source": {
                    "id": "al-jazeera-english",
                    "name": "Al Jazeera English"
                },
                "author": "Al Jazeera Staff",
                "title": "Is there life on another planet? Scientists find the strongest evidence yet - Al Jazeera",
                "description": "Near a planet far, far away astronomers have found traces of chemicals that on Earth are only produced by living beings.",
                "url": "https://www.aljazeera.com/news/2025/4/17/is-there-life-on-another-planet-scientists-find-the-strongest-evidence-yet",
                "urlToImage": "https://www.aljazeera.com/wp-content/uploads/2025/04/54167157727_9c8df56be1_o-1744886955.jpg?resize=1200%2C630",
                "publishedAt": "2025-04-17T12:06:10Z",
                "content": "Astronomers have found the clearest evidence yet that life might exist beyond the solar system, from the atmosphere of a planet 124 light years away from Earth, setting off rare excitement tinged wit… [+6694 chars]"
            },
            {
                "source": {
                    "id": "the-wall-street-journal",
                    "name": "The Wall Street Journal"
                },
                "author": "WSJ",
                "title": "Lebanon’s Government Arrests Militants, Asserting Its Authority - WSJ",
                "description": null,
                "url": "https://www.wsj.com/world/middle-east/lebanons-government-arrests-militants-asserting-its-authority-631a0ae9",
                "urlToImage": null,
                "publishedAt": "2025-04-17T11:18:00Z",
                "content": null
            },
            {
                "source": {
                    "id": "cnn",
                    "name": "CNN"
                },
                "author": "Neha Mukherjee",
                "title": "Measles costs are accumulating as funding cuts threaten the outbreak response - CNN",
                "description": "Measles cases have surpassed 650 in an ongoing multistate outbreak, but federal funding cuts could threaten the response.",
                "url": "https://www.cnn.com/2025/04/17/health/measles-response-funding-cuts/index.html",
                "urlToImage": "https://media.cnn.com/api/v1/images/stellar/prod/ap25099777459442.jpg?c=16x9&q=w_800,c_fill",
                "publishedAt": "2025-04-17T11:00:00Z",
                "content": "Measles cases have surpassed 650 in an ongoing multistate outbreak, but federal funding cuts could threaten the response.\r\nI think that we are scraping to find the resources and personnel needed to p… [+4124 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "WFAA.com"
                },
                "author": "Jaden Edison (Texas Tribune)",
                "title": "In historic first, Texas House approves private school voucher program - WFAA",
                "description": "The bill would let families use taxpayer dollars for their children’s private schooling. Lawmakers also signed a $7.7 billion package to boost public school funding.",
                "url": "https://www.wfaa.com/article/news/education/texas-house-voucher-bill-passes-house-school-funding-boost/287-11d44bfc-9536-457a-8bf9-9bafda7c4337",
                "urlToImage": "https://media.wfaa.com/assets/WFAA/images/455afa1c-aa52-4909-9dd6-1dbe76f26585/20250416T161936/455afa1c-aa52-4909-9dd6-1dbe76f26585_1140x641.jpg",
                "publishedAt": "2025-04-17T10:23:00Z",
                "content": "AUSTIN, Texas The Texas House gave initial approval early Thursday to a bill that would create a $1 billion private school voucher program, crossing a historic milestone and bringing Gov. Greg Abbott… [+11097 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "Discoverwildlife.com"
                },
                "author": "daniel.graham@ourmedia.co.uk",
                "title": "\"It's like finding a diamond\": 16-million-year-old animal found encased in amber in the Caribbean - BBC Wildlife Magazine",
                "description": "The remarkable discovery offers fresh insights into the history of one of the world’s most elusive animal groups, say scientists.",
                "url": "https://www.discoverwildlife.com/animal-facts/insects-invertebrates/basiceros-enana-amber-caribbean",
                "urlToImage": "https://c02.purpledshub.com/uploads/sites/62/2025/04/Basiceros-enana.jpeg?w=1200",
                "publishedAt": "2025-04-17T10:17:34Z",
                "content": "Scientists who found an ancient insect enveloped in 16-million-year-old amber in the Dominican Republic say it is the first-ever fossil of a dirt ant (a group of ants) from the Caribbean.\r\nThelong-ex… [+4666 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "Space.com"
                },
                "author": "Daisy Dobrijevic",
                "title": "Where to see the Lyrid meteor shower 2025. Top viewing tips - Space",
                "description": "The Lyrid meteor shower is active between April 16 and April 25. Here's how to see it.",
                "url": "https://www.space.com/where-to-see-lyrid-meteor-shower-2025-top-viewing-tips",
                "urlToImage": "https://cdn.mos.cms.futurecdn.net/5oiMVLXfc9fVrdVgWpoU5b.jpg",
                "publishedAt": "2025-04-17T10:00:00Z",
                "content": "The Lyrid meteor shower has returned, and some lucky skywatchers are already catching glimpses of these bright meteors as they streak across the sky.\r\nThe Lyrids appear to radiate from the constellat… [+2020 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "NPR"
                },
                "author": "",
                "title": "Stem cells to treat Parkinson’s? 2 small studies hint at success : Shots - Health News - NPR",
                "description": "Two new studies suggest that Parkinson's disease can potentially be treated with stem cells placed in a patient's brain.",
                "url": "https://www.npr.org/sections/shots-health-news/2025/04/17/g-s1-60796/parkinsons-stem-cell-transplant-treatment",
                "urlToImage": "https://npr.brightspotcdn.com/dims3/default/strip/false/crop/3840x2160+0+0/resize/1400/quality/100/format/jpeg/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F69%2F10%2F89fdb1434387bcec01f8f99bcfd4%2Fgettyimages-2012473987.jpg",
                "publishedAt": "2025-04-17T10:00:00Z",
                "content": "Patients suffering from Parkinson's disease may soon benefit from a powerful treatment option: stem-cell transplants.\r\nIn a pair of small studies designed primarily to test safety, two teams of resea… [+5235 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "ESPN Press Room"
                },
                "author": "Julie McKay",
                "title": "Legendary ESPN Broadcaster Lee Corso to Work His Final College GameDay Show on August 30 – Week 1 of the 2025 College Football Season - ESPN Press Room",
                "description": "Videos: The history of Lee Corso’s headgear picks; Most memorable headgear picks Rece Davis first-person via ESPN Front Row: https://bit.ly/3RmhHtL Photos via ESPN Images After entertaining fans for 3",
                "url": "https://espnpressroom.com/us/press-releases/2025/04/legendary-espn-broadcaster-lee-corso-to-work-his-final-college-gameday-show-on-august-30-week-1-of-the-2025-college-football-season/",
                "urlToImage": "https://espnpressroom.com/us/files/2025/04/LC-4.25-EXTERNAL-FINAL.png",
                "publishedAt": "2025-04-17T09:50:41Z",
                "content": "Videos: The history of Lee Corsos headgear picks; Most memorable headgear picks\r\nRece Davis first-person via ESPN Front Row: https://bit.ly/3RmhHtL\r\nPhotos via ESPN Images\r\n<ul><li>After entertaining… [+8605 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "BBC News"
                },
                "author": null,
                "title": "Campaigners warn of Supreme Court ruling impact on trans people - BBC",
                "description": "Campaigners say the trans community is now worried that \"people are coming after their right to exist\" as a result of the ruling.",
                "url": "https://www.bbc.com/news/articles/cy8q55d27lgo",
                "urlToImage": "https://ichef.bbci.co.uk/news/1024/branded_news/efa9/live/bc374130-1b65-11f0-8a1e-3ff815141b98.jpg",
                "publishedAt": "2025-04-17T09:46:46Z",
                "content": "Paul O'Hare\r\nKerrie Meyer had gender reassignment surgery at the age of 72\r\nCampaigners have warned the UK Supreme Court's ruling on the definition of a woman could have \"dire consequences\" for the s… [+6358 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "BBC News"
                },
                "author": null,
                "title": "Erik and Lyle Menendez resentencing hearing to begin in Los Angeles - BBC",
                "description": "The pair hope to take a step towards release - decades after killing their parents in a high-profile US case.",
                "url": "https://www.bbc.com/news/articles/c9ve7jlywpro",
                "urlToImage": "https://ichef.bbci.co.uk/news/1024/branded_news/ff13/live/5fa3c480-1b05-11f0-b731-c780c85cb550.jpg",
                "publishedAt": "2025-04-17T09:45:14Z",
                "content": "Christal Hayes and Regan MorrisReporting from\r\nLos Angeles, California \r\nAfter decades spent in prison by Erik and Lyle Menendez - and months of contentious court fights - a judge will hear arguments… [+7299 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "WTOP"
                },
                "author": "Mike Murillo",
                "title": "Wife of mistakenly deported Maryland man responds to release of protective order filing - WTOP",
                "description": "The Department of Homeland Security showed court filings for a protective order against Kilmar Abrego Garcia who was deported to a prison in El Salvador.",
                "url": "https://wtop.com/maryland/2025/04/wife-of-mistakenly-deported-maryland-man-responds-to-release-of-protective-order-filing/",
                "urlToImage": "https://wtop.com/wp-content/uploads/2025/04/Maryland_Deportation_Error_96495-scaled.jpg",
                "publishedAt": "2025-04-17T09:27:10Z",
                "content": "The Department of Homeland Security, in a post on X on Wednesday, showed court filings for a protective order against a man from Maryland who was wrongly deported to a notorious prison in El Salvador… [+2897 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "NPR"
                },
                "author": "Jonathan Lambert",
                "title": "Destroying endangered species' habitat wouldn't count as 'harm' under proposed Trump rule - NPR",
                "description": "The Trump administration is reinterpreting a key word in the Endangered Species Act that could have big consequences for the habitats of species at risk.",
                "url": "https://www.npr.org/2025/04/17/nx-s1-5366814/endangered-species-act-change-harm-trump-rule",
                "urlToImage": "https://npr.brightspotcdn.com/dims3/default/strip/false/crop/4354x2449+0+232/resize/1400/quality/100/format/jpeg/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F93%2Fd4%2F2c5c05264b2ea230b3b8df7227f5%2Fgettyimages-1417483742.jpg",
                "publishedAt": "2025-04-17T09:00:55Z",
                "content": "The Trump administration is proposing to significantly limit the Endangered Species Act's power to preserve crucial habitats by changing the definition of one word: harm.\r\nOn Wednesday, the administr… [+2551 chars]"
            }
        ]
    }

    ```

4. `/news/headlines/source/{source_id}`

    **_Request_**
    ```bash
    curl --location --request GET 'http://localhost:8000/news/headlines/source/the-verge' \
    --header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vLWNsaWVudCIsImV4cCI6MTc0NDk5NDUzOC45NTQyODJ9.jn9qGVFm9NqPOvivNKW91Ks8OCdjWjZOxULCkchkBtM' \
    --header 'Accept: */*' \
    --header 'Host: localhost:8000' \
    --header 'Connection: keep-alive'
    ```

    **_Response_**
    ```json
    {
        "success": true,
        "message": "Fetched headlines successfully",
        "data": [
            {
                "source": {
                    "id": "the-verge",
                    "name": "The Verge"
                },
                "author": "Charles Pulliam-Moore",
                "title": "Sinners is a breathtakingly horrific ode to Black mythology",
                "description": "Ryan Coogler’s Sinners — out April 18th — is a cinematic triumph with Black history and movie magic running through its veins.",
                "url": "http://www.theverge.com/movie-reviews/649188/sinners-review",
                "urlToImage": "https://platform.theverge.com/wp-content/uploads/sites/2/2025/04/rev-1-GRC-14350_High_Res_JPEG.jpeg?quality=90&strip=all&crop=0%2C5.1975692906829%2C100%2C89.604861418634&w=1200",
                "publishedAt": "2025-04-17T14:00:00Z",
                "content": "Sinners is a breathtakingly horrific ode to Black mythology\r\nRyan Cooglers latest feature feels like a classic southern vampire tale with movie magic running through its veins.\r\nSinners is a breathta… [+7119 chars]"
            },
            {
                "source": {
                    "id": "the-verge",
                    "name": "The Verge"
                },
                "author": "Nilay Patel",
                "title": "How shippers are trying to keep up with Trump’s trade war",
                "description": "Flexport CEO Ryan Petersen offers an air-, sea-, and ground-level view on the tariff chaos.",
                "url": "http://www.theverge.com/decoder-podcast-with-nilay-patel/649986/trump-tariffs-china-ryan-petersen-flexport-interview",
                "urlToImage": "https://platform.theverge.com/wp-content/uploads/sites/2/2025/04/STKS488_TARIFFS_CVirginia_C.jpg?quality=90&strip=all&crop=0%2C10.732984293194%2C100%2C78.534031413613&w=1200",
                "publishedAt": "2025-04-17T14:00:00Z",
                "content": "How shippers are trying to keep up with Trumps trade war\r\nFlexport CEO Ryan Petersen offers an air-, sea-, and ground-level view on the tariff chaos. \r\nHow shippers are trying to keep up with Trumps … [+4759 chars]"
            },
            {
                "source": {
                    "id": "the-verge",
                    "name": "The Verge"
                },
                "author": "Ash Parrish",
                "title": "Nintendo shows off Mario Kart World’s new courses, items, and open world features",
                "description": "Nintendo has held a Mario Kart World direct showing off more gameplay of the Switch 2 launch title.",
                "url": "http://www.theverge.com/news/649138/mario-kart-world-direct-nintendo-switch-2-gameplay",
                "urlToImage": "https://platform.theverge.com/wp-content/uploads/sites/2/2025/04/NintendoSwitch2_MarioKartWorld_SCRN_GrandPrix_01_a1f79d.png?quality=90&strip=all&crop=0%2C3.4613147178592%2C100%2C93.077370564282&w=1200",
                "publishedAt": "2025-04-17T13:38:47Z",
                "content": "Its Mario Karts world and were all driving in it.\r\nIts Mario Karts world and were all driving in it.\r\nNintendo is possibly hoping to steer the narrative regarding the Switch 2 back in a positive dire… [+2280 chars]"
            },
            {
                "source": {
                    "id": "the-verge",
                    "name": "The Verge"
                },
                "author": "Victoria Song",
                "title": "Strava acquires massively popular Runna app",
                "description": "Popular fitness app Strava announces it’s acquiring the Runna app. Financial details weren’t shared, but nothing changes for Strava or Runna users right away.",
                "url": "http://www.theverge.com/tech/648075/strava-runna-acquisition-running-fitness-tech",
                "urlToImage": "https://platform.theverge.com/wp-content/uploads/sites/2/2025/04/Strava-Runna-Landscape.png?quality=90&strip=all&crop=0%2C13.753523962948%2C100%2C72.492952074104&w=1200",
                "publishedAt": "2025-04-17T05:00:00Z",
                "content": "Nothings changing straight out of the gate, but Strava CEO Michael Martin says This isnt an efficiency play.\r\nNothings changing straight out of the gate, but Strava CEO Michael Martin says This isnt … [+5026 chars]"
            },
            {
                "source": {
                    "id": "the-verge",
                    "name": "The Verge"
                },
                "author": "Lauren Feiner, Alex Heath",
                "title": "FTC v. Meta live: the latest from the battle over Instagram and WhatsApp",
                "description": "The Federal Trade Commission is facing Meta in DC District Court over claims it illegally monopolized personal social networks in buying Instagram and WhatsApp.",
                "url": "http://www.theverge.com/news/646809/ftc-v-meta-antitrust-monopoly-trial-instagram-whatsapp",
                "urlToImage": "https://platform.theverge.com/wp-content/uploads/sites/2/2025/04/STKS507_FTCxMETA_ANTITRUST_CVIRGINIA_2_B.jpg?quality=90&strip=all&crop=0%2C10.732984293194%2C100%2C78.534031413613&w=1200",
                "publishedAt": "2025-04-14T13:46:45Z",
                "content": "The long-awaited antitrust trial between Meta and the Federal Trade Commission kicked off on April 14th. Over about two months, DC District Court Chief Judge James Boasberg is hearing arguments about… [+12076 chars]"
            }
        ]
    }

    ```

5. `/news/headlines/filter`

    **_Request_**
    ```bash
    curl --location --request GET 'http://localhost:8000/news/headlines/filter?country=us&source=the-verge' \
    --header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vLWNsaWVudCIsImV4cCI6MTc0NDk5NDUzOC45NTQyODJ9.jn9qGVFm9NqPOvivNKW91Ks8OCdjWjZOxULCkchkBtM' \
    --header 'Accept: */*' \
    --header 'Host: localhost:8000' \
    --header 'Connection: keep-alive'
    ```

    **_Response_**
    ```json
    {
        "success": true,
        "message": "Fetched headlines successfully",
        "data": [
            {
                "source": {
                    "id": "the-verge",
                    "name": "The Verge"
                },
                "author": "Ash Parrish",
                "title": "Nintendo shows off Mario Kart World’s new courses, items, and open world features - The Verge",
                "description": "Nintendo has held a Mario Kart World direct showing off more gameplay of the Switch 2 launch title.",
                "url": "https://www.theverge.com/news/649138/mario-kart-world-direct-nintendo-switch-2-gameplay",
                "urlToImage": "https://platform.theverge.com/wp-content/uploads/sites/2/2025/04/NintendoSwitch2_MarioKartWorld_SCRN_GrandPrix_01_a1f79d.png?quality=90&strip=all&crop=0%2C3.4613147178592%2C100%2C93.077370564282&w=1200",
                "publishedAt": "2025-04-17T13:38:47Z",
                "content": "Its Mario Karts world and were all driving in it.\r\nIts Mario Karts world and were all driving in it.\r\nNintendo is possibly hoping to steer the narrative regarding the Switch 2 back in a positive dire… [+2280 chars]"
            }
        ]
    }
    ```