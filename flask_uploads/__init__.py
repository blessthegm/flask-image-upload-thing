import loaders
loader = loaders.Lazy(
    '%s.models' % __name__,
    ('Upload',)
)

import extensions
from .functions import (
    delete,
    save,
    save_file,
    save_images,
)
from .models import Upload


def init(db, Storage, resizer=None):
    extensions.db = db
    extensions.resizer = resizer
    extensions.storage = Storage()
    loader.ready()

__all__ = (
    delete,
    init,
    save,
    save_file,
    save_images,
    Upload,
)
