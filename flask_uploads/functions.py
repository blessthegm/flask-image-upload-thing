import os
from StringIO import StringIO
import extensions as ext
from .models import Upload


def save_file(name, data):
    name = ext.storage.save(name, data)
    url = ext.storage.url(name)
    ext.db.session.add(Upload(name=name, url=url))
    ext.db.session.commit()


def save_images(name, data, images):
    name = ext.storage.save(name, data).decode('utf-8')
    url = ext.storage.url(name).decode('utf-8')
    upload = Upload(name=name, url=url)

    for size, image in images.iteritems():
        imageio = StringIO()
        image.save(imageio, format=image.ext)
        n = ext.storage.save(
            '%s_%s.%s' % (
                os.path.splitext(name)[0],
                size,
                image.ext
            ),
            imageio
        ).decode('utf-8')
        url = ext.storage.url(n).decode('utf-8')
        setattr(upload, u'%s_name' % size, n)
        setattr(upload, u'%s_url' % size, url)

    ext.db.session.add(upload)
    ext.db.session.commit()


def save(data, name=None):
    if name is None:
        name = data.filename
    data = data.read()
    datafile = StringIO(data)
    if ext.resizer:
        try:
            images = ext.resizer.resize_image(datafile)
        except IOError:
            # Not an image.
            return save_file(name, data)
        save_images(name, data, images)
    else:
        return save_file(name, data)


def delete(upload):
    ext.storage.delete(upload.name)
    if ext.resizer:
        for size in ext.resizer.sizes.iterkeys():
            if getattr(upload, size + '_name'):
                ext.storage.delete(getattr(upload, size + '_name'))
    ext.db.session.delete(upload)
    ext.db.session.commit()
