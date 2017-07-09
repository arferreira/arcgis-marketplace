import os
import uuid
import zipfile

from pathlib import Path

from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import validators


class CompressField(models.FileField):
    description = _('Compress path')

    default_validators = [
        validators.validate_file_extension,
        validators.validate_zip_compression
    ]

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)

        if value.name:
            outpath = Path(value.path).with_suffix('')

            if not outpath.is_dir() and zipfile.is_zipfile(value):
                with zipfile.ZipFile(value) as zip_file:
                    zip_file.extractall(outpath.as_posix())

        return value


class SymlinkField(models.Field):
    description = _('Symlink path')
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid path"),
    }

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs.setdefault('max_length', 255)
        source = kwargs.pop('source', None)

        if source is None:
            raise exceptions.FieldError(
                "{} requires a 'source' argument".format(
                    self.__class__.__name__
                )
            )

        self.source = source
        super().__init__(verbose_name, name, **kwargs)

    def contribute_to_class(self, cls, name):
        self.symlink_attname = "_symlink_{}".format(name)
        models.signals.post_init.connect(self._save_initial, sender=cls)
        super().contribute_to_class(cls, name)

    def _save_initial(self, sender, instance, **kwargs):
        setattr(
            instance,
            self.symlink_attname,
            Path(getattr(instance, self.attname))
        )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['source'] = self.source

        if kwargs.get('max_length') == 255:
            del kwargs['max_length']

        return name, path, args, kwargs

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        return str(value)

    def get_source_path(self, instance):
        return Path(getattr(instance, self.source).path)

    def pre_save(self, model_instance, add):
        value = Path(getattr(model_instance, self.attname))
        previous = getattr(model_instance, self.symlink_attname)
        path = self.get_source_path(model_instance).with_suffix('')

        if value.is_absolute():
            # Absolute to relative path
            value = value.resolve().relative_to(path)

        # Search the index preview
        file_index_path = next((path / value).glob('**/index.html'), None)

        # Relative path to index
        if file_index_path is not None:
            value = file_index_path.relative_to(path).parent

        # Any changes?
        if previous.resolve() == (path / value).resolve():
            return previous

        # Create the symlink
        symlink = path.parent / uuid.uuid4().hex
        symlink.symlink_to(path.name / value, target_is_directory=True)

        if previous.is_symlink():
            previous.unlink()

        setattr(model_instance, self.attname, symlink.as_posix())
        self._save_initial(model_instance.__class__, model_instance)

        return symlink

    def get_internal_type(self):
        return 'FilePathField'

    def to_python(self, value):
        if value and (Path(value).is_absolute() or os.pardir in value):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value})

        return value
