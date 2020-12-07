baza all countries

- logika biznesowa to przetwarzanie danych
- wczytywanie danych wejściowych to adaptery (w formacie dataframe)
- adapter na dynamodb

przetestować 2 podejścia:

- wczytywać główny plik (12M rekordów) do pandas i zobaczyć ile ramu zajmuje
- wczytywać dane z pliku w chunkach

etap 1:

- kazdy rekord ma kod kraju, z każdego wyrzucić kolumnę z innymi nazwami tego miejsca
- domergować kolumnę z countries info - pełna nazwa kraju po angielsku

- (spróbować to najpierw zrobić bez pandas)

- w oparciu o listę wszystkich miejsc policzyć ile jest miast w każdym kraju (tabela z nazwą kraju i miasta)
- policzyć histogram dla poszczególnych miast w krajach po ilości mieszkańców (*)
- znaleźć kraje z najniższą/ najwyższą sumą mieszkańców w swoich miastach (*)

etap 2:

* dla 500 miast *
- dostanę listę lotnisk
- znaleźć sposób i bibliotekę mierzenia odległości (pewnie model great circle, geopy, ew. scipy)
- wybrać listę miejscowości (np stolice) i dopasować najbliższe lotnisko

etap 3:

- zapis do dynamodb
- przetwarzanie równoległe, optymalizacja

***
do przechowywania tymczasowych tabel - pandas.to_feather ? czy coś bardziej optymalnego?