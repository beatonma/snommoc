from crawlers.parliamentdotuk.tasks.lda import schema

ELECTION_RESULT_DETAIL = schema.ElectionResultDetail.model_validate(
    {
        "_about": "http://data.parliament.uk/resources/382387",
        "candidate": [
            {
                "_about": "http://data.parliament.uk/resources/382387/candidates/1",
                "fullName": {"_value": "Doran, Frank"},
                "numberOfVotes": 16746,
                "order": 1,
                "party": {"_value": "Lab"},
            },
            {
                "_about": "http://data.parliament.uk/resources/382387/candidates/2",
                "fullName": {"_value": "Strathdee, Joanna"},
                "numberOfVotes": 8385,
                "order": 2,
                "party": {"_value": "SNP"},
            },
            {
                "_about": "http://data.parliament.uk/resources/382387/candidates/3",
                "fullName": {"_value": "Chapman, Kristian"},
                "numberOfVotes": 7001,
                "order": 3,
                "party": {"_value": "LD"},
            },
            {
                "_about": "http://data.parliament.uk/resources/382387/candidates/4",
                "fullName": {"_value": "Whyte, Stewart"},
                "numberOfVotes": 4666,
                "order": 4,
                "party": {"_value": "Con"},
            },
            {
                "_about": "http://data.parliament.uk/resources/382387/candidates/5",
                "fullName": {"_value": "Jones, Roy"},
                "numberOfVotes": 635,
                "order": 5,
                "party": {"_value": "BNP"},
            },
            {
                "_about": "http://data.parliament.uk/resources/382387/candidates/6",
                "fullName": {"_value": "Robertson, Ewan"},
                "numberOfVotes": 268,
                "order": 6,
                "party": {"_value": "SSP"},
            },
        ],
        "constituency": {
            "_about": "http://data.parliament.uk/resources/143474",
            "label": {"_value": "Aberdeen North"},
        },
        "election": {
            "_about": "http://data.parliament.uk/resources/382037",
            "label": {"_value": "2010 General Election"},
        },
        "electorate": 64808,
        "isPrimaryTopicOf": "http://eldaddp.azurewebsites.net/electionresults/382387.json",
        "majority": 8361,
        "resultOfElection": "Lab Hold",
        "turnout": 37701,
    }
)
