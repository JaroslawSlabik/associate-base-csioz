from django.db import models
import logging
from django.db import transaction, DatabaseError


class Associate(models.Model):
    name_text = models.CharField(max_length=200)
    surname_text = models.CharField(max_length=200)
    specialization_text = models.CharField(max_length=200, null=True, blank=True)
    pwz_num = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name_text + ' ' + self.surname_text


class Addresses(models.Model):
    associate = models.ForeignKey(Associate)
    name_text = models.CharField(max_length=300, null=True, blank=True)
    street_text = models.CharField(max_length=200, null=True, blank=True)
    number_text = models.CharField(max_length=200, null=True, blank=True)
    local_text = models.CharField(max_length=200, null=True, blank=True)
    zip_code_text = models.CharField(max_length=8, null=True, blank=True)
    city_text = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name_text


class Settings(models.Model):
    name_text = models.CharField(max_length=200)
    value_text = models.CharField(max_length=200)

    def __str__(self):
        return self.name_text + ' -> ' + self.value_text


class UploadFiles(models.Model):
    associate_file = models.FileField(null=True, blank=True)
    addresses_file = models.FileField(null=True, blank=True)

    """
    base class, validates the CSV file based on required columns.
    watches over the atomicity of insertion
    """

    class InterfaceInsertUpdate:
        __column_map = {}
        important_column_name_list = []

        def check(self, header):
            check_header = all(item in header for item in self.important_column_name_list)
            if not check_header:
                return False

            for item in self.important_column_name_list:
                self.__column_map[item] = header.index(item)

            return True

        """Method to override, should save items to database"""

        def saveToOverride(self, line_list):
            pass

        def save(self, lines):
            try:
                with transaction.atomic():
                    Addresses.objects.all().delete()
                    for line in lines:
                        columns = self.prepareOneRow(line)
                        self.saveToOverride(columns)
            except DatabaseError:
                pass

        """Get value under header name. Return None or string """
        def getValueUnderHeader(self, columns, name):
            """Get value under header column name """
            value_str = columns[self.__column_map[name]]
            if value_str == "NULL":
                return None

            return value_str

        def strToInt(self, my_str):
            try:
                return int(my_str) if my_str is not None else None
            except ValueError:
                return None

        """
        Check number PWZ, :
        https://nil.org.pl/rejestry/centralny-rejestr-lekarzy/zasady-weryfikowania-nr-prawa-wykonywania-zawodu
        """
        def checkPWZNumber(self, pwz_str):
            if len(pwz_str) != 7:
                return None

            chk = self.strToInt(pwz_str[0])
            if chk is None:
                return None

            sum_control = 0
            index = 1
            for char in pwz_str[1:]:
                char_as_int = self.strToInt(char)
                if char_as_int is None:
                    return None
                sum_control += char_as_int * index
                index = index + 1

            sum_control = sum_control % 11

            if chk != sum_control:
                return None

            return self.strToInt(pwz_str)

        def __undres__(self, element):
            if len(element) == 0:
                return ""

            if element[0] == '"':
                return element[1:-1]

            return element

        def prepareOneRow(self, one_row):
            return list(map(self.__undres__, one_row.decode("utf-8").replace("\r\n", "").split(';')))


    class InsertUpdateAssociate(InterfaceInsertUpdate):
        def __init__(self):
            self.important_column_name_list = [
                "Id wspólnika",
                "Imie",
                "Nazwisko",
                "Specjalizacja",
                "Numer prawa wykonywania zawodu"
            ]

        def saveToOverride(self, columns):

            """Get values"""
            id_associate_str = self.getValueUnderHeader(columns, "Id wspólnika")
            name = self.getValueUnderHeader(columns, "Imie")
            surname = self.getValueUnderHeader(columns, "Nazwisko")
            specialization = self.getValueUnderHeader(columns, "Specjalizacja")
            pwz_str = self.getValueUnderHeader(columns, "Numer prawa wykonywania zawodu")

            """Check PWZ"""
            pwz_number = None
            if pwz_str is not None:
                pwz_number = self.checkPWZNumber(pwz_str)

            """Make INTEGER"""
            id_associate = self.strToInt(id_associate_str)

            """If id_associate is none then insert with new ID"""
            if id_associate is None:
                Associate(
                    pk=None,
                    name_text=name,
                    surname_text=surname,
                    specialization_text=specialization,
                    pwz_num=pwz_number
                ).save()
                return True

            """If id_associate is not none then try update date """
            try:
                with transaction.atomic():
                    """Update data associate under ID"""
                    associate = Associate.objects.get(pk=id_associate)
                    associate.name_text = name
                    associate.surname_text = surname
                    associate.specialization_text = specialization
                    associate.pwz_num = pwz_number
                    associate.save()
            except Associate.DoesNotExist:
                """If not exist associate under ID then insert with ID from file """
                try:
                    with transaction.atomic():
                        Associate(
                            pk=id_associate,
                            name_text=name,
                            surname_text=surname,
                            specialization_text=specialization,
                            pwz_num=pwz_number
                        ).save()
                except DatabaseError:
                    return False

            return True

    class InsertUpdateAddresses(InterfaceInsertUpdate):
        def __init__(self):
            self.important_column_name_list = [
                "Id wspólnika",
                "Id adresu",
                "Nazwa zakladu",
                "Ulica",
                "Budynek",
                "Lokal",
                "Kod pocztowy",
                "Miejscowosc"
            ]

        def saveToOverride(self, columns):
            """Get values"""
            id_associate_str = self.getValueUnderHeader(columns, "Id wspólnika")
            id_address_str = self.getValueUnderHeader(columns, "Id adresu")
            name = self.getValueUnderHeader(columns, "Nazwa zakladu")
            street = self.getValueUnderHeader(columns, "Ulica")
            number = self.getValueUnderHeader(columns, "Budynek")
            local = self.getValueUnderHeader(columns, "Lokal")
            zip_code = self.getValueUnderHeader(columns, "Kod pocztowy")
            city = self.getValueUnderHeader(columns, "Miejscowosc")

            """Make INTEGER, id_associate not can be None"""
            id_associate = self.strToInt(id_associate_str)
            if id_associate is None:
                return False

            id_address = self.strToInt(id_address_str)

            """If not find relation to associate then return False"""
            try:
                associate_details = Associate.objects.get(pk=id_associate)
            except Associate.DoesNotExist:
                return False

            if zip_code is not None:
                if len(zip_code) > 6:
                    return False

            """If id_address is none then insert with new ID"""
            try:
                with transaction.atomic():
                    if id_address is None:
                        Addresses(
                            pk=None,
                            associate=associate_details,
                            name_text=name,
                            street_text=street,
                            number_text=number,
                            local_text=local,
                            zip_code_text=zip_code,
                            city_text=city
                        ).save()
                    else:
                        Addresses(
                            pk=id_address,
                            associate=associate_details,
                            name_text=name,
                            street_text=street,
                            number_text=number,
                            local_text=local,
                            zip_code_text=zip_code,
                            city_text=city
                        ).save()
            except DatabaseError:
                return False

            return True

    def save(self, *args, **kwargs):
        """file_name_associate = self.associate_file.url"""
        """First try upload associates"""
        try:
            f = self.associate_file
            f.open(mode='r')
            lines = f.readlines()
            f.close()

            insert_update = self.InsertUpdateAssociate()

            header = lines.pop(0)
            header = insert_update.prepareOneRow(header)
            if not insert_update.check(header):
                return

            insert_update.save(lines)
        except:
            pass

        """file_name_addresses = self.addresses_file.url"""
        """Next try upload addresses"""
        try:
            f = self.addresses_file
            f.open(mode='r')
            lines = f.readlines()
            f.close()

            insert_update = self.InsertUpdateAddresses()

            header = lines.pop(0)
            header = insert_update.prepareOneRow(header)
            if not insert_update.check(header):
                return

            insert_update.save(lines)
        except:
            pass
