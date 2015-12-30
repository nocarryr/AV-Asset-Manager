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
    content_type = ContentType.objects.get_for_model(sender)
    if not WatchedModel.objects.filter(content_type=content_type).exists():
        return
    obj = kwargs.get('instance')
    object_update = ObjectUpdate(content_object=obj)
    object_update.save()
