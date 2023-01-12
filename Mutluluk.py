# Bu program Cankaya Universitesi tarafından lise öğrencilerine yönelik düzenlenen meslek tanıtımı atölyeleri kapsamında Bilgisayar Mühendisi gibi Düşünmek 
# atölyesinde geliştirilen yazılım projesinin örnek uygulamasıdır. Projede bir text dosyasından virgülle ayrılmış ülke adları ve mutluluk endeksleri okunarak
# en mutlu, en mutsuz ve ortalama mutluluk endeks değeri bir pencere içerisinde kullanıcılara gösterilir. Ayrıca, kullanıcılara ülke adlarını girerek listede arama
# yapma imkanı sunar. Sonuçları bir çubuk grafiği ile görselleştirme özelliği de vardır. 

import sys
import tkinter as tk
import matplotlib.pyplot as plt
from typing import Dict

def veri_oku(dosya_adi, ayirici):
    """
    Veri dosyasından ülke mutluluk endekslerini oku.

    Returns:
        dict: Sözlük, ülke adlarını anahtar olarak ve mutluluk
        endekslerini değer olarak içerir.
    """
    data = {}
    
    try:
        with open(dosya_adi) as f:
            for line in f:
                key, values = line.strip().split(ayirici)
                data[key.upper()] = values

    except FileNotFoundError:
        return None

    except ValueError:
        return None

    return data

#birden fazla minimum değer olsa bile sadece ilk minimum değerini bulan ve ait olduğu anahtar adını hesaplayan fonksiyon
def minimum_tek(data):
    # mini değişkenin ilk değeri sys kütüphanesinde bulunan max değeri ya da notlarda olası en yüksek not olan 100'e eşitlenebilir 
    # ör. mini = sys.float_info.max ya da  mini = 100
    mini = sys.float_info.max  
    for key in data:
        if float(data[key])<mini:
            mini=float(data[key])
            name=key
    return mini, name

#birden fazla minimum değerini bulan ve ait oldukları anahtar adlarını hesaplayan fonksiyon
def minimum_tumu(data):
    #min hazır fonksiyonu kullanılarak da minimum değer bulunabilir
    min_keys = [key for key, value in data.items() if value == min(data.values())]
    return min_keys

#birden fazla maksimum değer olsa bile sadece ilk maksimum değerini bulan ve ait olduğu anahtar adını hesaplayan fonksiyon
def maximum_tek(data):
    # maxi değişkenin ilk değeri sys kütüphanesinde bulunan min değeri ya da notlarda olası en düşük not olan 0'a eşitlenebilir 
    # ör. maxi = sys.float_info.min ya da  maxi = 0
    maxi = sys.float_info.min  
    for key in data:
        if float(data[key])>maxi:
            maxi=float(data[key])
            name=key
    return maxi, name

#birden fazla maksimum değerini bulan ve ait oldukları anahtar adlarını hesaplayan fonksiyon
def maximum_tumu(data):
    max_keys = [key for key, value in data.items() if value == max(data.values())]
    return max_keys

#dictionary ya da liste türünde gelen veri setindeki değerlerin ortalamasını hesaplayan fonsiyon  
def average(data):
    if isinstance(data, Dict):
        sum = 0.0
        for key in data:
                sum += float(data[key])
        return sum/ len(data)
    elif isinstance(data, list):
        return sum(data) / len(data)
    else: 
        return None

def search(veriler, aranan_deger):
    # Aranan ülke isminin listedeki yerini bulun
	try:
		sonuc = veriler[aranan_deger]
	except KeyError:
		sonuc = None
	return sonuc 

