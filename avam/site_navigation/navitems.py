from django.core.urlresolvers import reverse

page_navitems = {}
navitems_by_href = {}

class NavItem(object):
    def __init__(self, **kwargs):
        self.index = kwargs.get('index')
        self.text = kwargs.get('text')
        href = kwargs.get('href')
        if href is None:
            pattern = kwargs.get('pattern')
            obj = kwargs.get('obj')
            if pattern is not None:
                pkwargs = {}
                if 'args' in kwargs:
                    pkwargs['args'] = kwargs['args']
                if 'kwargs' in kwargs:
                    pkwargs['kwargs'] = kwargs['kwargs']
                href = reverse(pattern, **pkwargs)
            elif obj is not None:
                href = obj.get_absolute_url()
        self.href = href
    @property
    def href(self):
        return getattr(self, '_href', None)
    @href.setter
    def href(self, value):
        old = self.href
        self._href = value
        if old in navitems_by_href:
            del navitems_by_href[old]
        navitems_by_href[value] = self
    @property
    def active(self):
        return getattr(self, '_active', False)
    @active.setter
    def active(self, value):
        self._active = value
        if self.active:
            for item in navitems_by_href.values():
                if item is self:
                    continue
                item.active = False
    def __str__(self):
        return '{0} ({1})'.format(self.text, self.href)

def add_page_navitem(nav_item=None, **kwargs):
    global page_navitems
    if nav_item is None:
        nav_item = NavItem(**kwargs)
    if nav_item.index is None:
        if not len(page_navitems):
            nav_item.index = 0
        else:
            nav_item.index = max(page_navitems.keys()) + 1
    page_navitems[nav_item.index] = nav_item
    return nav_item

def build_static_navitems():
    add_page_navitem(text='Home', pattern='home')
    add_page_navitem(text='Scan Tag', pattern='assettags:assettag_lookup')
    add_page_navitem(text='Print Tags', pattern='assettags:print_tags')
    return page_navitems

def navitem_context(request):
    if not len(page_navitems):
        build_static_navitems()
    d = {}
    active_item = navitems_by_href.get(request.path)
    if active_item is not None:
        active_item.active = True
        d['page_title'] = active_item.text
    items = [page_navitems[key] for key in sorted(page_navitems.keys())]
    d['page_navitems'] = items
    return d
