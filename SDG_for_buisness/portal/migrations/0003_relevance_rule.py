from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0002_seed_db"),
    ]

    operations = [
        migrations.CreateModel(
            name="RelevanceRule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("weight", models.IntegerField()),
                (
                    "answer_option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="relevance_rules",
                        to="portal.answeroption",
                    ),
                ),
                (
                    "sdg_goal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="relevance_rules",
                        to="portal.sdggoal",
                    ),
                ),
            ],
            options={
                "db_table": "relevance_rule",
                "unique_together": {("answer_option", "sdg_goal")},
            },
        ),
    ]