def GUI(data):
    # Pencere oluştur
    window = tk.Tk()
    window.title("Mutluluk Endeksi")

    # Text kutusu oluştur
    ulke_ad_giris = tk.Entry(window)

    # Etiketleri oluştur
    etiket_ulke_adi = tk.Label(window, text="Ülke adı giriniz: ")
    etiket_sonuc = tk.Label(window, text="")
    etiket_ortalama = tk.Label(window, text="")
    etiket_en_mutlu = tk.Label(window, text="")
    etiket_en_mutsuz = tk.Label(window, text="")
    
    #minimum fonksiyonunu çalıştır
    mini, key_mini = minimum_tek(data)

    #maksimum fonksiyonunu çalıştır
    maxi, key_max = maximum_tek(data)

    #ortalama fonsiyonun çalıştır
    ortalama = average(data)

    # Ortalama, en mutlu ve en mutsuz ülke sonuçlarını etiketlere yazdir
    etiket_ortalama.config(text=str(round(ortalama,3)), bg ="orange")
    etiket_en_mutlu.config(text=key_max + ': ' + str(round(maxi,3)), bg ="green")
    etiket_en_mutsuz.config(text=key_mini + ': ' + str(round(mini,3)), bg ="yellow")

    sonuclar ={}
    sonuclar.update([(key_mini,mini),('ORTALAMA',ortalama),(key_max,maxi)])
    
    def on_button_clicked():
        # Arama çubuğundan arama terimini alın
        aranan_ulke = ulke_ad_giris.get().upper()
        # Veriler arasında giriş yapılan ülkenin verisini arayın
        endeks_degeri = search(data, aranan_ulke)
        # sonuçları etiketlere yazdir
        if endeks_degeri is not None:
            etiket_sonuc.config(text=aranan_ulke + " " +str(endeks_degeri), background= "#FA8072")
            if float(data[aranan_ulke])>ortalama:
                sonuclar.clear()
                sonuclar.update([(key_mini,mini),('Ortalama',ortalama),(aranan_ulke, data[aranan_ulke]),(key_max,maxi)])
            else:
                sonuclar.clear()
                sonuclar.update([(key_mini,mini),(aranan_ulke, data[aranan_ulke]),('Ortalama',ortalama),(key_max,maxi)])
        else:
            etiket_sonuc.config(text=aranan_ulke + " bulunamadı!", bg = "red")
            sonuclar.clear()
            sonuclar.update([(key_mini,mini),('Ortalama',ortalama),(key_max,maxi)])
    
    def clear_text():
        ulke_ad_giris.delete(0, 'end')

    def chart():
        plt.style.use('ggplot')
        # Anahtar degerlerini listeye kopyala
        x_values=[]
        x_axis=[]
        y_axis=[]
        x_values_dict=sonuclar.keys()
        i=0
        for key in x_values_dict:
            x_values.append(key)
            x_axis.append(x_values[i])
            #y_axis.append(str(round(sonuclar[x_values[i]],2)))
            #y_axis.append(round(sonuclar[x_values[i]],2))
            y_axis.append(float(sonuclar[x_values[i]]))
            i= i + 1
        
        # Grafik ile x ve y eksenlerinin verilerini oluştur
        # x ekseninde sırasıyla en düşük mutluluk endeksine sahip ülke, ortalama, seçili ülkenin adı ve en yüksek mutluluk endeksine sahip ülke etiketleri gösterilecek
        # y ekseninde sırasıyla minimum, ortalama, seçili ülkenin adı ve maksimum sayısal değerleri gösterilecek

        x_pos = [i for i, _ in enumerate(x_axis)]
        plt.bar(x_pos, y_axis, color='green')
        # x ekseni ve y ekseni için başlık ve etiketleri ayarlayın
        plt.xlabel("Ülke")
        plt.ylabel("Mutluluk Endeksi")
        plt.title("Mutluluk Endeksi Karşılaştırması")

        plt.xticks(x_pos, x_axis)
        plt.show() 
   
    # Butonları oluştur
    buton_arama = tk.Button(window, text="   Ara  ", command=on_button_clicked)
    buton_temizle = tk.Button(window, text=" Temizle ", command=clear_text)
    buton_grafik_olustur = tk.Button(window, text=" Grafik oluştur ", command=chart)
   
    # GUI elementlerini pencereye yerleştirin
    etiket_ulke_adi.grid(row=0, column=1, padx=5, pady=5)
    ulke_ad_giris.grid(row=0, column=2, padx=5, pady=5)
    buton_arama.grid(row=0, column=3, padx=3, pady=3)
    buton_temizle.grid(row=0, column=4, padx=3, pady=3)
    etiket_sonuc.grid(row=1, columnspan=3, sticky="we", padx=5, pady=5)
    etiket_ortalama.grid(row=2, columnspan=3, sticky="we", padx=5, pady=5)
    etiket_en_mutsuz.grid(row=3, columnspan=3, sticky="we", padx=5, pady=5)
    etiket_en_mutlu.grid(row=4, columnspan=3, sticky="we", padx=5, pady=5)
    buton_grafik_olustur.grid(row=5, column=4, padx=5, pady=5)

    return window

def main():
    # Verileri text dosyasından okuyarak programa aktar
    data = {}
    data = veri_oku("mutluluk_veri.txt", ",")
   
    if data == None:
        # Pencere oluştur
        hata = tk.Tk()
        hata.title("Mutluluk Endeksi")
        etiket_hata = tk.Label(hata, text="Dosya okuma hatası ya da dosya bulunamadı!",bg = "red")
        buton_kapat = tk.Button(hata, text=" Programı kapat ", command=hata.destroy)
        buton_kapat.pack()
        etiket_hata.pack()
        hata.mainloop()
    else:
        #Grafik oluşturan fonsiyonu çalıştırın
        window = GUI(data)
        window.mainloop()

if __name__ == '__main__':
    main()
