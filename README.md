# Academia Carbon 🌍

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)](https://www.djangoproject.com/)

A Django web application for tracking and calculating greenhouse gas (GHG) emissions. Designed for academic institutions and research organizations.

![Academia Carbon Screenshot](https://via.placeholder.com/800x400/7ea05a/ffffff?text=Academia+Carbon+Dashboard)

## Features ✨

- 📊 Calculate emissions across Scope 1, 2, and 3
- 🌍 Country-specific emission factors (Turkey 2025 + Global)
- 📈 Interactive charts and visualizations
- 📱 Modern, responsive design
- 🎓 Academic-focused interface
- 🔐 Email-based authentication
- 📝 Emission history tracking
- 🔬 Research-grade accuracy
- 📝 Emission history tracking
- 🔬 Research-grade accuracy

---

## Quick Start 🚀

### 1. Activate Virtual Environment
```bash
.\venv\Scripts\activate
```

### 2. Run the Server
```bash
python manage.py runserver
```

### 3. Access the Application
```
http://127.0.0.1:8000/
```

### 4. Login
- **Email**: `admin@carbon.com`
- **Password**: `admin123`

Or create a new account at the signup page.

---

## Test Users

| Email | Password | Role |
|-------|----------|------|
| admin@carbon.com | admin123 | Administrator |
| test@example.com | test1234 | Test User |

---

## Creating New Users

### Via Web Interface
1. Go to: `http://127.0.0.1:8000/en/signup/`
2. Fill in the registration form
3. Start tracking emissions

### Via Command Line
```bash
python manage.py create_email_user your@email.com password123 --first-name "John" --last-name "Doe"
```

---

## Project Structure 📁

```
academia-carbon/
├── ghg/                          # Main application
│   ├── models.py                 # Database models
│   ├── views.py                  # Views and logic
│   ├── urls.py                   # URL routing
│   ├── forms.py                  # Authentication forms
│   ├── emission_factors.py       # Emission calculations
│   └── management/
│       └── commands/
│           ├── load_sample_data.py
│           └── create_email_user.py
├── templates/                    # HTML templates
│   ├── auth/                     # Login/Signup pages
│   ├── dashboard_base.html       # Dashboard layout
│   ├── data_entry.html           # Emission calculator
│   ├── emission_history.html     # History view
│   └── user_guide.html           # User guide
├── static/                       # Static files
│   ├── css/style.css
│   └── js/
│       ├── charts.js
│       └── dashboard.js
└── carbon_tracker/               # Project settings
    ├── settings.py
    └── urls.py
```

---

## Key Features

### 1. Emission Calculation
- **Scope 1**: Direct emissions (fuel combustion, vehicles, refrigerants)
- **Scope 2**: Indirect emissions (electricity, heating, cooling)
- **Scope 3**: Other indirect emissions (travel, waste, commuting)

### 2. Country-Specific Factors
- **Turkey 2025**: Updated emission factors based on Turkey Energy Strategy
- **Global Average**: International standards (IPCC, EPA, DEFRA)

### 3. Emission History
- Track all calculations
- Filter by scope
- View trends over time
- Export data

### 4. User Management
- Email-based authentication
- Secure password hashing
- User-specific emission records

---

## Emission Factors

### Turkey 2025 (Updated)

| Source | Factor | Unit |
|--------|--------|------|
| Electricity Grid | 0.452 kg CO2e | per kWh |
| Natural Gas | 1.99 kg CO2e | per m³ |
| Gasoline Car | 0.172 kg CO2e | per km |
| Electric Car | 0.045 kg CO2e | per km |
| Domestic Flight | 0.232 kg CO2e | per km |
| Landfill Waste | 0.54 kg CO2e | per kg |

### Global Average

| Source | Factor | Unit |
|--------|--------|------|
| Electricity Grid | 0.475 kg CO2e | per kWh |
| Natural Gas | 2.0 kg CO2e | per m³ |
| Gasoline | 2.31 kg CO2e | per liter |
| Diesel | 2.68 kg CO2e | per liter |

For complete emission factors, see `EMISSION_FACTORS_2025.md`

---

## Documentation 📚

- **QUICKSTART.md** - Quick setup guide
- **USER_GUIDE.md** - Complete user manual
- **QUICK_REFERENCE.md** - Quick reference card
- **TURKEY_EMISSION_FACTORS.md** - Turkey-specific factors
- **EMISSION_FACTORS_2025.md** - 2025 updates and projections

---

## Technology Stack 💻

- **Backend**: Django 5.2.8
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Styling**: Bootstrap 5.3

---

## API Endpoints 🔌

### Public Endpoints
- `GET /` - Redirect to login
- `GET /en/login/` - Login page
- `GET /en/signup/` - Signup page

### Authenticated Endpoints
- `GET /en/` - Dashboard
- `GET /en/data-entry/` - Emission calculator
- `GET /en/history/` - Emission history
- `GET /en/user-guide/` - User guide
- `POST /en/api/calculate/` - Calculate emissions
- `GET /en/api/user-summary/` - User emission summary

---

## Database Models

### Country
- `name`: Country name
- `code`: ISO country code

### EmissionData
- `country`: Foreign key to Country
- `year`: Data year
- `co2_emissions`: CO2 emissions
- `total_ghg`: Total GHG emissions

### EmissionRecord
- `user`: Foreign key to User
- `scope`: Emission scope (1, 2, or 3)
- `category`: Emission category
- `source`: Emission source
- `activity_data`: Amount of activity
- `emissions_kg`: Calculated emissions
- `country`: Country used for calculation
- `created_at`: Timestamp

---

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Loading Sample Data
```bash
python manage.py load_sample_data
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

---

## Contributing 🤝

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Changelog 📋

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

---

## Support 💬

For questions or issues:
- 📖 Check the [documentation files](.)
- 📚 Review the [User Guide](USER_GUIDE.md)
- 🐛 [Open an issue](https://github.com/yourusername/academia-carbon/issues)
- 💡 [Start a discussion](https://github.com/yourusername/academia-carbon/discussions)

---

## Acknowledgments 🙏

### Data Sources
- **IEA**: International Energy Agency
- **IPCC**: Intergovernmental Panel on Climate Change
- **EPA**: US Environmental Protection Agency
- **DEFRA**: UK Department for Environment
- **Turkish Ministry of Environment**: Official GHG guidelines

### Built With
- [Django](https://www.djangoproject.com/) - Web framework
- [Chart.js](https://www.chartjs.org/) - Data visualization
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Font Awesome](https://fontawesome.com/) - Icons

---

## Credits

### Data Sources
- **IEA**: International Energy Agency
- **IPCC**: Intergovernmental Panel on Climate Change
- **EPA**: US Environmental Protection Agency
- **DEFRA**: UK Department for Environment
- **Turkish Ministry of Environment**: Official GHG guidelines

### Emission Factor Standards
- IPCC 2006 Guidelines
- GHG Protocol
- ISO 14064
- Turkey Energy Strategy 2025

---

## Version

- **Version**: 2.0
- **Last Updated**: November 2025
- **Data Year**: 2025 (Projected)
- **Status**: Production Ready ✅

---

**Academia Carbon** - Environmental Solutions for Academic Excellence 🎓🌍
