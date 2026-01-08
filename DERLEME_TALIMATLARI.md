# Akademik Portal PDF Birleştirme Yazılımı - Derleme Talimatları

Bu yazılım Python ve CustomTkinter kullanılarak geliştirilmiştir. Windows, macOS ve Linux üzerinde çalışabilir. 
Ancak, **PyInstaller ile .exe (veya binary) oluşturma işlemi, her işletim sisteminin kendi üzerinde yapılmalıdır.**
Yani, Windows .exe dosyası Windows'ta, Mac uygulaması Mac'te, Linux uygulaması Linux'ta derlenmelidir.

Aşağıdaki adımları ilgili işletim sisteminde uygulayarak çalıştırılabilir dosya oluşturabilirsiniz.

## Ön Gereksinimler

Tüm platformlar için öncelikle Python yüklü olmalıdır.

Kodun bulunduğu klasörde terminal/komut satırını açın ve bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
pip install pyinstaller
```

## 1. Windows (Zaten Hazır)
Windows üzerinde şu komut kullanılır (bunu zaten yaptık):

```powershell
pyinstaller --noconsole --onefile --name "AkademikPortalPDF" --add-data "C:\Kullanici\Yolu\customtkinter;customtkinter/" pdf_merger_gui.py
```
*(Not: `--add-data` kısmındaki `customtkinter` yolu bilgisayarınızdaki Python kurulumuna göre değişir. Script içinde otomatik algılanır.)*

## 2. macOS

Mac bilgisayarınızda terminali açın, proje klasörüne gidin ve şu komutu çalıştırın:

```bash
# CustomTkinter yolunu bulmak için önce bunu çalıştırın:
python3 -c "import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))"
# Çıkan yolu aşağıda <path_to_customtkinter> yerine yazın.

# Derleme Komutu:
pyinstaller --noconsole --onefile --name "AkademikPortalPDF" --add-data "<path_to_customtkinter>:customtkinter/" pdf_merger_gui.py
```
*Not: Mac'te yol ayırıcı olarak noktalı virgül (;) yerine iki nokta üst üste (:) kullanılır.*

Oluşan dosya `dist` klasöründe olacaktır.

## 3. Linux (Ubuntu, Debian, vb.)

Linux terminalinde proje klasörüne gidin ve şu komutu çalıştırın:

```bash
# CustomTkinter yolunu bulmak için:
python3 -c "import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))"
# Çıkan yolu aşağıda <path_to_customtkinter> yerine yazın.

# Derleme Komutu:
pyinstaller --noconsole --onefile --name "AkademikPortalPDF" --add-data "<path_to_customtkinter>:customtkinter/" pdf_merger_gui.py
```

Oluşan dosya `dist` klasöründe olacaktır. Bu dosyaya sağ tıklayıp "Çalıştırılabilir" (Executable) izni vermeniz gerekebilir.
