from django.test import TestCase
from django.db import IntegrityError

from pdfuploader.models import Archive


class ArchiveModelsTestCase(TestCase):
    def setUp(self):
        self.archive_1 = Archive.objects.create(
            title="lion",
            locked=False,
            hash_data="0123ABC",
            author="Fake Authorson",
            produced_by="OpenWriter",
            url="www.makemoretestsorneh.com",
            pages="222",
            size=22222
        )
        self.archive_1.save()
        # the next object is intended to raise validators
        self.defective_archive = Archive.objects.create(title="")
        self.defective_archive.save()

    def test_str_representation(self):
        self.assertEqual(str(self.archive_1),
                         self.archive_1.title)

    def test_verbose_names(self):  # noQA; coverage purposes
        self.assertEqual(str(self.archive_1._meta.verbose_name), "archive")
        self.assertEqual(str(self.archive_1._meta.verbose_name_plural),
                         "archives"
                         )

    def test_repeated_hash(self):
        """hash is unique or IntegrityError:
        duplicate key value violates unique constraint
        pdfuploader_archive_hash_data_key DETAIL:
        Key (hash_data)=() already exists."""
        with self.assertRaises(IntegrityError):
            repeated_hash_archive = Archive.objects.create(hash_data="0123ABC")
            repeated_hash_archive.save()
