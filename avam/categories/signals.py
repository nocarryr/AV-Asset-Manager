from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from categories.models import Category, CategoryItem

@receiver(post_save, sender=CategoryItem)
def on_categoryitem_post_save(sender, **kwargs):
    if kwargs.get('raw'):
        return
    if not kwargs.get('created'):
        return
    category_item = kwargs.get('instance')
    category_item.category.add_item_to_links(category_item.content_object)

@receiver(pre_delete)
def on_all_pre_delete(sender, **kwargs):
    if sender is CategoryItem:
        return
    if sender is Category:
        return
    instance = kwargs.get('instance')
    q = CategoryItem.objects.get_for_object(instance)
    q.delete()
