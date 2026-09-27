"""
Seed the industry list with the NACE Rev.2 sections (the classification used
by TÜİK and Eurostat), in English and Turkish. Industry type is only a label
on emission records; it is not used in any calculation.

Existing rows are left untouched, and nothing is deleted on reverse.
"""

from django.db import migrations

NACE_SECTIONS = [
    ('A', 'Agriculture, forestry and fishing', 'Tarım, ormancılık ve balıkçılık'),
    ('B', 'Mining and quarrying', 'Madencilik ve taş ocakçılığı'),
    ('C', 'Manufacturing', 'İmalat'),
    ('D', 'Electricity, gas, steam and air conditioning supply',
     'Elektrik, gaz, buhar ve iklimlendirme üretimi ve dağıtımı'),
    ('E', 'Water supply; sewerage, waste management and remediation',
     'Su temini; kanalizasyon, atık yönetimi ve iyileştirme faaliyetleri'),
    ('F', 'Construction', 'İnşaat'),
    ('G', 'Wholesale and retail trade; repair of motor vehicles and motorcycles',
     'Toptan ve perakende ticaret; motorlu kara taşıtlarının ve motosikletlerin onarımı'),
    ('H', 'Transportation and storage', 'Ulaştırma ve depolama'),
    ('I', 'Accommodation and food service activities', 'Konaklama ve yiyecek hizmeti faaliyetleri'),
    ('J', 'Information and communication', 'Bilgi ve iletişim'),
    ('K', 'Financial and insurance activities', 'Finans ve sigorta faaliyetleri'),
    ('L', 'Real estate activities', 'Gayrimenkul faaliyetleri'),
    ('M', 'Professional, scientific and technical activities', 'Mesleki, bilimsel ve teknik faaliyetler'),
    ('N', 'Administrative and support service activities', 'İdari ve destek hizmet faaliyetleri'),
    ('O', 'Public administration and defence; compulsory social security',
     'Kamu yönetimi ve savunma; zorunlu sosyal güvenlik'),
    ('P', 'Education', 'Eğitim'),
    ('Q', 'Human health and social work activities', 'İnsan sağlığı ve sosyal hizmet faaliyetleri'),
    ('R', 'Arts, entertainment and recreation', 'Kültür, sanat, eğlence, dinlence ve spor'),
    ('S', 'Other service activities', 'Diğer hizmet faaliyetleri'),
]


def seed(apps, schema_editor):
    IndustryType = apps.get_model('ghg', 'IndustryType')
    for section, name, name_tr in NACE_SECTIONS:
        IndustryType.objects.get_or_create(
            name=name,
            defaults={'name_tr': name_tr, 'code': f'NACE {section}', 'is_active': True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('ghg', '0018_industrytype_name_tr'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
