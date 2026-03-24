# Güncellemeler - Emisyon Kaynakları

## Yapılan Değişiklikler

### 1. Emisyon Kaynaklarının Genişletilmesi

Önceden sistemde sadece **5 emisyon kaynağı** vardı (veritabanında). Şimdi **80 emisyon kaynağı** mevcut!

#### Kaynak Dağılımı:
- **Scope 1**: 3 kategori, 31 kaynak
  - Stationary Combustion (Sabit Yakma): 9 kaynak
  - Mobile Combustion (Hareketli Yakma): 16 kaynak
  - Fugitive Emissions (Kaçak Emisyonlar): 6 kaynak

- **Scope 2**: 2 kategori, 9 kaynak
  - Purchased Electricity (Satın Alınan Elektrik): 5 kaynak
  - Steam & Heat (Buhar ve Isı): 4 kaynak

- **Scope 3**: 7 kategori, 40 kaynak
  - Business Travel (İş Seyahati): 6 kaynak
  - Employee Commuting (Çalışan Ulaşımı): 5 kaynak
  - Purchased Goods & Services (Satın Alınan Mallar): 13 kaynak
  - Waste (Atık): 4 kaynak
  - Water (Su): 2 kaynak
  - Upstream Transportation (Yukarı Akış Taşımacılık): 4 kaynak
  - Ve daha fazlası...

### 2. API Güncellemeleri

#### Değiştirilen Dosyalar:
- `ghg/views.py`:
  - `api_get_sources()` fonksiyonu güncellendi
  - Artık veritabanı yerine `emission_factors.py` dosyasından direkt okuma yapıyor
  - `api_get_categories()` fonksiyonuna `code` alanı eklendi
  - `calculate_emission()` fonksiyonuna `@csrf_exempt` eklendi (API kullanımı için)

#### Yeni Özellikler:
- Tüm emisyon kaynakları `emission_factors.py` dosyasından geliyor
- Her kaynak için:
  - İsim (name)
  - Birim (unit)
  - Emisyon faktörü (emission_factor)
  - Kaynak referansı (source/reference)

### 3. Frontend Güncellemeleri

#### Değiştirilen Dosyalar:
- `frontend/app/data-entry/page.tsx`:
  - Kategori seçiminde `code` alanı eklendi
  - Hesaplama yaparken `category` ve `country` parametreleri eklendi
  - Kaydetme işleminde de aynı parametreler eklendi

#### Yeni Akış:
1. Kullanıcı Scope seçer (Scope 1, 2, veya 3)
2. Scope'a göre kategoriler yüklenir
3. Kategori seçilince o kategoriye ait TÜM kaynaklar yüklenir (80 kaynak!)
4. Kaynak seçilip aktivite verisi girilince hesaplama yapılır
5. Sonuç gösterilir ve kaydedilebilir

### 4. Test Sonuçları

Test scripti çalıştırıldı (`test_complete_flow.py`):
- ✓ 3 Scope başarıyla yüklendi
- ✓ 12 Kategori başarıyla yüklendi
- ✓ 80 Emisyon kaynağı başarıyla yüklendi
- ✓ Hesaplama başarıyla çalıştı
- ✓ Sonuçlar doğru şekilde döndü

#### Örnek Hesaplama:
- Kaynak: Coal (industrial)
- Aktivite: 100 kg
- Sonuç: 240.74 kg CO2e (0.2407 ton CO2e)
- Faktör: 2.40739 kg CO2e/kg
- Referans: Defra 2024 – UK GHG Conversion Factors

## Kullanım

### Frontend (Next.js):
```bash
cd frontend
npm run dev
```
Tarayıcıda: http://localhost:3001

### Backend (Django):
```bash
python manage.py runserver
```
API: http://127.0.0.1:8000

### Veri Girişi:
1. http://localhost:3001/login adresinden giriş yapın
2. http://localhost:3001/data-entry adresine gidin
3. Scope → Category → Source seçin
4. Aktivite verisini girin
5. "Calculate" butonuna tıklayın
6. Sonucu görün ve "Save" ile kaydedin

## Teknik Detaylar

### Emisyon Faktörleri:
Tüm emisyon faktörleri `ghg/emission_factors.py` dosyasında tanımlı:
- STATIONARY_COMBUSTION: Kömür, doğalgaz, LPG, dizel, vb.
- MOBILE_COMBUSTION: Benzin, dizel, CNG, araç-km, vb.
- FUGITIVE_EMISSIONS: Soğutucu gazlar (R-410A, R-22, vb.)
- ELECTRICITY: Elektrik şebekesi faktörleri
- PURCHASED_GOODS_GLOBAL: Plastik, metal, kağıt, cam, vb.
- BUSINESS_TRAVEL: Uçak, tren, taksi, otobüs
- EMPLOYEE_COMMUTING: Araba, otobüs, tren, motosiklet
- WASTE: Çöp, geri dönüşüm, kompost
- WATER: Su temini ve atık su arıtma
- Ve daha fazlası...

### Kaynaklar:
- IPCC 2019 (AR6 GWP)
- Defra 2024 (UK GHG Conversion Factors)
- DESNZ 2024
- Türkiye özel faktörler (ATOM KABLO ISO 14064-1)

## Sonuç

Artık sistemde **80 emisyon kaynağı** mevcut ve tümü Next.js frontend'den erişilebilir durumda. Eski Django template'lerindeki tüm kaynaklar yeni sisteme aktarıldı.
