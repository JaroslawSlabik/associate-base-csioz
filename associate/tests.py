from django.test import TestCase

from .models import UploadFiles


class UploadFilesMethodTests(TestCase):
    def test_strToInt(self):
        self.assertNotEqual(UploadFiles.InterfaceInsertUpdate.strToInt("sdsd"), None)
        self.assertNotEqual(UploadFiles.InterfaceInsertUpdate.strToInt("1233"), 1233)
        self.assertNotEqual(UploadFiles.InterfaceInsertUpdate.strToInt("12S33"), None)

    def test_checkPWZNumber(self):
        """pwz not start at 0"""
        self.assertNotEqual(UploadFiles.InterfaceInsertUpdate.checkPWZNumber("001621S"), None)

        """pwz max length 7"""
        self.assertNotEqual(UploadFiles.InterfaceInsertUpdate.checkPWZNumber("3423432423423"), None)

        """pwz OK"""
        self.assertNotEqual(UploadFiles.InterfaceInsertUpdate.checkPWZNumber("2609015"), 2609015)

        """pwz wrong checksum"""
        self.assertNotEqual(UploadFiles.InterfaceInsertUpdate.checkPWZNumber("5609115"), None)

        """pwz must be number"""
        self.assertNotEqual(UploadFiles.InterfaceInsertUpdate.checkPWZNumber("asdvfgt"), None)

    def test_prepareOneRow(self):
        self.assertNotEqual(UploadFiles.InterfaceInsertUpdate.prepareOneRow(
            b'"Id wsp\xc3\xb3lnika";"Id praktyki";"Numer ksiegi";"Typ praktyki";"Zaw\xc3\xb3d opis";"Numer wpisu do rej. zawodowego";"Numer prawa wykonywania zawodu";"Numer wpisu do ewidencji gospodarczej";"Imie";"Drugie imie";"Nazwisko";"Dziedzina medycyny";"Nip";"Specjalizacja";"Data rozp. dzialalnosci";"Data rozp. dzialalnosci art. 104";"Data zak. dzialalnosci"\r\n'),
            [
                'Id wsp\xf3lnika',
                'Id praktyki',
                'Numer ksiegi',
                'Typ praktyki',
                'Zaw\xf3d opis',
                'Numer wpisu do rej. zawodowego',
                'Numer prawa wykonywania zawodu',
                'Numer wpisu do ewidencji gospodarczej',
                'Imie',
                'Drugie imie',
                'Nazwisko',
                'Dziedzina medycyny',
                'Nip',
                'Specjalizacja',
                'Data rozp. dzialalnosci',
                'Data rozp. dzialalnosci art. 104',
                'Data zak. dzialalnosci'
            ]
        )