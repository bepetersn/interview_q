from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_description_question_notes_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questionlog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_logs', to=settings.AUTH_USER_MODEL),
        ),
    ]
