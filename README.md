# Wstęp
W celu wykonania poniższych zadań należy pobrać projekt z tej
<a href="">strony</a> i otworzyć go (najlepiej) w pycharmie.
Wszystkie deklaracje klas/fukncji zostały juz napisane w powyższym projekcie. Należy tylko uzupełnić pustą klasę/funkcję. Po uruchomieniu i wejściu na <a href="127.0.0.1:8000">localhost</a> należy zarejestrować konto swoim imieniem, nazwiskiem oraz e-mailem studenckim, aby na screenie z wykonania zadania potwierdzić swoją tożsamość.

Przydatne komendy:
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py shell
```

# Zadanie 1

##### Część 1:
Stwórz model zadania oraz listy zadań.
Model zadania powinien posiadać przynajmniej pola:
- name
- deadline
- completed

Utwórz przykładową listę zadań o nazwie swojego imienia i nazwiska, oraz dodaj do niej zadanie. </br>

Wyświetl zadania oraz listę zadań w terminalu.

#
##### Część 2:
Aby wyświetlić te modele na stronie należy utworzyć funkcję renderującą plik my_app/templates/task_list.html, jest to template zawierający kod pokazujący pola z części pierwszej, można go dowolnie zmieniać.
#
##### Część 3:
Spraw, aby lista zadań wraz z zadaniami pojawiły sie na stronie
<a href="127.0.0.1/task_list">localhost/task_list</a>.
#

#### Screen z rozwiązaniem należy umieścić na upelu. </br> </br>



# Zadanie 2

Po przejściu na <a href="127.0.0.1/admin">panel admina</a> w zakładce my_app spraw, aby pokazał się model zadań oraz listy zadań. Po kliknięciu w model zadań powinny wyświetlić się wszystkie zadania wraz z ich polem nazwy oraz z deadlinem posortowanym od tych najbliższych.

#### Screen z rozwiązaniem należy umieścić na upelu. </br> </br>

# Zadanie 3

Teraz już możesz dodawać modele do bazy danych z poziomu admina. </br>

##### Część 1:

Kolejnym zadaniem będzie dodanie nowej listy zawierającej kilka zadań. Teraz chcemy, aby na stronie pojawiły się wszystkie listy zadań oraz wszystkie zadania.
#
##### Część 2:

Dodaj przykładowe zadania z deadlinem wczorajszym i jutrzejszym. </br> </br>
Modyfikując task_list.html na stronie należy wyświetlić:
- na czerwono, zadania które nie zostały zrealizowane (wczorajsze)
- na żółto, zadania których termin się zbliża (dzień przed terminem)
- na biało, pozostałe

#
##### Część 3:
Uzupełnij funkcję set_task_as_completed w admin.py, tak aby po wejściu w model zadań na stronie admina była dostępna w liście rozwijanej "action". Przed użyciem tej funkcji zmodyfikuj template task_list.html, tak aby nie wyświetlał zadania, które jest "completed".

#### Screen z rozwiązaniem należy umieścić na upelu. </br> </br>

