import os

NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://0fb641ef.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "4kE5P7fMqBEhhvsJaO-E71OBy52iyB6JL9L-pu0eaqI")

COUNTRY_NAMES = {
    # Asia
    'Indonesia': {'id': 'Indonesia', 'en': 'Indonesia'},
    'Japan': {'id': 'Jepang', 'en': 'Japan'},
    'South Korea': {'id': 'Korea Selatan', 'en': 'South Korea'},
    'North Korea': {'id': 'Korea Utara', 'en': 'North Korea'},
    'China': {'id': 'Tiongkok', 'en': 'China'},
    'Hong Kong': {'id': 'Hong Kong', 'en': 'Hong Kong'},
    'Taiwan': {'id': 'Taiwan', 'en': 'Taiwan'},
    'Thailand': {'id': 'Thailand', 'en': 'Thailand'},
    'Vietnam': {'id': 'Vietnam', 'en': 'Vietnam'},
    'Malaysia': {'id': 'Malaysia', 'en': 'Malaysia'},
    'Singapore': {'id': 'Singapura', 'en': 'Singapore'},
    'Philippines': {'id': 'Filipina', 'en': 'Philippines'},
    'India': {'id': 'India', 'en': 'India'},
    
    # America
    'United States': {'id': 'Amerika Serikat', 'en': 'United States'},
    'USA': {'id': 'Amerika Serikat', 'en': 'USA'},
    'Canada': {'id': 'Kanada', 'en': 'Canada'},
    'Mexico': {'id': 'Meksiko', 'en': 'Mexico'},
    'Brazil': {'id': 'Brasil', 'en': 'Brazil'},
    
    # Europe
    'United Kingdom': {'id': 'Inggris', 'en': 'United Kingdom'},
    'UK': {'id': 'Inggris', 'en': 'UK'},
    'France': {'id': 'Prancis', 'en': 'France'},
    'Germany': {'id': 'Jerman', 'en': 'Germany'},
    'Italy': {'id': 'Italia', 'en': 'Italy'},
    'Spain': {'id': 'Spanyol', 'en': 'Spain'},
    'Netherlands': {'id': 'Belanda', 'en': 'Netherlands'},
    
    # Default values
    'Unknown origin': {'id': 'Asal tidak diketahui', 'en': 'Unknown origin'},
    'Unknown': {'id': 'Tidak diketahui', 'en': 'Unknown'}
}
