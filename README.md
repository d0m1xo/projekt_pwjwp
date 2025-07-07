# projekt_pwjwp
Chcąc uruchomić aplikację, należy zapisać pliki w odpowiednim folderze. W moim przypadku przykładowa nazwa folderu to "projekt_pwjwp".
### Uruchomienie projektu lokalnie
Na początku należy zainstalować pakiety z pliku requirements.txt. Może to być w środowisku wirtualnym, wtedy należy wykonać następujące kroki:
 1) python -m venv aplikacja
 2) .\aplikacja\Scripts\activate
 3) pip install -r requirements.txt
 4) streamlit run app.py
 5) aplikacja powinna się otworzyć automatycznie, ale jeżeli nie to w oknie przeglądarki należy wpisać http://localhost:8501

### Zbudowanie i uruchomienie obrazu Docker
Chcąc zbudować i uruchomić obraz Docker należy wykonać następujące kroki:
  1) docker build -t projekt_pwjwp .
  2) docker run -p 8501:8501 projekt_pwjwp
  3) w oknie przeglądarki należy wpisać http://localhost:8501
