# Generated by Django 5.1.3 on 2024-11-26 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0091_alter_personstatus_is_active"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="commonsdivisionvote",
            options={"ordering": ["-modified_at"]},
        ),
        migrations.AlterModelOptions(
            name="lordsdivisionvote",
            options={"ordering": ["-modified_at"]},
        ),
        migrations.RenameField(
            model_name="addresstype",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="addresstype",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="bill",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="bill",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billagent",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billagent",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billpublication",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billpublication",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billpublicationlink",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billpublicationlink",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billpublicationtype",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billpublicationtype",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billsponsor",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billsponsor",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billstage",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billstage",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billstagesitting",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billstagesitting",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billstagetype",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billstagetype",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billtype",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billtype",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="billtypecategory",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="billtypecategory",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="committee",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="committee",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="committeechair",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="committeechair",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="committeemember",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="committeemember",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="commonsdivision",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="commonsdivision",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="commonsdivisionvote",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="commonsdivisionvote",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="constituency",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="constituency",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="constituencyboundary",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="constituencyboundary",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="constituencycandidate",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="constituencycandidate",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="constituencyrepresentative",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="constituencyrepresentative",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="constituencyresult",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="constituencyresult",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="constituencyresultdetail",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="constituencyresultdetail",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="contestedelection",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="contestedelection",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="country",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="country",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="divisionvotetype",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="divisionvotetype",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="election",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="election",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="electionnationalresult",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="electionnationalresult",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="electiontype",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="electiontype",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="experience",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="experience",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="experiencecategory",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="experiencecategory",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="house",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="house",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="housemembership",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="housemembership",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="lordsdivision",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="lordsdivision",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="lordsdivisionvote",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="lordsdivisionvote",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="lordstype",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="lordstype",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="maidenspeech",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="maidenspeech",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="memberportrait",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="memberportrait",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="organisation",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="organisation",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="parliamentarysession",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="parliamentarysession",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="party",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="party",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="partyaffiliation",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="partyaffiliation",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="partyalsoknownas",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="partyalsoknownas",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="partytheme",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="partytheme",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="person",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="person",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="personalsoknownas",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="personalsoknownas",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="personstatus",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="personstatus",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="physicaladdress",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="physicaladdress",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="postholder",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="postholder",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="registeredinterest",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="registeredinterest",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="registeredinterestcategory",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="registeredinterestcategory",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="subjectofinterest",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="subjectofinterest",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="subjectofinterestcategory",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="subjectofinterestcategory",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="town",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="town",
            old_name="modified_on",
            new_name="modified_at",
        ),
        migrations.RenameField(
            model_name="webaddress",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="webaddress",
            old_name="modified_on",
            new_name="modified_at",
        ),
    ]
