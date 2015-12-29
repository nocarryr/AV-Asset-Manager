from django.conf import settings

ASSET_TAG_LENGTH = getattr(settings, 'ASSET_TAG_LENGTH', 8)

ASSET_TAG_CHARS = getattr(settings, 'ASSET_TAG_CHARS', '0123456789')

ASSET_TAG_GENERATE_FUNCTION = getattr(settings, 'ASSET_TAG_GENERATE_FUNCTION', None)
