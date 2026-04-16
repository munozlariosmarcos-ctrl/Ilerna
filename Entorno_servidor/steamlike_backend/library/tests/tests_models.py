from django.test import TestCase

from library.models import LibraryEntry


class DemoTest(TestCase):
    def test_demo(self):
        # Comprueba que dos valores son exactamente iguales.
        self.assertEqual(4, 2+2)
        # Comprueba si una condición se cumple o no.
        self.assertTrue(4 == 4)
        self.assertFalse(5 == 4)
        # Permiten distinguir entre None y otros valores como cadenas vacías o ceros.
        self.assertIsNone(None)
        # Comprueba que una acción provoca un error concreto.
        with self.assertRaises(ZeroDivisionError):
            # Codigo que lanza la excepcion
            4/0

class LibraryEntryExternalIdLengthTests(TestCase):
    def test_external_id_length_counts_regular_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 3)

    def test_external_id_length_counts_empty_string_as_zero(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 0)

    def test_external_id_length_counts_whitespace(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="   ")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 3)

    def test_external_id_length_counts_max_length_boundary_100(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="x" * 100)

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 100)

    def test_external_id_length_raises_type_error_if_not_string_or_none(self):
        # Caso anómalo: asignación indebida en memoria.
        # Precondiciones
        entry = LibraryEntry(external_game_id=123)

        # Llamada
        # Comprobaciones
        with self.assertRaises(TypeError):
            entry.external_id_length()



# CREACION DE TESTS 

class LibraryEntryExternalIdUpperTests(TestCase):
    def test_External_Id_Upper(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc")

        # Llamada
        cadena = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(cadena, "ABC")
    
    def test_External_Id_Upper_empty_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="")

        # Llamada
        cadena = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(cadena, "")

    def test_External_Id_Upper_whitespace(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="   ")

        # Llamada
        cadena = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(cadena, "   ")


class LibraryEntryHoursPlayedLabelTests(TestCase):
        def test_Hours_Played_label(self):
            # Precondiciones
            entry = LibraryEntry(hours_played=5)

            # Llamada
            cadena = entry.hours_played_label()
            # Comprobaciones
            self.assertEqual(cadena, "low")
        
        def test_Hours_Played_label_zero(self):
            # Precondiciones
            entry = LibraryEntry(hours_played=0)

            # Llamada
            cadena = entry.hours_played_label()
            # Comprobaciones
            self.assertEqual(cadena, "none")

        def test_Hours_Played_label_high(self):
            # Precondiciones
            entry = LibraryEntry(hours_played=15)

            # Llamada
            cadena = entry.hours_played_label()
            # Comprobaciones
            self.assertEqual(cadena, "high")
        

class LibraryEntryStatusValueTests(TestCase):
        def test_Status_Value(self):
            # Precondiciones
            entry = LibraryEntry(status=LibraryEntry.STATUS_PLAYING)

            # Llamada
            valor = entry.status_value()
            # Comprobaciones
            self.assertEqual(valor, 1)

        def test_Status_Value_Wishlist(self):
            # Precondiciones
            entry = LibraryEntry(status=LibraryEntry.STATUS_WISHLIST)

            # Llamada
            valor = entry.status_value()
            # Comprobaciones
            self.assertEqual(valor, 0)
        
        def test_Status_Value_Completed(self):
            # Precondiciones
            entry = LibraryEntry(status=LibraryEntry.STATUS_COMPLETED)

            # Llamada
            valor = entry.status_value()
            # Comprobaciones
            self.assertEqual(valor, 2)
            

 
