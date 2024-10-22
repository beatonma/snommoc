from crawlers.parliamentdotuk.tasks.lda.schema import CommonsDivision, Vote

EXAMPLE_COMMONS_DIVISION = CommonsDivision.model_validate(
    {
        "_about": "http://data.parliament.uk/resources/1171292",
        "AbstainCount": [{"_value": "0"}],
        "AyesCount": [{"_value": "222"}],
        "DeferredVote": False,
        "Didnotvotecount": [{"_value": "0"}],
        "Errorvotecount": [{"_value": "0"}],
        "Margin": [{"_value": "91"}],
        "Noesvotecount": [{"_value": "313"}],
        "Noneligiblecount": [{"_value": "0"}],
        "Suspendedorexpelledvotescount": [{"_value": "0"}],
        "date": {"_value": "2020-01-16", "_datatype": "dateTime"},
        "divisionNumber": "15",
        "isPrimaryTopicOf": "http://eldaddp.azurewebsites.net/commonsdivisions/id/1171292.json",
        "legislature": ["http://data.parliament.uk/terms/25259"],
        "session": ["2017/19", "http://data.parliament.uk/resources/730830"],
        "title": "The Queen's Speech: Jeremy Corbyn's amendment (c) ",
        "uin": "CD:2020-01-16:750",
        "vote": [
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/1",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/163",
                        "label": {"_value": "Biography information for Stephen Timms"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Stephen Timms"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/10",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4420",
                        "label": {"_value": "Biography information for Gavin Newlands"},
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Gavin Newlands"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/100",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/415",
                        "label": {
                            "_value": "Biography information for Fabian Hamilton"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Fabian Hamilton"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/101",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/1533",
                        "label": {
                            "_value": "Biography information for Dame Diana Johnson"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Dame Diana Johnson"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/102",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/1506",
                        "label": {"_value": "Biography information for Andrew Gwynne"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Andrew Gwynne"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/103",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4443",
                        "label": {"_value": "Biography information for Carol Monaghan"},
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Carol Monaghan"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/104",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4873",
                        "label": {"_value": "Biography information for Rachel Hopkins"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Rachel Hopkins"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/105",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4408",
                        "label": {
                            "_value": "Biography information for Christian Matheson"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Christian Matheson"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/106",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4120",
                        "label": {"_value": "Biography information for Kate Green"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Kate Green"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/107",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4656",
                        "label": {"_value": "Biography information for Layla Moran"},
                    }
                ],
                "memberParty": "Liberal Democrat",
                "memberPrinted": {"_value": "Layla Moran"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/108",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4653",
                        "label": {
                            "_value": "Biography information for Mr Stephen Morgan"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Mr Stephen Morgan"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/109",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4125",
                        "label": {
                            "_value": "Biography information for Catherine McKinnell"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Catherine McKinnell"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/11",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4654",
                        "label": {"_value": "Biography information for Matt Rodda"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Matt Rodda"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/110",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4418",
                        "label": {"_value": "Biography information for Justin Madders"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Justin Madders"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/111",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4253",
                        "label": {"_value": "Biography information for Seema Malhotra"},
                    }
                ],
                "memberParty": "Labour (Co-op)",
                "memberPrinted": {"_value": "Seema Malhotra"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/112",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4631",
                        "label": {"_value": "Biography information for Sarah Jones"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Sarah Jones"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/113",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4633",
                        "label": {"_value": "Biography information for Paul Girvan"},
                    }
                ],
                "memberParty": "Democratic Unionist Party",
                "memberPrinted": {"_value": "Paul Girvan"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/114",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4359",
                        "label": {
                            "_value": "Biography information for Stephen Kinnock"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Stephen Kinnock"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/115",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4772",
                        "label": {
                            "_value": "Biography information for Kenny MacAskill"
                        },
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Kenny MacAskill"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/116",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4029",
                        "label": {
                            "_value": "Biography information for Lilian Greenwood"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Lilian Greenwood"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/117",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/206",
                        "label": {"_value": "Biography information for Mr David Lammy"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Mr David Lammy"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/118",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4500",
                        "label": {"_value": "Biography information for Clive Lewis"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Clive Lewis"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/119",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4437",
                        "label": {
                            "_value": "Biography information for Anne McLaughlin"
                        },
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Anne McLaughlin"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/12",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4755",
                        "label": {"_value": "Biography information for Mick Whitley"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Mick Whitley"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/120",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4126",
                        "label": {"_value": "Biography information for Mary Glindon"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Mary Glindon"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/121",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/1541",
                        "label": {"_value": "Biography information for Nia Griffith"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Nia Griffith"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/122",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4403",
                        "label": {"_value": "Biography information for Chris Law"},
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Chris Law"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/123",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4139",
                        "label": {"_value": "Biography information for Ian Lavery"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Ian Lavery"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/124",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/193",
                        "label": {
                            "_value": "Biography information for Siobhain McDonagh"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Siobhain McDonagh"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/125",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/1524",
                        "label": {"_value": "Biography information for Meg Hillier"},
                    }
                ],
                "memberParty": "Labour (Co-op)",
                "memberPrinted": {"_value": "Meg Hillier"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/126",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/140",
                        "label": {
                            "_value": "Biography information for Dame Margaret Hodge"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Dame Margaret Hodge"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/127",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/150",
                        "label": {
                            "_value": "Biography information for Ms Harriet Harman"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Ms Harriet Harman"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/128",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4569",
                        "label": {"_value": "Biography information for Jim McMahon"},
                    }
                ],
                "memberParty": "Labour (Co-op)",
                "memberPrinted": {"_value": "Jim McMahon"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/129",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4435",
                        "label": {
                            "_value": "Biography information for Patricia Gibson"
                        },
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Patricia Gibson"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/13",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/429",
                        "label": {"_value": "Biography information for Derek Twigg"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Derek Twigg"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/130",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4393",
                        "label": {
                            "_value": "Biography information for Stuart C McDonald"
                        },
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Stuart C McDonald"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/131",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/178",
                        "label": {"_value": "Biography information for John McDonnell"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "John McDonnell"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/132",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4501",
                        "label": {"_value": "Biography information for Gerald Jones"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Gerald Jones"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/133",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4466",
                        "label": {"_value": "Biography information for Peter Grant"},
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Peter Grant"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/134",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4603",
                        "label": {
                            "_value": "Biography information for Preet Kaur Gill"
                        },
                    }
                ],
                "memberParty": "Labour (Co-op)",
                "memberPrinted": {"_value": "Preet Kaur Gill"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/135",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4632",
                        "label": {"_value": "Biography information for Anna McMorrin"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Anna McMorrin"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/136",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4365",
                        "label": {"_value": "Biography information for Neil Gray"},
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Neil Gray"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/137",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4480",
                        "label": {"_value": "Biography information for Carolyn Harris"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Carolyn Harris"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/138",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/146",
                        "label": {"_value": "Biography information for Barry Gardiner"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Barry Gardiner"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/139",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4277",
                        "label": {
                            "_value": "Biography information for Mrs Emma Lewell-Buck"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Mrs Emma Lewell-Buck"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/14",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4436",
                        "label": {"_value": "Biography information for Cat Smith"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Cat Smith"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/140",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4473",
                        "label": {"_value": "Biography information for Louise Haigh"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Louise Haigh"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/141",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4432",
                        "label": {"_value": "Biography information for Patrick Grady"},
                    }
                ],
                "memberParty": "Scottish National Party",
                "memberPrinted": {"_value": "Patrick Grady"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/142",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/1438",
                        "label": {"_value": "Biography information for Mr Kevan Jones"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Mr Kevan Jones"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/143",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4243",
                        "label": {"_value": "Biography information for Dan Jarvis"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Dan Jarvis"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/144",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/1510",
                        "label": {
                            "_value": "Biography information for Edward Miliband"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Edward Miliband"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/145",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/3914",
                        "label": {
                            "_value": "Biography information for Shabana Mahmood"
                        },
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Shabana Mahmood"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/146",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4511",
                        "label": {"_value": "Biography information for Dr Rupa Huq"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Dr Rupa Huq"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/147",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/4458",
                        "label": {"_value": "Biography information for Conor McGinn"},
                    }
                ],
                "memberParty": "Labour",
                "memberPrinted": {"_value": "Conor McGinn"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
            {
                "_about": "http://data.parliament.uk/resources/1171292/vote/148",
                "member": [
                    {
                        "_about": "http://data.parliament.uk/members/3943",
                        "label": {
                            "_value": "Biography information for Jonathan Edwards"
                        },
                    }
                ],
                "memberParty": "Plaid Cymru",
                "memberPrinted": {"_value": "Jonathan Edwards"},
                "type": "http://data.parliament.uk/schema/parl#AyeVote",
            },
        ],
    }
)

EXAMPLE_LORDS_VOTE = {
    "_about": "http://data.parliament.uk/resources/714002/vote/1",
    "member": ["http://data.parliament.uk/resources/members/api/lords/id/3898"],
    "memberParty": "Crossbench",
    "memberRank": "Lord",
    "memberTitle": "Aberdare",
    "type": "http://data.parliament.uk/schema/parl#ContentVote",
}
EXAMPLE_COMMONS_VOTE = Vote.model_validate(
    {
        "_about": "http://data.parliament.uk/resources/1171292/vote/103",
        "member": [
            {
                "_about": "http://data.parliament.uk/members/4443",
                "label": {"_value": "Biography information for Carol Monaghan"},
            }
        ],
        "memberParty": "Scottish National Party",
        "memberPrinted": {"_value": "Carol Monaghan"},
        "type": "http://data.parliament.uk/schema/parl#AyeVote",
    }
)

EXAMPLE_COMMONS_VOTE_AYE = Vote.model_validate(
    {
        "_about": "http://data.parliament.uk/resources/1171292/vote/10",
        "member": [
            {
                "_about": "http://data.parliament.uk/members/4420",
                "label": {"_value": "Biography information for Gavin Newlands"},
            }
        ],
        "memberParty": "Scottish National Party",
        "memberPrinted": {"_value": "Gavin Newlands"},
        "type": "http://data.parliament.uk/schema/parl#AyeVote",
    }
)
EXAMPLE_COMMONS_VOTE_NO = Vote.model_validate(
    {
        "_about": "http://data.parliament.uk/resources/1171292/vote/223",
        "member": [
            {
                "_about": "http://data.parliament.uk/members/4118",
                "label": {"_value": "Biography information for Julian Smith"},
            }
        ],
        "memberParty": "Conservative",
        "memberPrinted": {"_value": "Julian Smith"},
        "type": "http://data.parliament.uk/schema/parl#NoVote",
    }
)

# Complete data (with trimmed votes) from https://lda.data.parliament.uk/commonsdivisions/id/1180266.json
EXAMPLE_COMMONS_DIVISION_COMPLETE = {
    "format": "linked-data-api",
    "version": "0.2",
    "result": {
        "_about": "http://eldaddp.azurewebsites.net/commonsdivisions/id/1180266.json",
        "definition": "http://eldaddp.azurewebsites.net/meta/commonsdivisions/id/_ddpid.json",
        "extendedMetadataVersion": "http://eldaddp.azurewebsites.net/commonsdivisions/id/1180266.json?_metadata=all",
        "primaryTopic": {
            "_about": "http://data.parliament.uk/resources/1180266",
            "AbstainCount": [{"_value": "0"}],
            "AyesCount": [{"_value": "236"}],
            "DeferredVote": False,
            "Didnotvotecount": [{"_value": "0"}],
            "Errorvotecount": [{"_value": "0"}],
            "Margin": [{"_value": "86"}],
            "Noesvotecount": [{"_value": "322"}],
            "Noneligiblecount": [{"_value": "0"}],
            "Suspendedorexpelledvotescount": [{"_value": "0"}],
            "date": {"_value": "2020-02-25", "_datatype": "dateTime"},
            "divisionNumber": "35",
            "isPrimaryTopicOf": "http://eldaddp.azurewebsites.net/commonsdivisions/id/1180266.json",
            "legislature": ["http://data.parliament.uk/terms/25259"],
            "session": ["2017/19", "http://data.parliament.uk/resources/730830"],
            "title": "Opposition day debate on tax avoidance and evasion: Mr Corbyn's motion ",
            "uin": "CD:2020-02-25:770",
            "vote": [
                {
                    "_about": "http://data.parliament.uk/resources/1180266/vote/1",
                    "member": [
                        {
                            "_about": "http://data.parliament.uk/members/4479",
                            "label": {
                                "_value": "Biography information for Nick Thomas-Symonds"
                            },
                        }
                    ],
                    "memberParty": "Labour",
                    "memberPrinted": {"_value": "Nick Thomas-Symonds"},
                    "type": "http://data.parliament.uk/schema/parl#AyeVote",
                },
                {
                    "_about": "http://data.parliament.uk/resources/1180266/vote/10",
                    "member": [
                        {
                            "_about": "http://data.parliament.uk/members/4786",
                            "label": {
                                "_value": "Biography information for Zarah Sultana"
                            },
                        }
                    ],
                    "memberParty": "Labour",
                    "memberPrinted": {"_value": "Zarah Sultana"},
                    "type": "http://data.parliament.uk/schema/parl#AyeVote",
                },
                {
                    "_about": "http://data.parliament.uk/resources/1180266/vote/100",
                    "member": [
                        {
                            "_about": "http://data.parliament.uk/members/4765",
                            "label": {
                                "_value": "Biography information for Wendy Chamberlain"
                            },
                        }
                    ],
                    "memberParty": "Liberal Democrat",
                    "memberPrinted": {"_value": "Wendy Chamberlain"},
                    "type": "http://data.parliament.uk/schema/parl#AyeVote",
                },
            ],
        },
        "type": [
            "http://purl.org/linked-data/api/vocab#ItemEndpoint",
            "http://purl.org/linked-data/api/vocab#Page",
        ],
    },
}

EXAMPLE_COMMONS_DIVISIONS_LIST = {
    "format": "linked-data-api",
    "version": "0.2",
    "result": {
        "_about": "http://eldaddp.azurewebsites.net/commonsdivisions.json",
        "definition": "http://eldaddp.azurewebsites.net/meta/commonsdivisions.json",
        "extendedMetadataVersion": "http://eldaddp.azurewebsites.net/commonsdivisions.json?_metadata=all",
        "first": "http://eldaddp.azurewebsites.net/commonsdivisions.json?_page=0",
        "hasPart": "http://eldaddp.azurewebsites.net/commonsdivisions.json",
        "isPartOf": "http://eldaddp.azurewebsites.net/commonsdivisions.json",
        "items": [
            {
                "_about": "http://data.parliament.uk/resources/1180266",
                "date": {"_value": "2020-02-25", "_datatype": "dateTime"},
                "title": "Opposition day debate on tax avoidance and evasion: Mr Corbyn's motion ",
                "uin": "CD:2020-02-25:770",
            },
        ],
        "itemsPerPage": 10,
        "next": "http://eldaddp.azurewebsites.net/commonsdivisions.json?_page=1",
        "page": 0,
        "startIndex": 1,
        "totalResults": 4526,
        "type": [
            "http://purl.org/linked-data/api/vocab#ListEndpoint",
            "http://purl.org/linked-data/api/vocab#Page",
        ],
    },
}
