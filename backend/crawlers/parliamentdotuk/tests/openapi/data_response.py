"""Samples of full JSON responses from """

"""Response is a list with no wrapper object."""
UNWRAPPED_DIVISIONS_RESPONSE = [
    {
        "divisionId": 2684,
        "date": "2022-02-09T00:00:00",
        "number": 2,
        # ...
    },
]

"""Response is a list wrapped by an object with default "items" key."""
WRAPPED_BILLS_RESPONSE = {
    "items": [
        {
            "billId": 2818,
            "shortTitle": "Abolition of Business Rates Bill",
            "currentHouse": "Commons",
            "originatingHouse": "Commons",
            "lastUpdate": "2021-05-04T10:42:08.0579851",
            "billWithdrawn": None,
            "isDefeated": False,
            "billTypeId": 5,
            "introducedSessionId": 35,
            "includedSessionIds": [35],
            "isAct": False,
            "currentStage": {
                "id": 12655,
                "stageId": 7,
                "sessionId": 35,
                "description": "2nd reading",
                "abbreviation": "2R",
                "house": "Commons",
                "stageSittings": [],
                "sortOrder": 2,
            },
        },
        {
            "billId": 2302,
            "shortTitle": "Abortion Bill",
            "currentHouse": "Commons",
            "originatingHouse": "Commons",
            "lastUpdate": "2019-09-17T16:22:10",
            "billWithdrawn": None,
            "isDefeated": False,
            "billTypeId": 5,
            "introducedSessionId": 30,
            "includedSessionIds": [30],
            "isAct": False,
            "currentStage": {
                "id": 15039,
                "stageId": 7,
                "sessionId": 30,
                "description": "2nd reading",
                "abbreviation": "2R",
                "house": "Commons",
                "stageSittings": [],
                "sortOrder": 2,
            },
        },
        {
            "billId": 2556,
            "shortTitle": "Abortion Bill [HL]",
            "currentHouse": "Lords",
            "originatingHouse": "Lords",
            "lastUpdate": "2021-05-05T11:05:17.4984479",
            "billWithdrawn": None,
            "isDefeated": False,
            "billTypeId": 2,
            "introducedSessionId": 35,
            "includedSessionIds": [35],
            "isAct": False,
            "currentStage": {
                "id": 11662,
                "stageId": 2,
                "sessionId": 35,
                "description": "2nd reading",
                "abbreviation": "2R",
                "house": "Lords",
                "stageSittings": [],
                "sortOrder": 2,
            },
        },
    ]
}

"""Response is a list wrapped in an object with a custom key ("publications")"""
WRAPPED_PUBLICATIONS_RESPONSE = {
    "billId": 512,
    "publications": [
        {
            "house": "Commons",
            "id": 2716,
            "title": (
                "Public Administration Select Committee, Constitional Renewal: Draft"
                " Bill and White Paper (HC 499, 2007-08)"
            ),
            "publicationType": {
                "id": 9,
                "name": "Select Committee report",
                "description": (
                    "The following select committee reports have been identified as"
                    " relevant to the debate on the Bill."
                ),
            },
            "displayDate": "2008-06-04T00:00:00",
            "links": [
                {
                    "id": 3096,
                    "title": (
                        "Public Administration Select Committee, Constitional Renewal:"
                        " Draft Bill and White Paper (HC 499, 2007-08)"
                    ),
                    "url": "https://www.publications.parliament.uk/pa/cm200708/cmselect/cmpubadm/499/49902.htm",
                    "contentType": "text/html",
                }
            ],
            "files": [],
        },
    ],
}
