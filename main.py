"""
Konspekt:
Klasy:
0. FileJSONHandler
0. FilePickleHandler
0. FileCSVHandler
1. Obsługa plików:
    - wykrycie typu pliku
    - otwarcie
    - zapisanie
2. Kontroler ścieżki:
    - sprawdza czy ścieżka istnieje
    - tworzy ścieżkę jeśli nie istnieje
    - wypisuje elementy w ostatnim istniejącym folderze
3. Kontroler wartości wejściowych (<change1><change2>)
    - pobiera wartości wejściowe
    - ma metode do kontroli "y,x,value"
4. Edytor csv(?) -> zmieniacz wartości w listach
    - obsługa wyjątków -> wartości spoza zakresu wielkości listy
"""
import csv
import json
import os.path
import pickle
import os
import sys

src = 'katalog1/katalog11/katalog111/ford_escort.csv'
dst = 'katalog2/katalog22/katalog222/ford_escort_zmiany.csv'

if os.path.exists(os.path.split(dst)[0]):
    pass
else:
    os.makedirs(os.path.split(dst)[0])


class FileJSONHandler:
    def open(self, src):
        with open(src) as file:
            retval = json.load(file)
        return retval

    def save(self, dst, obj):
        with open(dst, 'w') as f:
            json.dump(obj, f)


class FilePickleHandler:
    def open(self, src):
        with open(src, 'rb') as file:
            retval = pickle.load(file)
        return retval

    def save(self, dst, obj):
        with open(dst, 'wb') as f:
            pickle.dump(obj, f)


class FileCSVHandler:
    def open(self, src):
        with open(src) as file:
            reader = csv.reader(file)
            retval = [[element.strip() for element in line] for line in reader]
        return retval

    def save(self, dst, obj):
        with open(dst, 'w') as f:
            writer = csv.writer(f)
            for row in obj:
                writer.writerow(row)
        return obj


def wprowadz_zmiany(obiekt_wejsciowy, zmiany):
    for _zmiana in zmiany:
        zmiana = _zmiana.split(',')
        liczba_wierszy = len(obiekt_wejsciowy)
        liczba_kolumn = len(obiekt_wejsciowy[0])
        if liczba_wierszy > int(zmiana[0]) and liczba_kolumn > int(zmiana[1]):
            obiekt_wejsciowy[int(zmiana[0])][int(zmiana[1])] = zmiana[2]
    return obiekt_wejsciowy


def check_file_type(src):
    ext = os.path.splitext(src)[-1]
    # ext = src.split('.')[-1] -> zamiennie do wyższego
    return ext


csv_reader = FileCSVHandler()
json_reader = FileJSONHandler()
pickle_reader = FilePickleHandler()

if check_file_type(src) == '.csv':
    obiekt_wejsciowy = csv_reader.open(src)

if check_file_type(src) == '.json':
    obiekt_wejsciowy = json_reader.open(src)

if check_file_type(src) == '.pickle':
    obiekt_wejsciowy = pickle_reader.open(src)

zmiany = sys.argv[1:]
obiekt_wyjsciowy = wprowadz_zmiany(obiekt_wejsciowy, zmiany)

if check_file_type(dst) == '.csv':
    csv_reader.save(dst, obiekt_wyjsciowy)

if check_file_type(dst) == '.json':
    json_reader.save(dst, obiekt_wyjsciowy)

if check_file_type(dst) == '.pickle':
    pickle_reader.save(dst, obiekt_wyjsciowy)
