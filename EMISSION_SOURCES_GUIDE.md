# 📚 Emission Sources Management System Guide

## 🎯 Purpose

This system allows admins to add new categories and emission sources for each Scope (1, 2, 3).

## 📊 Hierarchical Structure

```
Scope (e.g., Scope 1)
  └── Category (e.g., Stationary Combustion)
      └── Source (e.g., Natural Gas)
          └── Emission Factor (e.g., 2.03 kg CO2e/m³)
```

## 🔑 Main Models

### 1️⃣ Emission Scopes
**What is it?** The three main emission scopes (1, 2, 3)

**When to use?**
- Usually set up only once
- No need to change later

**Important fields:**
- Scope Number (1, 2, 3)
- Name (English + Turkish)
- Icon & Color (for display)

**Example:**
```
Scope 1 - Direct Emissions 🔥 (Red)
Scope 2 - Indirect Emissions ⚡ (Orange)
Scope 3 - Other Indirect 🌍 (Blue)
```

---

### 2️⃣ Emission Categories
**What is it?** Main categories within each Scope

**When to use?**
- When you want to add a new category
- e.g., Refrigerants, Waste, Water

**Important fields:**
- Scope (Select Scope)
- Code (Unique code)
- Name (English + Turkish)
- Icon

**Scope 1 Example:**
```
- Stationary Combustion 🏭
- Mobile Combustion 🚗
- Fugitive Emissions 💨
- Process Emissions ⚗️
```

---

### 3️⃣ Emission Sources
**What is it?** Emission sources within each category

**When to use?**
- **This is where admins do most of their work**
- Adding new fuels, materials, activities

**Important fields:**
- Category (Select category)
- Code (Unique code)
- Name (English + Turkish)
- Default Unit (Default unit)
- Alternative Units (Alternative units)

**Stationary Combustion Example:**
```
- Natural Gas (m³, kg, GJ)
- Diesel (liters, kg)
- Fuel Oil (liters, kg)
- Coal (kg, tons)
- LPG (kg, liters)
```

---

### 4️⃣ Emission Factor Data
**What is it?** Emission factors for each source

**When to use?**
- When you want to add a factor for a new country
- When a factor is updated (new year)

**Important fields:**
- Source (Select source)
- Country Code (turkey, iran, global, ...)
- Factor Value (Factor value)
- Unit (Unit)
- Reference Source (Source)
- Reference Year (Year)
- Is Default (Default?)
- Data Quality (Data quality)

**Natural Gas Example:**
```
Turkey 2025:  2.03 kg CO2e/m³  (Default, High Quality)
Global 2006:  2.00 kg CO2e/m³  (Medium Quality)
Iran 2024:    1.95 kg CO2e/m³  (High Quality)
```

---

## 🚀 How to Use (Step by Step)

### Example: Adding "Coal" to Scope 1

#### Step 1: Check Scope and Category
```
✅ Scope 1 exists
✅ Category "Stationary Combustion" exists
```

#### Step 2: Add New Source
```
Admin Panel → Emission Sources → Add

Category: Stationary Combustion
Code: coal
Name (EN): Coal
Name (TR): Kömür
Default Unit: kg
Alternative Units: ["tons", "GJ"]
Icon: ⚫
```

#### Step 3: Add Emission Factor
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

#### Step 4: Test
```
Now users can select "Coal"
and it will calculate with factor 2.42
```

---

## 📋 Admin Checklist

### Initial Setup (One time):
- [ ] Scope 1, 2, 3 created
- [ ] Main categories added
- [ ] Common sources added
- [ ] Factors for main country added

### Ongoing Maintenance:
- [ ] New source when user requests
- [ ] New factor for new countries
- [ ] Annual factor updates
- [ ] Data quality review

---

## 💡 Important Tips

### ✅ Do:
- Use unique codes (e.g., natural-gas)
- Each source should have at least one default factor
- Set quality rating correctly
- Always write reference source

### ❌ Don't:
- Don't create duplicate codes
- Don't create source without factor
- Don't delete old factors (just deactivate)
- Don't use wrong units

---

## 🔍 Frequently Asked Questions

**Q: How many factors can I have for one source?**
A: Unlimited! You can have one factor for each country and each year.

**Q: What is a default factor?**
A: The factor used when the user hasn't selected a country.

**Q: Can I delete a category?**
A: Better to deactivate it so previous data isn't broken.

**Q: How do alternative units work?**
A: Users can calculate with different units (automatic conversion is performed).

---

## 📊 Current System Stats

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

## 🎯 Development Priorities

### Phase 1 (Current): ✅
- [x] Main Scope 1
- [x] Scope 2 electricity
- [x] Scope 3 travel

### Phase 2 (Next):
- [ ] Refrigerants (Scope 1)
- [ ] Heating/Cooling (Scope 2)
- [ ] Waste (Scope 3)
- [ ] Water (Scope 3)

### Phase 3 (Future):
- [ ] More country factors
- [ ] Industry-specific factors
- [ ] Custom calculation methods

---

**Last Updated:** 2026-02-02  
**Version:** 1.0  
**Status:** Production Ready ✅
