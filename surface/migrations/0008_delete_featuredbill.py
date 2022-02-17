from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("surface", "0007_auto_20210902_1733"),
        ("repository", "0045_auto_20211124_1731"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="featuredbill",
            name="target",
        ),
        migrations.DeleteModel(
            name="featuredbill",
        ),
    ]
