
# 🛠️ Motorola 6800 Assembler with GUI

Bu proje, **Motorola 6800** mikroişlemcisi için bir assembler simülatörüdür. Python ile geliştirilmiş olan bu uygulama, assembly komutlarını makine diline çevirmekle kalmaz, aynı zamanda kullanıcı dostu bir grafik arayüz ile derlenen kodun hafıza ve register durumlarını da görselleştirir.

## 🎯 Projenin Amacı

Bu proje, bir derleyici (assembler) mantığını anlamak ve 6800 işlemcisine uygun assembly komutlarını makine koduna çevirebilen interaktif bir sistem geliştirmek amacıyla oluşturulmuştur.

## 📁 Proje Dosya Yapısı

```
Assembler_mc6800/
├── assembler.py            # Assembler sınıfı: parsing, opcode çözümleme, hafıza ve register işlemleri
├── gui.py                  # Tkinter tabanlı kullanıcı arayüzü
├── opcodes_full.py         # Tüm 6800 komut seti ve opcode tanımları
├── tempCodeRunnerFile.py   # Geçici çalışma dosyası (gereksiz)
├── __pycache__/            # Derlenmiş Python bytecode dosyaları (ihmal edilebilir)
```

## 🖥️ Özellikler

- Assembly kodlarını satır satır analiz eder.
- Etiket (label) çözümlemesi ve adresleme modlarını destekler.
- `.ORG`, `.END`, `.BYTE`, `.EQU` gibi pseudo-komutları işler.
- Kayıtlar (A, B, X, SP) ve bellek durumunu görsel olarak sunar.
- Derlenen makine kodunu listeler.

## ▶️ Kurulum ve Çalıştırma

### Gereksinimler

- Python 3.7+
- Tkinter (standart Python kurulumu ile gelir)

### Çalıştırmak için

```bash
python gui.py
```

GUI arayüz açıldığında assembly kodunuzu girip `Derle` butonuna basabilirsiniz. Derlenen kodun çıktısı, bellek içeriği ve register durumu ekranda görüntülenir.


## 🧠 Geliştiriciler İçin Notlar

- Kod iki aşamalı bir assembler mantığı ile yazılmıştır: birinci geçişte label'lar işlenir, ikinci geçişte opcode'lar çözülür.
- `opcodes_full.py` tüm opcode varyasyonlarını (immediate, direct, extended, indexed) içerir.
- Gelecekte step-by-step simülasyon, breakpoint desteği ve hata ayıklayıcı gibi gelişmiş özellikler eklenebilir.
