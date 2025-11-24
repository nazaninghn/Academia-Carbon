# Carbon Tracker - Quick Reference 🚀

## 🎯 Quick Start (30 seconds)

1. Login: `admin` / `admin123`
2. Click "Emission Management"
3. Select Country: 🇹🇷 Turkey
4. Choose Scope → Select Source → Enter Data → Calculate
5. View results in "History"

---

## 📊 The 3 Scopes

| Scope | What | Examples |
|-------|------|----------|
| **1** | Direct emissions you control | Company cars, boilers, AC leaks |
| **2** | Purchased energy | Electricity, district heating |
| **3** | Everything else | Business travel, waste, suppliers |

---

## 🇹🇷 Turkey Quick Factors

### Most Used

| Source | Factor | Unit |
|--------|--------|------|
| Electricity | 0.486 | kg CO2e/kWh |
| Natural Gas | 2.03 | kg CO2e/m³ |
| Diesel | 2.68 | kg CO2e/liter |
| Gasoline | 2.31 | kg CO2e/liter |
| LPG (car) | 0.175 | kg CO2e/km |

### Transportation

| Mode | Factor | Unit |
|------|--------|------|
| Domestic Flight | 0.245 | kg CO2e/km |
| Train (TCDD) | 0.035 | kg CO2e/km |
| Metro | 0.028 | kg CO2e/km |
| Bus | 0.095 | kg CO2e/km |
| Dolmuş | 0.082 | kg CO2e/km |
| Car (avg) | 0.185 | kg CO2e/km |

### Waste

| Type | Factor | Unit |
|------|--------|------|
| Landfill | 0.62 | kg CO2e/kg |
| Recyclable | 0.021 | kg CO2e/kg |
| Compost | 0.018 | kg CO2e/kg |

---

## 💡 Quick Examples

### Example 1: Monthly Office Electricity
```
Input: 5,000 kWh
Calculation: 5,000 × 0.486 = 2,430 kg CO2e
Result: 2.43 tons CO2e
```

### Example 2: Business Trip (Istanbul → Ankara)
```
Distance: 450 km
Mode: Domestic Flight
Calculation: 450 × 0.245 = 110.25 kg CO2e
Result: 0.11 tons CO2e
```

### Example 3: Company Car (Monthly)
```
Fuel: 200 liters diesel
Calculation: 200 × 2.68 = 536 kg CO2e
Result: 0.536 tons CO2e
```

### Example 4: Office Waste
```
Waste: 300 kg to landfill
Calculation: 300 × 0.62 = 186 kg CO2e
Result: 0.186 tons CO2e
```

---

## 🔍 Where to Find Data

| Data Type | Source |
|-----------|--------|
| Electricity | Monthly bill, meter reading |
| Natural Gas | Monthly bill, İGDAŞ invoice |
| Fuel | Gas station receipts, fuel cards |
| Travel | Booking confirmations, expense reports |
| Waste | Waste management invoices |

---

## ⚠️ Common Mistakes

| ❌ Wrong | ✓ Right |
|---------|---------|
| Forget to select Turkey | Always select country first |
| Use estimates | Use actual bills/invoices |
| Mix units (kWh vs MWh) | Check unit carefully |
| Enter yearly data as monthly | Be consistent with periods |
| Skip Scope 3 | Include at least travel & waste |

---

## 🎨 Understanding Colors

- 🔴 **Red** = Scope 1 (Direct)
- 🟠 **Orange** = Scope 2 (Energy)
- 🔵 **Blue** = Scope 3 (Indirect)
- 🟢 **Green** = Results/Success

---

## 📱 Navigation

```
Dashboard → Overview & charts
Data Entry → Calculate emissions
History → View all records
Analysis → Coming soon
Reporting → Coming soon
```

---

## 🆘 Quick Troubleshooting

**Problem**: Can't calculate
- ✓ Check country selected
- ✓ Check source selected
- ✓ Check activity data > 0

**Problem**: Results seem wrong
- ✓ Verify decimal point
- ✓ Check unit (kWh not MWh)
- ✓ Confirm country

**Problem**: No history showing
- ✓ Click "Calculate" button
- ✓ Look for "Saved to History" message
- ✓ Refresh page

---

## 📏 Unit Conversions

```
1 ton = 1,000 kg
1 MWh = 1,000 kWh
1 m³ natural gas ≈ 10.55 kWh
1 liter diesel ≈ 10 kWh
1 gallon = 3.785 liters
1 mile = 1.609 km
```

---

## 🎯 Monthly Checklist

- [ ] Enter all electricity bills
- [ ] Enter all gas bills
- [ ] Log fuel purchases
- [ ] Record business travel
- [ ] Track waste disposal
- [ ] Review history totals

---

## 📞 Need Help?

1. Check `USER_GUIDE.md` (full guide)
2. Check `TURKEY_EMISSION_FACTORS.md` (Turkey details)
3. Check `QUICKSTART.md` (setup)
4. Contact admin

---

## 🌟 Pro Tips

💡 **Tip 1**: Calculate monthly for better tracking  
💡 **Tip 2**: Add descriptions to remember context  
💡 **Tip 3**: Use supplier field for easy filtering  
💡 **Tip 4**: Check history regularly for trends  
💡 **Tip 5**: Turkey factors are more accurate for Turkey!

---

**Version**: 1.0 | **Updated**: Nov 2025 | **Language**: English/Turkish
