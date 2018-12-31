from django.test import TestCase

from pdfuploader.views import ArchiveDelete, ArchiveUpdate
# , listArchives, stats, tag_detail, tags, uploadpdf, scrap_data, data_organizer

# TODO: ArchiveDetail from urls

class ArchiveModelsTestCase(TestCase):
    def setUp(self):
        pass

    def test_delete(self):  # ArchiveDelete class
        self.assertTrue(True, True)

    def test_update(self):  # ArchiveUpdate class
        pass

    def test_list(self):  # listArchives def
        pass

    def test_stats(self):  # stats def
        self.assertEqual(1, 1)

    def test_tags(self):  # tags def
        pass

    def test_upload_archive(self): # uploadpdf def
        pass

    def test_scrap_data(self): # scrap_data def
        pass

    def test_data_organizer(self):  # data_organizer def
        pass

    def test_md5_forge_from_file(self):  # md5_forge_from_file def
        # uses md5_forge_from_string
        pass

    def test_md5_forge_from_string(self):  # md5_forge_from_string
        pass

if __name__ == '__main__':
      unittest.main()
