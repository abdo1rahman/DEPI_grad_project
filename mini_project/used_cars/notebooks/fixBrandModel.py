import pandas as pd

# (Brand, model) -> (Brand, model): wrong brand split / brand-swapped entries
BRAND_FIX = {
    ('Toyota Land','Cruiser'):('Toyota','Land Cruiser'),
    ('Toyota Land','Cruiser Prado'):('Toyota','Land Cruiser Prado'),
    ('Force','Motors FM Gurkha'):('Force','Gurkha'),
    ('Force','Motors FM Force One Test'):('Force','Force One'),
    ('Force','Motors FM Trax Cruiser'):('Force','Trax Cruiser'),
    ('Ashok','Leyland Stile'):('Ashok Leyland','Stile'),
    ('Mahindra','Ssangyong Rexton'):('Ssangyong','Rexton'),
    ('Mahindra','Ssangyong-Rexton'):('Ssangyong','Rexton'),
    ('Mahindra','Rexton'):('Ssangyong','Rexton'),
    ('Mahindra','Renault Logan'):('Mahindra','Logan'),
    ('Isuzu','Hi-Lande Isuzu Hi-Lander'):('Isuzu','Hi-Lander'),
}

# Tier 1: spelling / spacing / case / junk-suffix variants of the SAME model
MODEL_FIX = {
    ' Wagon R':'Wagon R','Wagon-R':'Wagon R','Wagon R 1.0':'Wagon R','Wagon-R-1-0':'Wagon R',
    'Alto-800':'Alto 800','Alto-K10':'Alto K10','Celerio-X':'Celerio X',
    'S-Cross':'S Cross','S-Cross1':'S Cross','Fronx ':'Fronx','Sx4':'SX4','Zen-Estilo':'Zen Estilo',
    'Vitara-Brezza':'Vitara Brezza','maruti-suzuki-brezza':'Brezza','maruti-suzuki-dzire':'Dzire',
    'Swift-Dzire':'Swift Dzire','Baleno-RS':'Baleno RS',
    'Punch ':'Punch','tata-punch':'Punch',
    'Scorpio-N':'Scorpio N','XUV300':'XUV 300','TUV 300-plus':'TUV 300 Plus','KUV100 NXT':'KUV 100 NXT',
    'EON':'Eon','CRV':'CR-V','WRV':'WR-V','MUX':'MU-X','RediGO':'Redi Go','Grande Punto':'Grand Punto',
    'S 80':'S80','XC 90':'XC90','VentoTest':'Vento',
    'A-class Limousine':'A-Class Limousine','C Class':'C-Class','G Class':'G-Class','G':'G-Class',
    'GLA Class':'GLA','GLC Class':'GLC','GLE Class':'GLE','GLE COUPE':'GLE Coupe',
    'OptraSRV':'Optra SRV','CERATO':'Cerato','MICRA PRIMO':'Micra Primo','PATROL':'Patrol','ASTOR':'Astor',
    '718 CAYMAN':'Cayman','5 Series Gt':'5 Series GT',
}

# Tier 2 (OPTIONAL, judgment calls): generation / facelift / trim names -> parent model
TIER2 = {
    ('Hyundai','Elite i20'):'i20',('Hyundai','New i20'):'i20',
    ('Hyundai','Santro Xing'):'Santro',('Hyundai','New Santro'):'Santro',
    ('Hyundai','Fluidic Verna'):'Verna',('Hyundai','New Verna'):'Verna',
    ('Hyundai','Creta Facelift'):'Creta',('Hyundai','New Elantra'):'Elantra',
    ('Hyundai','Accent Hatchback'):'Accent',('Hyundai','Grand i10 Prime'):'Grand i10',
    ('Hyundai','Xcent Prime'):'Xcent',('Honda','New Accord'):'Accord',('Renault','New Duster'):'Duster',
    ('Mahindra','Five-door Thar'):'Thar Roxx',('Maruti Suzuki','New-gen Swift'):'Swift',
    ('Maruti Suzuki','Swift Dzire'):'Dzire',('Maruti Suzuki','Swift-Dzire-Tour'):'Dzire',
    ('Mini','Cooper 3 DOOR'):'3 DOOR',('Mini','Cooper 5 DOOR'):'5 DOOR',('Mini','Cooper Countryman'):'Countryman',
    ('Volvo','S60 Cross Country'):'S60',('Tata','Safari Storme'):'Safari',
    ('BMW','5 Series GT'):'5 Series GT',('BMW','6 Series GT'):'6 Series GT',
}

def fix_brand_model(df, tier2=False):
    df = df.copy()
    b, m = df['Brand'].copy(), df['model'].copy()
    for (ob, om), (nb, nm) in BRAND_FIX.items():
        mask = (b == ob) & (m == om); b[mask], m[mask] = nb, nm
    m = m.replace(MODEL_FIX)
    if tier2:
        for (bb, om), nm in TIER2.items():
            m[(b == bb) & (m == om)] = nm
    df['Brand'], df['model'] = b.str.strip(), m.str.strip()
    df['brand_model'] = df['Brand'] + ',' + df['model']
    return df

if __name__ == '__main__':
    df = pd.read_csv('cleaned_used_cars_dataset.csv')
    print('before:', (df.Brand + ',' + df.model).nunique())
    print('tier 1:', fix_brand_model(df).brand_model.nunique())
    print('tier 1+2:', fix_brand_model(df, tier2=True).brand_model.nunique())