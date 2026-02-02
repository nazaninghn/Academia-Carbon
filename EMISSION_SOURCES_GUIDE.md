# 📚 راهنمای سیستم مدیریت منابع انتشار

## 🎯 هدف

این سیستم به ادمین اجازه می‌ده که برای هر Scope (1, 2, 3)، دسته‌بندی‌ها و منابع انتشار جدید اضافه کنه.

## 📊 ساختار سلسله مراتبی

```
Scope (مثلاً Scope 1)
  └── Category (مثلاً Stationary Combustion)
      └── Source (مثلاً Natural Gas)
          └── Emission Factor (مثلاً 2.03 kg CO2e/m³)
```

## 🔑 مدل‌های اصلی

### 1️⃣ Emission Scopes
**چیه؟** سه Scope اصلی انتشار (1, 2, 3)

**کی استفاده میشه؟**
- معمولاً فقط یک بار setup میشه
- بعداً نیازی به تغییر نیست

**فیلدهای مهم:**
- Scope Number (1, 2, 3)
- Name (English + Persian)
- Icon & Color (برای نمایش)

**مثال:**
```
Scope 1 - Direct Emissions 🔥 (قرمز)
Scope 2 - Indirect Emissions ⚡ (نارنجی)
Scope 3 - Other Indirect 🌍 (آبی)
```

---

### 2️⃣ Emission Categories
**چیه؟** دسته‌بندی‌های اصلی در هر Scope

**کی استفاده میشه؟**
- وقتی می‌خوای یک دسته جدید اضافه کنی
- مثلاً: Refrigerants, Waste, Water

**فیلدهای مهم:**
- Scope (انتخاب Scope)
- Code (کد یکتا)
- Name (English + Persian)
- Icon

**مثال Scope 1:**
```
- Stationary Combustion 🏭
- Mobile Combustion 🚗
- Fugitive Emissions 💨
- Process Emissions ⚗️
```

---

### 3️⃣ Emission Sources
**چیه؟** منابع انتشار در هر دسته

**کی استفاده میشه؟**
- **اینجا ادمین بیشترین کار رو می‌کنه**
- اضافه کردن سوخت‌ها، مواد، فعالیت‌های جدید

**فیلدهای مهم:**
- Category (انتخاب دسته)
- Code (کد یکتا)
- Name (English + Persian)
- Default Unit (واحد پیش‌فرض)
- Alternative Units (واحدهای جایگزین)

**مثال Stationary Combustion:**
```
- Natural Gas (m³, kg, GJ)
- Diesel (liters, kg)
- Fuel Oil (liters, kg)
- Coal (kg, tons)
- LPG (kg, liters)
```

---

### 4️⃣ Emission Factor Data
**چیه؟** ضرایب انتشار برای هر منبع

**کی استفاده میشه؟**
- وقتی می‌خوای ضریب برای کشور جدید اضافه کنی
- وقتی ضریب آپدیت میشه (سال جدید)

**فیلدهای مهم:**
- Source (انتخاب منبع)
- Country Code (turkey, iran, global, ...)
- Factor Value (مقدار ضریب)
- Unit (واحد)
- Reference Source (منبع)
- Reference Year (سال)
- Is Default (پیش‌فرض؟)
- Data Quality (کیفیت داده)

**مثال Natural Gas:**
```
Turkey 2025:  2.03 kg CO2e/m³  (Default, High Quality)
Global 2006:  2.00 kg CO2e/m³  (Medium Quality)
Iran 2024:    1.95 kg CO2e/m³  (High Quality)
```

---

## 🚀 نحوه استفاده (گام به گام)

### مثال: اضافه کردن "Coal" به Scope 1

#### گام 1: بررسی Scope و Category
```
✅ Scope 1 موجود هست
✅ Category "Stationary Combustion" موجود هست
```

#### گام 2: اضافه کردن Source جدید
```
Admin Panel → Emission Sources → Add

Category: Stationary Combustion
Code: coal
Name (EN): Coal
Name (FA): زغال سنگ
Default Unit: kg
Alternative Units: ["tons", "GJ"]
Icon: ⚫
```

#### گام 3: اضافه کردن Emission Factor
```
Admin Panel → Emission Factor Data → Add

Source: Coal
Country: Turkey
Factor Value: 2.42
Unit: kg
Reference: Turkey 2025 Official
Year: 2025
Is Default: ✅
Quality: High
```

#### گام 4: تست
```
حالا کاربران می‌تونن "Coal" رو انتخاب کنن
و با ضریب 2.42 محاسبه میشه
```

---

## 📋 چک‌لیست ادمین

### Setup اولیه (یک بار):
- [ ] Scope 1, 2, 3 ساخته شده
- [ ] Categories اصلی اضافه شده
- [ ] Sources پرکاربرد اضافه شده
- [ ] Factors برای کشور اصلی اضافه شده

### نگهداری مداوم:
- [ ] Source جدید وقتی کاربر درخواست میده
- [ ] Factor جدید برای کشورهای جدید
- [ ] آپدیت Factors سالانه
- [ ] بررسی Quality داده‌ها

---

## 💡 نکات مهم

### ✅ انجام بده:
- از Code های یکتا استفاده کن (مثل: natural-gas)
- هر Source حداقل یک Default Factor داشته باشه
- Quality Rating رو درست تنظیم کن
- Reference Source رو حتماً بنویس

### ❌ انجام نده:
- Code تکراری نساز
- بدون Factor، Source نساز
- Factor های قدیمی رو حذف نکن (فقط Deactivate کن)
- واحدهای اشتباه استفاده نکن

---

## 🔍 سوالات متداول

**Q: چند تا Factor می‌تونم برای یک Source داشته باشم؟**
A: نامحدود! می‌تونی برای هر کشور و هر سال یک Factor داشته باشی.

**Q: Default Factor چیه؟**
A: Factor ای که وقتی کاربر کشور انتخاب نکرده، استفاده میشه.

**Q: می‌تونم Category حذف کنم؟**
A: بهتره Deactivate کنی تا داده‌های قبلی خراب نشن.

**Q: Alternative Units چطور کار می‌کنه؟**
A: کاربر می‌تونه با واحدهای مختلف محاسبه کنه (تبدیل خودکار انجام میشه).

---

## 📊 آمار فعلی سیستم

```
✅ Scopes: 3
✅ Categories: 4
✅ Sources: 5
✅ Emission Factors: 7
```

**Coverage:**
- Scope 1: 2 categories, 3 sources
- Scope 2: 1 category, 1 source
- Scope 3: 1 category, 1 source

**Countries:**
- Turkey: 4 factors
- Global: 3 factors

---

## 🎯 اولویت‌های توسعه

### فاز 1 (فعلی): ✅
- [x] Scope 1 اصلی
- [x] Scope 2 برق
- [x] Scope 3 سفر

### فاز 2 (بعدی):
- [ ] Refrigerants (Scope 1)
- [ ] Heating/Cooling (Scope 2)
- [ ] Waste (Scope 3)
- [ ] Water (Scope 3)

### فاز 3 (آینده):
- [ ] ضرایب کشورهای بیشتر
- [ ] Industry-specific factors
- [ ] Custom calculation methods

---

**آخرین آپدیت:** 2026-02-02  
**نسخه:** 1.0  
**وضعیت:** Production Ready ✅
