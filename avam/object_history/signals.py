from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from object_history.models import WatchedModel, ObjectUpdate, ObjectChange

@receiver(post_save)
def on_all_post_save(sender, **kwargs):
    if kwargs.get('raw'):
        return
    if issubclass(sender, (WatchedModel, ObjectUpdate, ObjectChange)):
        return
    try:
        content_type = ContentType.objects.get_for_model(sender)
    except RuntimeError as e:
        if 'migrate' in str(e):
            return
    try:
        if not WatchedModel.objects.filter(content_type=content_type).exists():
            return
    except Exception as e:
        if 'no such table' in str(e):
            return
    obj = kwargs.get('instance')
    object_update = ObjectUpdate(content_object=obj)
    object_update.save()
