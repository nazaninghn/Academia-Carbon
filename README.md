# Academia Carbon 🌍

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)](https://www.djangoproject.com/)
[![GitHub](https://img.shields.io/badge/GitHub-nazaninghn/Academia--Carbon-blue.svg)](https://github.com/nazaninghn/Academia-Carbon)

A comprehensive Django web application for tracking, calculating, and reporting greenhouse gas (GHG) emissions. Designed for academic institutions, research organizations, and businesses seeking ISO 14064-1 compliant emissions management.

![Academia Carbon Screenshot](https://via.placeholder.com/800x400/2d7a5f/ffffff?text=Academia+Carbon+Dashboard)

## 🚀 Features

### 📊 Emissions Management
- **Multi-Scope Tracking**: Complete Scope 1, 2, and 3 emissions calculation
- **Country-Specific Factors**: Turkey 2025 + Global emission factors database
- **Custom Factors**: Support for supplier-provided emission factors
- **Real-time Calculations**: Instant emission calculations with activity data input

### 📈 Analysis & Reporting
- **Analysis Dashboard**: Interactive charts and KPI cards with dynamic data loading
- **ISO 14064-1 Reports**: Professional PDF inventory reports with filtering
- **Scope Distribution**: Visual breakdown by emission scopes
- **Top Sources Analysis**: Identify highest emission contributors
- **Monthly Trends**: Track emissions over time

### 🎨 User Experience
- **Modern Interface**: Clean, responsive design with mobile optimization
- **Multi-language**: English and Turkish language support
- **Dashboard**: Comprehensive overview with key metrics
- **Email Notifications**: Automated alerts and updates

### 🔧 Technical Features
- **PDF Generation**: Professional reports using ReportLab
- **RESTful APIs**: JSON endpoints for data integration
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Security**: Django authentication with CSRF protection

---

## 🏗️ Architecture

### New Modules (v2.1)
- **`ghg/reporting/`**: Complete reporting system with services layer
- **Analysis Landing Cards**: Dynamic KPI cards with API integration
- **PDF Generation**: ISO 14064-1 compliant inventory reports
- **Enhanced Navigation**: Improved user experience with consistent styling

### Project Structure
```
academia-carbon/
├── ghg/                          # Main application
│   ├── models.py                 # Database models
│   ├── views.py                  # Views and logic
│   ├── urls.py                   # URL routing
│   ├── forms.py                  # Authentication forms
│   ├── emission_factors.py       # Emission calculations
│   ├── reporting/                # NEW: Reporting module
│   │   ├── services.py           # Business logic layer
│   │   ├── views.py              # Report views
│   │   └── urls.py               # Report URLs
│   └── management/
│       └── commands/
│           ├── load_sample_data.py
│           └── create_email_user.py
├── templates/                    # HTML templates
│   ├── auth/                     # Login/Signup pages
│   ├── analysis/                 # NEW: Analysis templates
│   │   ├── index.html            # Analysis landing page
│   │   └── emissions.html        # Emissions analysis
│   ├── reporting/                # NEW: Reporting templates
│   │   ├── inventory.html        # HTML report view
│   │   └── inventory_pdf.html    # PDF template
│   ├── dashboard_base.html       # Dashboard layout
│   ├── data_entry.html           # Emission calculator
│   └── emissions.html            # Emissions overview
├── static/                       # Static files
│   ├── css/
│   │   ├── style.css
│   │   ├── analysis-cards.css    # NEW: Analysis styling
│   │   └── analysis-emissions.css
│   ├── js/
│   │   ├── charts.js
│   │   ├── analysis-cards.js     # NEW: Dynamic cards
│   │   └── analysis-emissions.js
│   └── reporting/                # NEW: Report assets
│       └── pdf.css
└── carbon_tracker/               # Project settings
    ├── settings.py
    └── urls.py
```

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/nazaninghn/Academia-Carbon.git
cd Academia-Carbon
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python manage.py migrate
python manage.py load_sample_data
```

### 5. Create User
```bash
python manage.py create_email_user your@email.com SecurePassword123! --first-name "Your" --last-name "Name"
```

### 6. Run Server
```bash
python manage.py runserver
```

### 7. Access Application
```
http://127.0.0.1:8000/
```

---

## 📊 Key Features

### 1. Analysis Dashboard
- **Landing Cards**: Dynamic KPI display with real-time data
- **Interactive Charts**: Scope distribution, monthly trends, top sources
- **API Integration**: RESTful endpoints for data fetching
- **Responsive Design**: Mobile-optimized interface

### 2. Reporting System
- **ISO 14064-1 Compliance**: Professional inventory reports
- **PDF Generation**: High-quality reports with ReportLab
- **Filtering Options**: Date range, scope, country filters
- **Executive Summary**: Key metrics and totals
- **Methodology Notes**: Transparent calculation methods

### 3. Emission Calculation
- **Scope 1**: Direct emissions (fuel combustion, vehicles, refrigerants)
- **Scope 2**: Indirect emissions (electricity, heating, cooling)
- **Scope 3**: Other indirect emissions (travel, waste, commuting)
- **Custom Factors**: Supplier-provided emission factors
- **Real-time Updates**: Instant calculation results

### 4. Data Management
- **Country-Specific Factors**: Turkey 2025 + Global standards
- **DESNZ 2024 Standards**: Latest UK government factors
- **IPCC AR6 GWP**: Updated global warming potentials
- **Supplier Tracking**: Emission source management

---

## 🔌 API Endpoints

### Analysis APIs
- `GET /api/analysis/emissions/summary/` - Emissions summary for cards
- `GET /api/analysis/scope-distribution/` - Scope breakdown data
- `GET /api/analysis/monthly-trends/` - Monthly emissions trends
- `GET /api/analysis/top-sources/` - Top emission sources

### Reporting APIs
- `GET /en/reporting/inventory` - HTML inventory report
- `GET /en/reporting/inventory?format=pdf` - PDF inventory report
- `GET /en/reporting/inventory?from=2025-01-01&to=2025-12-31` - Filtered report

### Core APIs
- `POST /api/calculate/` - Calculate emissions
- `GET /api/user-summary/` - User emission summary
- `GET /api/country/<country_code>/` - Country-specific data

---

## 🎨 UI Components

### Analysis Landing Cards
```javascript
// Dynamic KPI cards with API integration
fetch('/api/analysis/emissions/summary/')
  .then(response => response.json())
  .then(data => {
    document.getElementById('kpiTotal').textContent = data.total_tco2e;
    document.getElementById('kpiRecords').textContent = data.records;
  });
```

### Reporting Interface
- **Modern Cards**: Clean, professional design
- **Gradient Buttons**: Consistent styling across the application
- **Responsive Tables**: Mobile-optimized data display
- **Filter Examples**: User-friendly filtering options

---

## 📋 Emission Factors

### Turkey 2025 (Updated)
| Source | Factor | Unit |
|--------|--------|------|
| Electricity Grid | 0.452 kg CO2e | per kWh |
| Natural Gas | 2.03 kg CO2e | per m³ |
| Motor Gasoline | 69.56 kg CO2e | per GJ |
| Gas/Diesel Oil | 74.1 kg CO2e | per GJ |

### DESNZ 2024 Standards
| Source | Factor | Unit |
|--------|--------|------|
| On-Road Diesel | 2.51 kg CO2e | per liter |
| On-Road Petrol | 2.16 kg CO2e | per liter |
| R-410A Refrigerant | 2088 kg CO2e | per kg |
| Off-Road Diesel | 74.4 kg CO2e | per GJ |

---

## 🛠️ Technology Stack

- **Backend**: Django 5.2.8, Python 3.8+
- **Database**: SQLite3 (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Charts**: Chart.js 4.4.0
- **PDF Generation**: ReportLab
- **Styling**: Bootstrap 5.3, Custom CSS
- **Icons**: Font Awesome 6.4

---

## 🚀 Deployment

### Using Deploy Script
```bash
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run checks
python manage.py check

# Migrate database
python manage.py migrate
```

### Environment Variables
```bash
# .env file
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,127.0.0.1
DATABASE_URL=postgres://user:pass@host:port/db
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
- Model tests for emission calculations
- View tests for all endpoints
- Template rendering tests
- API response validation

---

## 📚 Documentation

- **INSTALLATION.md** - Detailed setup guide
- **QUICKSTART.md** - Quick setup guide
- **SECURITY.md** - Security guidelines
- **CONTRIBUTING.md** - Contribution guidelines
- **CHANGELOG.md** - Version history
- **TROUBLESHOOTING.md** - Common issues and solutions

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### Data Sources
- **IPCC**: Intergovernmental Panel on Climate Change
- **DESNZ**: UK Department for Energy Security and Net Zero
- **Turkish Ministry of Environment**: Official GHG guidelines
- **EPA**: US Environmental Protection Agency

### Standards Compliance
- ISO 14064-1: Greenhouse gas inventories
- GHG Protocol: Corporate accounting standards
- IPCC 2006 Guidelines: National inventories
- AR6 GWP Values: Latest warming potentials

---

## 📊 Version Information

- **Version**: 2.1.0
- **Last Updated**: December 2025
- **Data Year**: 2025 (Current)
- **Status**: Production Ready ✅

---

**Academia Carbon** - Professional GHG Management for Academic Excellence 🎓🌍

*Built with ❤️ for environmental sustainability and academic research*