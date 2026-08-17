#Hastane Acil Servis & Triyaj / Hasta Kabul Otomasyonu
import os
class hasta:
    def __init__(self,tc_no,ad_soyad,yas,triyaj_kodu):
        
        self.ad_soyad=ad_soyad
        self.triyaj_kodu=triyaj_kodu
        if yas<=0 or yas>130:
            raise ValueError("yaş negatif veya 130 dan büyük olamaz!!!")
        else:
            self._yas=yas

        if  ((len(tc_no)==11) and (tc_no.isdigit())):
            self._tc_no=tc_no
        else:
            raise ValueError("tc niz 11 rakamdan oluşmalidir!!!")
    @property
    def yas(self):
        return self._yas

    @yas.setter
    def yas(self,yeni_yas):
        if yeni_yas<=0 or yeni_yas>130:
            raise ValueError("yaş negatif veya 130 dan büyük olamaz!!!")
        else:
             self._yas=yeni_yas

    @property
    def tc_bilgisi(self):
        return self._tc_no

    def __str__(self):
        return f"tc :[{self.tc_bilgisi}] | ad_soyad : {self.ad_soyad} | yas : {self.yas} | triyaj kod : {self.triyaj_kodu} "

class Yogun_Bakim_Hastasi(hasta):
    def __init__(self, tc_no, ad_soyad, yas, triyaj_kodu="kirmizi",bağli_cihaz="solunum_makinesi"):
        super().__init__(tc_no, ad_soyad, yas, triyaj_kodu)
        self.bağli_cihaz=bağli_cihaz

    def __str__(self):
        return f"{super().__str__()} | bağli_cihaz : {self.bağli_cihaz}"

    
class acil_servis:
    def __init__(self,dosya_adi="acil_hastalar.txt"):
        self.dosya_adi=dosya_adi
        if not os.path.exists(self.dosya_adi):

            with open(self.dosya_adi,"w",encoding="utf-8")as f:
                pass

    def hasta_kabul(self,hasta_obj):
        with open(self.dosya_adi,"r",encoding="utf-8")as f:
            satirlar=f.readlines()
            var_mi=False

            for satir in satirlar:
                if not satir.strip():
                    continue
                veri=satir.strip().split(",")
                if veri[0] == hasta_obj.tc_bilgisi:
                    raise FileExistsError(f"[{hasta_obj.tc_bilgisi}] tc numarali hasata zaten acil serviste kayitli!!!")

        with open(self.dosya_adi,"a",encoding="utf-8")as f:
            yeni_kayit=f"{hasta_obj.tc_bilgisi},{hasta_obj.ad_soyad},{hasta_obj.yas},{hasta_obj.triyaj_kodu}\n"
            f.write(yeni_kayit)
            f.flush()
            print(f"{hasta_obj.ad_soyad} acil servise kabul edildi...")

    def taburcu_et(self,tc_no):
           if not ((len(tc_no)==11) and (tc_no.isdigit())):
               raise ValueError("tc niz 11 rakamdan oluşmalidir!!!")

           with open(self.dosya_adi,"r+",encoding="utf-8")as f:
               satirlar=f.readlines()
               kalan_satirlar=[]

               for satir in satirlar:
                   if not satir.strip():
                       continue
                   veri=satir.strip().split(",")
                   if veri[0] == tc_no:
                       continue
                   else:
                       kalan_satirlar.append(satir)
               if len(kalan_satirlar)==len(satirlar):
                   raise LookupError(f"[{tc_no}] tc numarali hasta bulunamadi!!!")
               else:
                   f.seek(0)
                   f.writelines(kalan_satirlar)
                   f.truncate()
                   f.flush()
                   print(f"[{tc_no}] tc numarali hasta başariyla taburcu edilmiştir...")

    def hastalari_listele(self):
        with open(self.dosya_adi,"r",encoding="utf-8")as f:
            satirlar=f.readlines()
            if not satirlar:
                print("\nAcil serviste şu an kayitli hasta bulunmamaktadir!!!\n")
                return
            for satir in satirlar:
                if not satir.strip():
                    continue
                veri=satir.strip().split(",")
                print(25*"=")
                print(f"tc : {veri[0]}")
                print(f"adi ve soyadi : {veri[1]}")
                print(f"yasi : {veri[2]}")
                print(f"triyaj kodu : {veri[3]}")
                print(25*"=")
servis = acil_servis()

while True:
    print("=" * 45)
    print("    HASTANE ACİL SERVİS & TRİYAJ SİSTEMİ   ")
    print("=" * 45)
    print("1 - Yeni Hasta Kabul")
    print("2 - Hasta Taburcu Et")
    print("3 - Aktif Hastalari Listele")
    print("4 - Çikiş")
    print("=" * 45)

    secim = input("Lütfen bir işlem seçiniz (1-4): ")

    if secim == "1":
        tur = input("Hasta Türü (1: Standart Hasta, 2: Yoğun Bakim): ")
        tc = input("11 Haneli TC Kimlik No: ")
        ad_soyad = input("Ad Soyad: ")

        try:
            yas = int(input("Yaş: "))
            triyaj = input("Triyaj Kodu (Kirmizi / Sari / Yeşil): ")

            if tur == "1":
                yeni_hasta = hasta(tc, ad_soyad, yas, triyaj)
            elif tur == "2":
                cihaz = input("Bağli Cihaz (Örn: Solunum Cihazi): ")
                yeni_hasta = Yogun_Bakim_Hastasi(tc, ad_soyad, yas, triyaj_kodu=triyaj, bağli_cihaz=cihaz)
            else:
                print("Geçersiz hasta türü seçimi!")
                continue

            servis.hasta_kabul(yeni_hasta)

        except ValueError as e:
            print(f"\n[GEÇERSİZ GİRİŞ]: {e}")
        except FileExistsError as e:
            print(f"\n[MÜKERRER KAYIT]: {e}")
        else:
            print("[BAŞARILI]: Hasta kabul işlemi tamamlandi.")
        finally:
            print("[SİSTEM LOG]: Kabul protokolü sonlandirildi.\n")

    elif secim == "2":
        silinecek_tc = input("Taburcu edilecek hastanin TC Kimlik No: ")
        try:
            servis.taburcu_et(silinecek_tc)
        except ValueError as e:
            print(f"\n[HATALI TC]: {e}")
        except LookupError as e:
            print(f"\n[KAYIT BULUNAMADI]: {e}")
        else:
            print("[BAŞARILI]: Taburcu işlemi dosyaya işlendi.")
        finally:
            print("[SİSTEM LOG]: Taburcu protokolü sonlandirildi.\n")

    elif secim == "3":
        servis.hastalari_listele()

    elif secim == "4":
        print("\nSistemden çikiş yapiliyor. İyi çalişmalar!")
        break
    else:
        print("\nGeçersiz seçim! Lütfen 1-4 arasinda bir sayi giriniz.\n")
                   

               
            

    
    

