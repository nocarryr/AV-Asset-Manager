
class Unit(object):
    def __init__(self, value, dpi=None):
        self.value = value
        self.dpi = dpi
    @classmethod
    def unit_from_label(cls, label, dpi=None):
        def is_number(s):
            if '.' in s:
                for _s in s.split('.'):
                    if len(_s) and not _s.isdigit():
                        return False
                return True
            else:
                return s.isdigit()
        def find_cls(_cls):
            cls_label = getattr(_cls, 'unit_label', None)
            if cls_label is not None and label.endswith(cls_label):
                val = label.rstrip(cls_label)
                if not is_number(val):
                    val = 0.
                else:
                    val = float(val)
                return _cls(val, dpi)
            for subcls in _cls.__subclasses__():
                r = find_cls(subcls)
                if r:
                    return r
        if not isinstance(label, basestring):
            return cls(float(label), dpi)
        obj = find_cls(Unit)
        if not obj:
            obj = cls(float(label), dpi)
        return obj
    def to_other(self, other):
        return self.value
    def __add__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        value = other.to_other(self)
        value += self.value
        return self.__class__(value, self.dpi)
    def __radd__(self, other):
        return self + other
    def __iadd__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        value = other.to_other(self)
        self.value += value
        return self
    def __sub__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        value = self.value - other.to_other(self)
        return self.__class__(value, self.dpi)
    def __rsub__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        value = other.to_other(self) - self.value
        return self.__class__(value, self.dpi)
    def __isub__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        self.value -= other.to_other(self)
        return self
    def __mul__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        value = other.to_other(self)
        value *= self.value
        return self.__class__(value, self.dpi)
    def __rmul__(self, other):
        return self * other
    def __imul__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        value = other.to_other(self)
        self.value *= value
        return self
    def __div__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        value = self.value / other.to_other(self)
        return self.__class__(value, self.dpi)
    def __rdiv__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        value = other.to_other(self) / self.value
        return self.__class__(value, self.dpi)
    def __idiv__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        self.value /= other.to_other(self)
        return self
    def __cmp__(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        value = other.to_other(self)
        return cmp(self.value, value)
    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self)
    def __str__(self):
        lbl = getattr(self, 'unit_label', '')
        return '{}{}'.format(self.value, lbl)

class Pixel(Unit):
    unit_label = 'px'
    def to_other(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        if isinstance(other, Pixel):
            return self.value
        elif isinstance(other, Inch):
            if self.value > 0:
                return self.dpi / float(self.value)
            else:
                return self.value
        else:
            return self.value

class Inch(Unit):
    unit_label = 'in'
    def to_other(self, other):
        if not isinstance(other, Unit):
            other = self.unit_from_label(other)
        if isinstance(other, Inch):
            return self.value
        elif isinstance(other, Pixel):
            return self.dpi * float(self.value)
        else:
            return self.value
