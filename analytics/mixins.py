from .signals import object_viewed_signal


class ObjectViewMixin(object):
    def dispatch(self, request, *args, **kwargs):
        print('printing self:', self)
        try:
            instance = self.get_object()
        except:
            instance = None
        if instance is not None:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return super(ObjectViewMixin, self).dispatch(request, *args, **kwargs)
