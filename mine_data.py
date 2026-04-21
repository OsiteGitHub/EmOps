# Copyright 2026 EmOps
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Global Mine Database — Active & Abandoned Mines + Rare Earth Mining Pits
Sources: USGS Mineral Resources Data System (MRDS), Global Energy Monitor Coal Mine Tracker,
ICMM Global Mining datasets, AML (Abandoned Mine Lands) inventory programs,
EJAtlas (Environmental Justice Atlas), ScienceDirect research papers,
Nature journal studies, Australia DEIS (~50,000+ abandoned sites),
Canada Ontario AML (5,700+), South Africa DMRE (6,000+ abandoned),
UNEP Global Mercury Assessment, World Bank Mining databases,
Satellite analyses (Landsat, Sentinel-2), Country mining inventories.
"""

ABANDONED_MINES = [
    # ===== NORTH AMERICA =====
    # United States — AML Inventory: ~500,000 abandoned hardrock mine features
    {"name": "Iron Mountain Mine", "lat": 40.67, "lon": -122.52, "country": "United States", "state": "California", "type": "Abandoned Mine", "mineral": "Iron/Pyrite", "status": "Abandoned", "severity": "Critical", "issue": "Acid mine drainage — produces most acidic natural water on Earth (pH 0.5)", "source": "USEPA Superfund / USGS", "year_abandoned": 1963, "area_ha": 650},
    {"name": "Tar Creek Superfund Site", "lat": 36.94, "lon": -94.85, "country": "United States", "state": "Oklahoma", "type": "Abandoned Mine", "mineral": "Lead/Zinc", "status": "Abandoned", "severity": "Critical", "issue": "Heavy metal contamination, chat piles covering 40+ km², elevated blood lead in children", "source": "USEPA Superfund", "year_abandoned": 1970, "area_ha": 4000},
    {"name": "Berkeley Pit", "lat": 46.01, "lon": -112.53, "country": "United States", "state": "Montana", "type": "Abandoned Mine", "mineral": "Copper", "status": "Abandoned", "severity": "Critical", "issue": "Toxic lake (pH 2.5), 1995 Snow Geese mass die-off; water rising toward groundwater", "source": "USEPA / USGS MRDS", "year_abandoned": 1982, "area_ha": 600},
    {"name": "Bunker Hill Superfund Site", "lat": 47.54, "lon": -116.13, "country": "United States", "state": "Idaho", "type": "Abandoned Mine", "mineral": "Lead/Silver/Zinc", "status": "Abandoned", "severity": "Critical", "issue": "1,500 km² contaminated, largest US Superfund site; lead poisoning legacy", "source": "USEPA / USGS MRDS", "year_abandoned": 1981, "area_ha": 150000},
    {"name": "Colorado Uranium Mill Tailings (Moab)", "lat": 38.57, "lon": -109.55, "country": "United States", "state": "Utah", "type": "Abandoned Mine", "mineral": "Uranium", "status": "Abandoned", "severity": "Critical", "issue": "16 million tonnes radioactive tailings adjacent to Colorado River", "source": "DOE UMTRA Program", "year_abandoned": 1984, "area_ha": 130},
    {"name": "Summitville Mine", "lat": 37.43, "lon": -106.58, "country": "United States", "state": "Colorado", "type": "Abandoned Mine", "mineral": "Gold/Silver", "status": "Abandoned", "severity": "High", "issue": "Heap leach cyanide spill killed 27 km of Alamosa River", "source": "USEPA / Colorado DRMS", "year_abandoned": 1992, "area_ha": 280},
    {"name": "Mount Polley Mine Area (US side)", "lat": 52.53, "lon": -121.60, "country": "United States", "state": "Washington", "type": "Abandoned Mine", "mineral": "Copper/Gold", "status": "Abandoned", "severity": "Moderate", "issue": "Historic acid drainage into tributaries", "source": "USGS MRDS", "year_abandoned": 1955},
    {"name": "Smuggler Mountain Mine", "lat": 39.20, "lon": -106.80, "country": "United States", "state": "Colorado", "type": "Abandoned Mine", "mineral": "Silver/Lead", "status": "Abandoned", "severity": "High", "issue": "Residential area overlays contaminated mine waste; lead, cadmium in soil", "source": "USEPA", "year_abandoned": 1920},
    {"name": "Picher Mining District (Tri-State)", "lat": 36.98, "lon": -94.83, "country": "United States", "state": "Oklahoma", "type": "Abandoned Mine", "mineral": "Lead/Zinc", "status": "Abandoned", "severity": "Critical", "issue": "Entire town evacuated 2009; chat piles leach zinc/cadmium into groundwater", "source": "USEPA Superfund Priority List", "year_abandoned": 1970, "area_ha": 2800},
    {"name": "Animas River Gold King Mine Spill", "lat": 37.89, "lon": -107.66, "country": "United States", "state": "Colorado", "type": "Abandoned Mine", "mineral": "Gold/Silver", "status": "Abandoned", "severity": "Critical", "issue": "2015 blowout released 11M gallons of acid mine drainage; 563 km of river contaminated", "source": "EPA Incident Report 2015", "year_abandoned": 1991, "area_ha": 200},
    {"name": "Formosa Mine", "lat": 42.90, "lon": -123.84, "country": "United States", "state": "Oregon", "type": "Abandoned Mine", "mineral": "Copper/Zinc", "status": "Abandoned", "severity": "High", "issue": "Acid drainage eliminated fish from 20 km of South Umpqua River", "source": "Oregon DEQ", "year_abandoned": 1937},
    {"name": "Leviathan Mine", "lat": 38.69, "lon": -119.65, "country": "United States", "state": "California", "type": "Abandoned Mine", "mineral": "Sulfur/Copper", "status": "Abandoned", "severity": "High", "issue": "Sulfuric acid drainage into antelope Creek killed all fish", "source": "USEPA Superfund", "year_abandoned": 1962},
    {"name": "Penn Mine", "lat": 38.22, "lon": -120.75, "country": "United States", "state": "California", "type": "Abandoned Mine", "mineral": "Copper/Zinc", "status": "Abandoned", "severity": "High", "issue": "AMD impacting Mokelumne River watershed", "source": "California DTSC", "year_abandoned": 1942},
    {"name": "Kennecott Utah Copper (Bingham Canyon)", "lat": 40.53, "lon": -112.15, "country": "United States", "state": "Utah", "type": "Active Mine", "mineral": "Copper/Gold/Silver/Molybdenum", "status": "Active", "severity": "Moderate", "issue": "Largest open-pit copper mine in world; tailings impoundment >100 km²", "source": "USGS / Rio Tinto", "area_ha": 7700},
    {"name": "Morenci Mine", "lat": 33.07, "lon": -109.37, "country": "United States", "state": "Arizona", "type": "Active Mine", "mineral": "Copper", "status": "Active", "severity": "Moderate", "issue": "Largest US copper producer; pit visible from space; tailings >5000 ha", "source": "Freeport-McMoRan / USGS", "area_ha": 5200},

    # Canada — 5,700+ abandoned mines in Ontario alone
    {"name": "Giant Mine (Yellowknife)", "lat": 62.49, "lon": -114.36, "country": "Canada", "state": "Northwest Territories", "type": "Abandoned Mine", "mineral": "Gold", "status": "Abandoned", "severity": "Critical", "issue": "237,000 tonnes arsenic trioxide stored underground; permafrost thaw risks massive release", "source": "GNWT / INAC Canada AML Inventory", "year_abandoned": 2004, "area_ha": 913},
    {"name": "Faro Mine", "lat": 62.23, "lon": -133.35, "country": "Canada", "state": "Yukon", "type": "Abandoned Mine", "mineral": "Lead/Zinc", "status": "Abandoned", "severity": "Critical", "issue": "Largest AML liability in Canada (~C$2B remediation); 70M tonnes tailings, acid drainage", "source": "Crown-Indigenous Relations Canada / Yukon Government", "year_abandoned": 1998, "area_ha": 2500},
    {"name": "Britannia Mine", "lat": 49.61, "lon": -123.20, "country": "Canada", "state": "British Columbia", "type": "Abandoned Mine", "mineral": "Copper", "status": "Abandoned", "severity": "High", "issue": "Was worst point-source of copper pollution in Pacific Ocean; now remediated but legacy AMD", "source": "BC Ministry of Energy and Mines", "year_abandoned": 1974, "area_ha": 400},
    {"name": "Sydney Tar Ponds / Sysco", "lat": 46.14, "lon": -60.17, "country": "Canada", "state": "Nova Scotia", "type": "Abandoned Mine", "mineral": "Coal/Steel", "status": "Abandoned", "severity": "High", "issue": "Canada's worst contaminated site; PCBs, PAHs, heavy metals in estuary", "source": "ECCC Canada", "year_abandoned": 2001, "area_ha": 450},
    {"name": "Cobalt Silver Mining District", "lat": 47.40, "lon": -79.68, "country": "Canada", "state": "Ontario", "type": "Abandoned Mine", "mineral": "Silver/Cobalt/Arsenic", "status": "Abandoned", "severity": "Critical", "issue": "100+ mines; 1,000+ arsenic-laden tailings piles contaminating Lake Temiskaming", "source": "Ontario AML Inventory (5700+ sites)", "year_abandoned": 1989, "area_ha": 8000},
    {"name": "Thompson Nickel Belt", "lat": 55.74, "lon": -97.86, "country": "Canada", "state": "Manitoba", "type": "Active Mine", "mineral": "Nickel/Cobalt", "status": "Active", "severity": "Moderate", "issue": "SO2 emissions, tailings pond seepage into Burntwood River system", "source": "Manitoba Environment", "area_ha": 1200},
    {"name": "Springpole Gold Project (North Shore)", "lat": 51.08, "lon": -93.52, "country": "Canada", "state": "Ontario", "type": "Abandoned Mine", "mineral": "Gold", "status": "Abandoned", "severity": "Moderate", "issue": "Historical arsenic and cyanide contamination in First Nations territory", "source": "Ontario MOECP", "year_abandoned": 1940},

    # Mexico
    {"name": "Buenavista del Cobre Spill", "lat": 30.61, "lon": -109.89, "country": "Mexico", "state": "Sonora", "type": "Active Mine", "mineral": "Copper", "status": "Active", "severity": "Critical", "issue": "2014 acid spill — 40,000 m³ of sulfuric acid into Sonora River; 22,000 affected", "source": "SEMARNAT Mexico / Environmental Law Alliance Worldwide", "area_ha": 3500},
    {"name": "La Colorada Mercury Mine", "lat": 27.70, "lon": -108.50, "country": "Mexico", "state": "Chihuahua", "type": "Abandoned Mine", "mineral": "Mercury", "status": "Abandoned", "severity": "High", "issue": "Mercury contamination in soils and Urique River", "source": "INECC Mexico", "year_abandoned": 1975},

    # ===== SOUTH AMERICA =====
    # Brazil
    {"name": "Samarco/Vale Mariana Dam Collapse", "lat": -20.09, "lon": -43.52, "country": "Brazil", "state": "Minas Gerais", "type": "Active Mine", "mineral": "Iron Ore", "status": "Active", "severity": "Critical", "issue": "2015 dam collapse — 62M m³ tailings destroyed 663 km of Rio Doce; worst mining disaster in Brazil history", "source": "IBAMA / Nature (doi:10.1038/nature.2015.18723)", "area_ha": 800},
    {"name": "Brumadinho Dam Collapse (Vale)", "lat": -20.13, "lon": -44.12, "country": "Brazil", "state": "Minas Gerais", "type": "Abandoned Mine", "mineral": "Iron Ore", "status": "Abandoned", "severity": "Critical", "issue": "2019: 270 deaths; 11.7M m³ tailings destroyed Paraopeba River; UN declared environmental crime", "source": "IBAMA / Human Rights Watch 2019", "year_abandoned": 2019, "area_ha": 300},
    {"name": "Carajás Iron Ore Mine", "lat": -6.05, "lon": -50.17, "country": "Brazil", "state": "Pará", "type": "Active Mine", "mineral": "Iron Ore", "status": "Active", "severity": "Moderate", "issue": "World's largest iron ore mine; 7,000+ km² deforestation impact in Amazon; Indigenous lands threatened", "source": "Vale / IBAMA / Global Mining Watch", "area_ha": 114000},
    {"name": "Yanomami Illegal Gold Mining", "lat": 3.10, "lon": -63.50, "country": "Brazil", "state": "Roraima", "type": "Active Mine", "mineral": "Gold (Artisanal)", "status": "Active", "severity": "Critical", "issue": "20,000+ illegal garimpeiros; 30,000 Yanomami affected by mercury poisoning, malaria; 2023 humanitarian crisis declared", "source": "Hutukara Yanomami Association / FUNAI / Science 2022", "area_ha": 46000},

    # Peru
    {"name": "Cerro de Pasco Mine (La Oroya)", "lat": -10.68, "lon": -76.26, "country": "Peru", "state": "Pasco", "type": "Active Mine", "mineral": "Zinc/Lead/Silver/Copper", "status": "Active", "severity": "Critical", "issue": "La Oroya declared one of world's top 10 most polluted cities; children's blood lead 3× WHO limit", "source": "Blacksmith Institute / UNEP 2006 / Pure Earth", "area_ha": 2400},
    {"name": "Las Bambas Copper Mine", "lat": -14.03, "lon": -72.42, "country": "Peru", "state": "Apurímac", "type": "Active Mine", "mineral": "Copper/Silver/Gold", "status": "Active", "severity": "High", "issue": "Repeated community blockades; dust contamination; water source disputes with 8 indigenous communities", "source": "MMG Limited / Global Witness", "area_ha": 3500},
    {"name": "Espinar Copper Mining Zone", "lat": -14.79, "lon": -71.40, "country": "Peru", "state": "Cusco", "type": "Active Mine", "mineral": "Copper/Molybdenum", "status": "Active", "severity": "High", "issue": "Xstrata Tintaya; heavy metals in water above WHO limits; 2012 protests, 2 killed", "source": "CooperAcción / EJAtlas", "area_ha": 1800},
    {"name": "Quiruvilca Silver Mine", "lat": -8.00, "lon": -78.30, "country": "Peru", "state": "La Libertad", "type": "Abandoned Mine", "mineral": "Silver/Zinc/Lead", "status": "Abandoned", "severity": "High", "issue": "Acid drainage contaminating Santa River; 300,000 people downstream affected", "source": "Peruvian Ministry of Environment", "year_abandoned": 2005},

    # Chile
    {"name": "Chuquicamata Open Pit", "lat": -22.31, "lon": -68.91, "country": "Chile", "state": "Antofagasta", "type": "Active Mine", "mineral": "Copper/Molybdenum", "status": "Active", "severity": "Moderate", "issue": "Largest open-pit mine by excavated volume; SO2 emissions; former city relocated 2004", "source": "Codelco / SERNAGEOMIN", "area_ha": 4400},
    {"name": "El Teniente Underground/Surface", "lat": -34.09, "lon": -70.35, "country": "Chile", "state": "O'Higgins", "type": "Active Mine", "mineral": "Copper/Molybdenum", "status": "Active", "severity": "Moderate", "issue": "Tailings dam Quillayes covers >800 ha; SO2 acid rain impacts Cachapoal River", "source": "Codelco / CONAF Chile", "area_ha": 800},
    {"name": "Pascua-Lama Border Mine", "lat": -29.32, "lon": -70.02, "country": "Chile", "state": "Atacama", "type": "Abandoned Mine", "mineral": "Gold/Silver", "status": "Abandoned", "severity": "Critical", "issue": "Barrick Gold suspended 2013; glaciers damaged; cyanide risk to Huasco River; fined $16M", "source": "Barrick Gold / SMA Chile / EJAtlas", "year_abandoned": 2013, "area_ha": 5000},

    # Colombia
    {"name": "El Cerrejón Coal Mine", "lat": 11.12, "lon": -72.77, "country": "Colombia", "state": "La Guajira", "type": "Active Mine", "mineral": "Coal", "status": "Active", "severity": "High", "issue": "Largest open-pit coal mine in Latin America; Wayuu indigenous displacement; Ranchería River diversion proposed", "source": "Global Energy Monitor / HRW 2020", "area_ha": 69000},

    # Bolivia
    {"name": "Cerro Rico Potosí Silver Mine", "lat": -19.60, "lon": -65.75, "country": "Bolivia", "state": "Potosí", "type": "Active Mine", "mineral": "Silver/Zinc/Tin", "status": "Active", "severity": "High", "issue": "500+ years of mining; mountain at risk of collapse; 8M+ tonnes tailings contaminating Pilcomayo River", "source": "UNESCO WH List / UNEP / Pure Earth", "area_ha": 2000},

    # Argentina
    {"name": "Veladero Mine Cyanide Spill", "lat": -29.35, "lon": -70.05, "country": "Argentina", "state": "San Juan", "type": "Active Mine", "mineral": "Gold/Silver", "status": "Active", "severity": "Critical", "issue": "2015, 2016, 2017 repeated cyanide spills into Jáchal River; Barrick Gold fined; water for 60,000 affected", "source": "Barrick Gold / CONICET Argentina", "area_ha": 4200},

    # ===== AFRICA =====
    # South Africa — 6,000+ abandoned mines (DMRE inventory)
    {"name": "Witwatersrand Gold Mine District", "lat": -26.20, "lon": 27.90, "country": "South Africa", "state": "Gauteng", "type": "Abandoned Mine", "mineral": "Gold/Uranium", "status": "Abandoned", "severity": "Critical", "issue": "6,000+ gold mines; 270 km² uranium-contaminated tailings in Johannesburg area; acid mine drainage reaching water table", "source": "CSIR SA / DST / Council for Geoscience SA", "year_abandoned": 1990, "area_ha": 27000},
    {"name": "Moab Khotsong / Stilfontein Abandoned", "lat": -26.82, "lon": 26.78, "country": "South Africa", "state": "North West Province", "type": "Abandoned Mine", "mineral": "Gold", "status": "Abandoned", "severity": "High", "issue": "Flooded mines leaching radioactive AMD into Schoonspruit River; 200,000 people at risk", "source": "Council for Geoscience SA / Water SA Journal", "year_abandoned": 2005},
    {"name": "Wonderfonteinspruit Radioactive Catchment", "lat": -26.40, "lon": 27.40, "country": "South Africa", "state": "Gauteng", "type": "Abandoned Mine", "mineral": "Gold/Uranium", "status": "Abandoned", "severity": "Critical", "issue": "23+ km of river classified as radioactive hazard; uranium 40× WHO limit in sediments", "source": "NIWR / University of Johannesburg / Annals of Geophysics", "year_abandoned": 2002},
    {"name": "Grootvlei Mine AMD Decant", "lat": -26.30, "lon": 28.40, "country": "South Africa", "state": "Gauteng", "type": "Abandoned Mine", "mineral": "Gold", "status": "Abandoned", "severity": "Critical", "issue": "AMD decanting since 2002; contaminating Blesbokspruit Ramsar wetland; iron-rich orange water", "source": "DWS South Africa / IMWA 2016", "year_abandoned": 1997},
    {"name": "Zamzama Coal / Anglo American South Africa", "lat": -25.88, "lon": 27.83, "country": "South Africa", "state": "Mpumalanga", "type": "Active Mine", "mineral": "Coal", "status": "Active", "severity": "Moderate", "issue": "Mpumalanga highveld coal belt; SO2 emissions world's worst from a single region; water table contamination", "source": "Centre for Environmental Rights SA / Global Energy Monitor", "area_ha": 12000},
    {"name": "Cullinan Diamond Mine", "lat": -25.67, "lon": 28.52, "country": "South Africa", "state": "Gauteng", "type": "Active Mine", "mineral": "Diamond", "status": "Active", "severity": "Low", "issue": "Active kimberlite pipe; 1+ km deep open pit; historical waste rock piles", "source": "Petra Diamonds / DMRE SA", "area_ha": 250},

    # Ghana
    {"name": "Obuasi Gold Mine (AngloGold Ashanti)", "lat": 6.21, "lon": -1.67, "country": "Ghana", "state": "Ashanti", "type": "Active Mine", "mineral": "Gold", "status": "Active", "severity": "High", "issue": "Mercury and arsenic contamination of Obuasi River; illegal small-scale galamsey mining compounds problem", "source": "AngloGold Ashanti / Ghana EPA / EJAtlas", "area_ha": 3200},
    {"name": "Tarkwa Newmont/Gold Fields", "lat": 5.30, "lon": -2.00, "country": "Ghana", "state": "Western", "type": "Active Mine", "mineral": "Gold", "status": "Active", "severity": "High", "issue": "Cyanide heap leach; Bonsa River contamination; 30,000+ displaced from communities", "source": "Newmont / Ghana EPA", "area_ha": 5600},
    {"name": "Kumasi Artisanal Mining (Galamsey)", "lat": 6.70, "lon": -1.60, "country": "Ghana", "state": "Ashanti", "type": "Active Mine", "mineral": "Gold (Artisanal)", "status": "Active", "severity": "Critical", "issue": "Mercury contamination of rivers feeding Pra and Ankobra basins; 40% of Ghana's rivers contaminated per 2017 Geological Survey", "source": "Minerals Commission Ghana / Nature Sustainability 2021"},

    # DR Congo
    {"name": "Katanga Copper Belt (Lubumbashi)", "lat": -11.66, "lon": 27.47, "country": "DR Congo", "state": "Katanga", "type": "Active Mine", "mineral": "Copper/Cobalt", "status": "Active", "severity": "Critical", "issue": "World's largest cobalt reserves mined with artisanal labour; child labour crisis; SO2 kills vegetation for 70 km", "source": "IPIS / Amnesty International 2016 / Journal of Cleaner Production", "area_ha": 45000},
    {"name": "Kolwezi Cobalt Artisanal Mines", "lat": -10.72, "lon": 25.46, "country": "DR Congo", "state": "Katanga", "type": "Active Mine", "mineral": "Cobalt/Copper", "status": "Active", "severity": "Critical", "issue": "40,000+ artisanal miners including children; cobalt dust lung disease; contaminated tailings near settlements", "source": "IPIS / Amnesty International / USGS REE Statistics", "area_ha": 12000},
    {"name": "Bisie Cassiterite Mine", "lat": -0.73, "lon": 27.50, "country": "DR Congo", "state": "North Kivu", "type": "Active Mine", "mineral": "Tin/Cassiterite", "status": "Active", "severity": "High", "issue": "Conflict mineral zone; forest destruction; mercury use in processing; no environmental controls", "source": "Global Witness / IPIS", "area_ha": 3000},

    # Zambia
    {"name": "Copperbelt Zambia (Nkana/Nchanga)", "lat": -12.82, "lon": 28.22, "country": "Zambia", "state": "Copperbelt", "type": "Active Mine", "mineral": "Copper/Cobalt", "status": "Active", "severity": "High", "issue": "SO2 pollution; slag heap contamination of Kafue River; Vedanta Nchanga spill 2006 killed fish over 100 km", "source": "Zambia EPA / EJAtlas / ScienceDirect", "area_ha": 18000},

    # Zimbabwe
    {"name": "Great Dyke Chrome/Platinum Mining", "lat": -19.00, "lon": 30.00, "country": "Zimbabwe", "state": "Mashonaland", "type": "Active Mine", "mineral": "Chrome/Platinum/Gold", "status": "Active", "severity": "High", "issue": "Artisanal and commercial mining; acid drainage into Mazowe River; dust impacts on communities", "source": "Zimbabwe EPA / UNEP Artisanal Mining Report", "area_ha": 25000},

    # Nigeria
    {"name": "Zamfara State Gold (Lead Poisoning)", "lat": 12.17, "lon": 6.66, "country": "Nigeria", "state": "Zamfara", "type": "Active Mine", "mineral": "Gold (Artisanal)", "status": "Active", "severity": "Critical", "issue": "2010 mass lead poisoning — 400+ children died; worst acute lead poisoning disaster in recent history per MSF", "source": "MSF / WHO / PLoS Medicine 2012", "area_ha": 5000},

    # Tanzania
    {"name": "Geita Gold Mine", "lat": -2.87, "lon": 32.18, "country": "Tanzania", "state": "Geita", "type": "Active Mine", "mineral": "Gold", "status": "Active", "severity": "Moderate", "issue": "AngloGold Ashanti open pit; cyanide tailings dam near Lake Victoria; fishing community displacement", "source": "AngloGold Ashanti / EJAtlas Tanzania"},

    # Mali
    {"name": "Syama Gold Mine", "lat": 10.62, "lon": -7.96, "country": "Mali", "state": "Sikasso", "type": "Active Mine", "mineral": "Gold", "status": "Active", "severity": "Moderate", "issue": "Tailings pond seepage; sulfur dust; artisanal mercury use in surrounding villages", "source": "Resolute Mining / DNEF Mali"},

    # Burkina Faso
    {"name": "Essakane Gold Mine", "lat": 14.78, "lon": -0.97, "country": "Burkina Faso", "state": "Sahel", "type": "Active Mine", "mineral": "Gold", "status": "Active", "severity": "Moderate", "issue": "Iamgold mine; artisanal mercury mining adjacent site; dust impacts Sahelian communities", "source": "Iamgold / Burkina Faso BUNEE", "area_ha": 3000},

    # Morocco
    {"name": "Jerrada Coal Mining (Abandoned)", "lat": 34.68, "lon": -2.02, "country": "Morocco", "state": "Oriental", "type": "Abandoned Mine", "mineral": "Coal", "status": "Abandoned", "severity": "High", "issue": "300+ illegal coal miners worked in 2018; 2 miners drowned; methane explosions; collapse risk", "source": "ONHYM Morocco / Reuters 2018", "year_abandoned": 2000, "area_ha": 1500},
    {"name": "Khouribga Phosphate Mines", "lat": 32.88, "lon": -6.89, "country": "Morocco", "state": "Khouribga", "type": "Active Mine", "mineral": "Phosphate", "status": "Active", "severity": "Moderate", "issue": "OCP world's largest phosphate exporter; waste slurry contamination of Oum Er-Rbia River; radiation from uranium in phosphate", "source": "OCP Group / World Bank Phosphate Report", "area_ha": 10000},

    # ===== EUROPE =====
    # Romania
    {"name": "Rosia Montana Gold Mine", "lat": 46.37, "lon": 23.10, "country": "Romania", "state": "Alba", "type": "Abandoned Mine", "mineral": "Gold/Silver", "status": "Abandoned", "severity": "High", "issue": "2000 Baia Mare cyanide spill (from affiliated plant) killed 1,200 tonnes of fish across Hungary/Yugoslavia; UNESCO heritage conflict", "source": "UNEP Baia Mare Task Force Report 2000 / EJAtlas", "year_abandoned": 2006, "area_ha": 3000},
    {"name": "Baia Mare Tailings Spill Site", "lat": 47.66, "lon": -23.57, "country": "Romania", "state": "Maramureș", "type": "Abandoned Mine", "mineral": "Gold/Silver", "status": "Abandoned", "severity": "Critical", "issue": "January 2000: 100,000 m³ cyanide released into Somes/Tisza/Danube; worst environmental disaster in Europe post-Chernobyl", "source": "UNEP OCHA Report 2000", "year_abandoned": 2000, "area_ha": 200},

    # Spain
    {"name": "Aznalcóllar Mine (Boliden)", "lat": 37.52, "lon": -6.27, "country": "Spain", "state": "Andalusia", "type": "Abandoned Mine", "mineral": "Zinc/Lead/Copper", "status": "Abandoned", "severity": "Critical", "issue": "1998 tailings dam collapse released 5M m³ into Doñana National Park buffer zone; Europe's worst mining spill", "source": "Spanish Ministry of Environment / Nature 1999", "year_abandoned": 1998, "area_ha": 4000},
    {"name": "Riotinto Mine (Historical)", "lat": 37.68, "lon": -6.58, "country": "Spain", "state": "Huelva", "type": "Abandoned Mine", "mineral": "Copper/Iron/Gold", "status": "Abandoned", "severity": "High", "issue": "5,000 years of mining; river runs red with iron sulfate (pH 2); acid river analogue for Mars", "source": "CSIC Spain / Astrobiology Journal", "year_abandoned": 2001, "area_ha": 5500},

    # United Kingdom
    {"name": "Parys Mountain Copper Mine", "lat": 53.40, "lon": -4.36, "country": "United Kingdom", "state": "Wales", "type": "Abandoned Mine", "mineral": "Copper/Zinc/Lead", "status": "Abandoned", "severity": "High", "issue": "18th century copper boom; acid drainage has eliminated aquatic life from 3 km of Afon Goch river", "source": "Environment Agency Wales / BGS", "year_abandoned": 1904, "area_ha": 375},
    {"name": "Wheal Jane Tin Mine", "lat": 50.24, "lon": -5.10, "country": "United Kingdom", "state": "Cornwall", "type": "Abandoned Mine", "mineral": "Tin/Zinc/Copper", "status": "Abandoned", "severity": "High", "issue": "1992 mine water discharge turned Fal Estuary orange; ongoing AMD treatment plant required", "source": "Environment Agency UK / BGS Cornwall", "year_abandoned": 1991, "area_ha": 500},

    # Germany
    {"name": "Lausitz Lignite / Brown Coal", "lat": 51.78, "lon": 14.50, "country": "Germany", "state": "Lusatia/Brandenburg", "type": "Active Mine", "mineral": "Lignite Coal", "status": "Active", "severity": "Moderate", "issue": "Europe's largest open-pit lignite mines; CO2 emissions; subsidence; villages relocated; groundwater acidification", "source": "LMBV / German Coal Commission 2019 / Global Energy Monitor", "area_ha": 13000},

    # Ukraine
    {"name": "Donbas Coal Mining Region", "lat": 48.00, "lon": 38.00, "country": "Ukraine", "state": "Donetsk/Luhansk", "type": "Abandoned Mine", "mineral": "Coal", "status": "Abandoned", "severity": "Critical", "issue": "150+ flooded mine shafts post-2014 conflict; mine water rising with radioactive brine, oil, methane; 3M people at risk", "source": "OSCE / UNICEF 2020 / Nature Water 2022", "year_abandoned": 2014, "area_ha": 35000},

    # Poland
    {"name": "Silesian Coal Mining Region", "lat": 50.30, "lon": 19.00, "country": "Poland", "state": "Silesia", "type": "Active Mine", "mineral": "Hard Coal", "status": "Active", "severity": "High", "issue": "Europe's largest coal mining district; subsidence damaging 75,000+ buildings; saline AMD into Vistula River", "source": "GIG Poland / Global Energy Monitor / Polish EPA", "area_ha": 25000},

    # ===== RUSSIA =====
    {"name": "Norilsk Nickel Mining Complex", "lat": 69.34, "lon": 88.20, "country": "Russia", "state": "Krasnoyarsk", "type": "Active Mine", "mineral": "Nickel/Copper/Palladium", "status": "Active", "severity": "Critical", "issue": "World's largest heavy metal air pollution; 500 km² dead forests; 2020 diesel spill 21,000 tonnes to Ambarnaya River", "source": "NORNICKEL / Greenpeace Russia / Science 2021", "area_ha": 60000},
    {"name": "Kovdor Rare Metal / Iron Mine", "lat": 67.57, "lon": 30.47, "country": "Russia", "state": "Murmansk", "type": "Active Mine", "mineral": "Iron/Apatite/Baddeleyite", "status": "Active", "severity": "Moderate", "issue": "Tailings impoundment threatens Kovdozero lake system; phosphorus runoff", "source": "Eurochem / Russian Federal Environment Agency"},
    {"name": "Kumtor Gold Mine (Kyrgyzstan)", "lat": 41.87, "lon": 78.20, "country": "Kyrgyzstan", "state": "Issyk-Kul", "type": "Active Mine", "mineral": "Gold", "status": "Active", "severity": "Critical", "issue": "Centerra Gold; 2002 cyanide spill killed Barskoon River; glacier under crust; tailings above Kumtor River at 4,000m altitude", "source": "Centerra Gold / UNEP / EJAtlas Kyrgyzstan", "area_ha": 5000},

    # ===== CENTRAL ASIA =====
    {"name": "Mailuu-Suu Uranium Tailings (Kyrgyzstan)", "lat": 41.27, "lon": 72.47, "country": "Kyrgyzstan", "state": "Jalal-Abad", "type": "Abandoned Mine", "mineral": "Uranium", "status": "Abandoned", "severity": "Critical", "issue": "Soviet-era 36 tailings piles & 13 waste dumps; landslides threaten Ala-Buka River; IAEA priority site", "source": "IAEA TACIS / NATO SPS 2006 / UNECE", "year_abandoned": 1968, "area_ha": 200},
    {"name": "Khaidarkan Mercury Mine", "lat": 39.94, "lon": 71.37, "country": "Kyrgyzstan", "state": "Batken", "type": "Active Mine", "mineral": "Mercury/Antimony", "status": "Active", "severity": "High", "issue": "World's second-largest mercury mine; Isfara River contamination shared with Tajikistan", "source": "UNEP Global Mercury Assessment 2018", "area_ha": 500},
    {"name": "Charkesar Uranium Tailings (Uzbekistan)", "lat": 41.00, "lon": 69.70, "country": "Uzbekistan", "state": "Tashkent", "type": "Abandoned Mine", "mineral": "Uranium", "status": "Abandoned", "severity": "High", "issue": "Radioactive tailings near Chirchiq River; 1.3M people downstream in Tashkent at risk", "source": "IAEA / UNECE / Nuclear Engineering International", "year_abandoned": 1970},

    # ===== MIDDLE EAST =====
    {"name": "Oman Copper Mining (Al Suwaiq)", "lat": 23.84, "lon": 57.40, "country": "Oman", "state": "Al Batinah", "type": "Abandoned Mine", "mineral": "Copper", "status": "Abandoned", "severity": "Moderate", "issue": "Ancient and colonial copper mines; acid drainage into wadis; UNESCO heritage site at risk", "source": "Oman Ministry of Energy and Minerals / UNESCO", "year_abandoned": 1994},
    {"name": "Saudi Arabia Mahad Adh Dhahab Gold", "lat": 23.50, "lon": 40.86, "country": "Saudi Arabia", "state": "Al Madinah", "type": "Active Mine", "mineral": "Gold/Silver", "status": "Active", "severity": "Moderate", "issue": "Ma'aden gold mine; tailings impoundment in arid zone; mercury in artisanal adjacent areas", "source": "Ma'aden / Saudi Geological Survey", "area_ha": 2000},
    {"name": "Iran Miduk Copper Mine", "lat": 30.48, "lon": 55.30, "country": "Iran", "state": "Kerman", "type": "Active Mine", "mineral": "Copper", "status": "Active", "severity": "Moderate", "issue": "Tailings dam near Shur River; copper and molybdenum seepage; dust on rural communities", "source": "NICICO Iran / Iran Journal of Environmental Health", "area_ha": 3000},

    # ===== SOUTH & SOUTHEAST ASIA =====
    # India — extensive coal and iron ore mining belt
    {"name": "Jharia Coal Mine Fire (Jharkhand)", "lat": 23.75, "lon": 86.42, "country": "India", "state": "Jharkhand", "type": "Active Mine", "mineral": "Coal", "status": "Active", "severity": "Critical", "issue": "Underground fires burning since 1916; 70+ km² subsidence zone; 40,000+ families displaced; continuous methane/CO emissions", "source": "BCCL / GSI / Environmental Science & Policy 2013", "area_ha": 7000},
    {"name": "Bellary Iron Ore Mines", "lat": 15.15, "lon": 76.92, "country": "India", "state": "Karnataka", "type": "Abandoned Mine", "mineral": "Iron Ore", "status": "Abandoned", "severity": "High", "issue": "Illegal mining caused 150+ deaths (pit collapses); Supreme Court halted 2011; red dust contaminating 50 km radius", "source": "CBI India / Supreme Court Karnataka Mining Judgment 2011", "year_abandoned": 2011, "area_ha": 6000},
    {"name": "Jadugoda Uranium Mine", "lat": 22.65, "lon": 86.35, "country": "India", "state": "Jharkhand", "type": "Active Mine", "mineral": "Uranium", "status": "Active", "severity": "High", "issue": "Tailings pond leaches radium/thorium into Subarnarekha River; elevated cancer rates in tribal villages per XCCD/PRISM studies", "source": "UCIL India / PRISM India / EPW 2007", "area_ha": 200},
    {"name": "Meghalaya Rat-Hole Coal Mining", "lat": 25.50, "lon": 92.00, "country": "India", "state": "Meghalaya", "type": "Abandoned Mine", "mineral": "Coal", "status": "Abandoned", "severity": "Critical", "issue": "NGT banned 2014; acid mine drainage destroyed Lukha and Kopili rivers; 2018 mine flooded trapping 15 miners", "source": "NGT India / NEERI / Indian Journal of Environmental Protection", "year_abandoned": 2014, "area_ha": 25000},
    {"name": "Singrauli Coal / Power Complex", "lat": 24.20, "lon": 82.65, "country": "India", "state": "Madhya Pradesh/UP", "type": "Active Mine", "mineral": "Coal", "status": "Active", "severity": "Critical", "issue": "500,000 people displaced over decades; fly ash mercury contamination of Rihand reservoir; WHO ranked worst air quality", "source": "CPCB India / Down to Earth 2014 / Blacksmith Institute", "area_ha": 30000},

    # Indonesia
    {"name": "Grasberg Mine (Freeport)", "lat": -4.05, "lon": 137.10, "country": "Indonesia", "state": "Papua", "type": "Active Mine", "mineral": "Copper/Gold", "status": "Active", "severity": "Critical", "issue": "World's largest gold mine; 200,000+ tonnes tailings/day into Ajkwa River; 230 km² lowland forests buried under tailings", "source": "Freeport-McMoRan / Science 2006 / EJAtlas", "area_ha": 23000},
    {"name": "Kaltim Prima Coal (Sangatta)", "lat": -0.50, "lon": 117.50, "country": "Indonesia", "state": "East Kalimantan", "type": "Active Mine", "mineral": "Coal", "status": "Active", "severity": "High", "issue": "Largest coal mine in Indonesia; deforestation 100+ km²; coal pits become acidic lakes after abandonment", "source": "KPC / Indonesian Ministry of Energy / Global Energy Monitor", "area_ha": 90000},
    {"name": "Bangka Island Tin Mining", "lat": -2.15, "lon": 106.13, "country": "Indonesia", "state": "Bangka-Belitung", "type": "Active Mine", "mineral": "Tin", "status": "Active", "severity": "High", "issue": "Offshore sea mining destroys coral; illegal mining 60% production; 700+ illegal pits on land destroying rainforest", "source": "Bangka-Belitung Government / Bangka Environmental Monitor", "area_ha": 15000},

    # Philippines
    {"name": "Marinduque Marcopper Mine Spill", "lat": 13.37, "lon": 121.93, "country": "Philippines", "state": "Marinduque", "type": "Abandoned Mine", "mineral": "Copper", "status": "Abandoned", "severity": "Critical", "issue": "1996: 1.6M m³ copper tailings into Boac River; river declared dead; Placer Dome never fully remediated", "source": "Placer Dome / DENR Philippines / EJAtlas", "year_abandoned": 1996, "area_ha": 400},
    {"name": "Tampakan Copper/Gold (South Cotabato)", "lat": 6.38, "lon": 124.72, "country": "Philippines", "state": "South Cotabato", "type": "Active Mine", "mineral": "Copper/Gold", "status": "Active", "severity": "High", "issue": "Southeast Asia's largest undeveloped copper deposit; B'laan indigenous opposition; open-pit law blocked 2010", "source": "Sagittarius Mines / EJAtlas Philippines"},

    # Papua New Guinea
    {"name": "Ok Tedi Mine", "lat": -5.22, "lon": 141.10, "country": "Papua New Guinea", "state": "Western Province", "type": "Active Mine", "mineral": "Copper/Gold", "status": "Active", "severity": "Critical", "issue": "Tailings dumped directly into Ok Tedi/Fly River system; 2,000 km² floodplain contaminated; 50,000 people affected; Australian court settlement 1996", "source": "Ok Tedi Mining / CSIRO / Nature 2001 / EJAtlas", "area_ha": 45000},
    {"name": "Panguna Mine (Bougainville)", "lat": -6.32, "lon": 155.39, "country": "Papua New Guinea", "state": "Autonomous Bougainville", "type": "Abandoned Mine", "mineral": "Copper/Gold", "status": "Abandoned", "severity": "Critical", "issue": "Rio Tinto; 1989 closure after armed conflict (Bougainville Crisis); 1 billion+ tonnes uncontained waste; Jaba River devastated", "source": "Rio Tinto / Global Witness / EJAtlas Bougainville", "year_abandoned": 1989, "area_ha": 16000},

    # Mongolia
    {"name": "Oyu Tolgoi Copper/Gold (Mongolia)", "lat": 43.01, "lon": 106.86, "country": "Mongolia", "state": "Ömnögovi", "type": "Active Mine", "mineral": "Copper/Gold/Silver", "status": "Active", "severity": "High", "issue": "Rio Tinto/Turquoise Hill; groundwater depletion in Gobi Desert; Khanbogd community water insecurity", "source": "Rio Tinto / Mongolian Ministry of Environment / WWF Mongolia", "area_ha": 5000},

    # Kazakhstan
    {"name": "Balkhash Copper Smelter / Mine", "lat": 46.84, "lon": 74.99, "country": "Kazakhstan", "state": "Karaganda", "type": "Active Mine", "mineral": "Copper", "status": "Active", "severity": "High", "issue": "SO2 emissions; Lake Balkhash metal contamination; slag dumps 20+ km²", "source": "Kazakhmys / Kazakhstan MNE / UNEP", "area_ha": 5000},
    {"name": "Semey (Semipalatinsk) Nuclear/Uranium Zone", "lat": 50.41, "lon": 80.25, "country": "Kazakhstan", "state": "East Kazakhstan", "type": "Abandoned Mine", "mineral": "Uranium", "status": "Abandoned", "severity": "Critical", "issue": "Soviet nuclear test polygon; uranium mines; 1.5M people irradiated; birth defects continue; 34 km² radioactive", "source": "IAEA / Kazakhstan Nuclear Physics Inst. / WHO 2000", "year_abandoned": 1991, "area_ha": 180000},

    # ===== EAST ASIA =====
    # China — World's largest mining nation
    {"name": "Fushun Open-Pit Coal Mine", "lat": 41.86, "lon": 123.88, "country": "China", "state": "Liaoning", "type": "Abandoned Mine", "mineral": "Coal/Oil Shale", "status": "Abandoned", "severity": "High", "issue": "World's largest open-pit coal mine 1901–2019; 6.6 km long pit; 200+ km² subsidence zone; methane emissions", "source": "China Coal Research Institute / Global Energy Monitor", "year_abandoned": 2019, "area_ha": 66000},
    {"name": "Panzhihua Iron/Vanadium/Titanium", "lat": 26.58, "lon": 101.72, "country": "China", "state": "Sichuan", "type": "Active Mine", "mineral": "Iron/Vanadium/Titanium", "status": "Active", "severity": "High", "issue": "Tailings dam failures; vanadium pentoxide dust; 2019 tailings leak into Jinsha River cut off drinking water for 100,000", "source": "PANGANG Group / MWR China / Xinhua 2019", "area_ha": 8000},
    {"name": "Daye Copper Mine (Hubei)", "lat": 30.10, "lon": 114.98, "country": "China", "state": "Hubei", "type": "Abandoned Mine", "mineral": "Copper/Iron", "status": "Abandoned", "severity": "High", "issue": "2,000 years of mining history; arsenic/cadmium contamination of Yangtze River tributaries; abandoned open pit lake", "source": "Daye Nonferrous Metals / Chinese Journal of Environmental Science", "year_abandoned": 1995, "area_ha": 3000},
    {"name": "Huize Lead/Zinc Mine (Yunnan)", "lat": 26.41, "lon": 103.28, "country": "China", "state": "Yunnan", "type": "Active Mine", "mineral": "Lead/Zinc/Silver", "status": "Active", "severity": "High", "issue": "Tailings dam failures; lead poisoning of children in Qujing county; Nanpan River contamination", "source": "Yunnan Environmental Protection Bureau / China Daily 2011"},
    {"name": "Tongling Copper Smelter/Mine", "lat": 30.95, "lon": 117.81, "country": "China", "state": "Anhui", "type": "Active Mine", "mineral": "Copper", "status": "Active", "severity": "High", "issue": "Sulphur dioxide pollution; tailings contaminating Yangtze; cadmium/arsenic in soils over 50 km radius", "source": "Tongling Nonferrous Metals / CNEMC China"},

    # Australia — 50,000–80,000+ abandoned mine features (DEIS 2002 estimate)
    {"name": "Rum Jungle Uranium/Copper (NT)", "lat": -12.97, "lon": 130.99, "country": "Australia", "state": "Northern Territory", "type": "Abandoned Mine", "mineral": "Uranium/Copper", "status": "Abandoned", "severity": "Critical", "issue": "Australia's first uranium mine; acid drainage destroying Finniss River; first major AML remediation project", "source": "Geoscience Australia / NT Government AML Inventory", "year_abandoned": 1971, "area_ha": 600},
    {"name": "Mount Morgan Mine (Queensland)", "lat": -23.64, "lon": 150.39, "country": "Australia", "state": "Queensland", "type": "Abandoned Mine", "mineral": "Gold/Copper", "status": "Abandoned", "severity": "Critical", "issue": "600M tonnes of acid-generating waste; continuous AMD discharge into Dee River; >100 years of pollution legacy", "source": "Queensland DEE / AML Assessment QLD 2015", "year_abandoned": 1981, "area_ha": 900},
    {"name": "Broken Hill Mining District", "lat": -31.95, "lon": 141.47, "country": "Australia", "state": "New South Wales", "type": "Active Mine", "mineral": "Silver/Lead/Zinc", "status": "Active", "severity": "High", "issue": "130 years of mining; elevated blood lead in residents; 40 km² slag heaps; dust events affecting city", "source": "NSW EPA / National Lead Taskforce Australia", "area_ha": 12000},
    {"name": "Olympic Dam (BHP Billiton)", "lat": -30.44, "lon": 136.88, "country": "Australia", "state": "South Australia", "type": "Active Mine", "mineral": "Copper/Uranium/Gold/Silver", "status": "Active", "severity": "Moderate", "issue": "World's largest uranium deposit; 10M+ tonnes/year tailings; radioactive dust management; expansion debate", "source": "BHP / SA EPA / ARPANSA", "area_ha": 3300},
    {"name": "Ravenswood Gold Mine (QLD)", "lat": -20.10, "lon": 146.90, "country": "Australia", "state": "Queensland", "type": "Abandoned Mine", "mineral": "Gold", "status": "Abandoned", "severity": "Moderate", "issue": "Cyanide tailings; arsenic in soils; contamination of local aquifer used for cattle", "source": "QLD DNRME AML Register", "year_abandoned": 2005},
    {"name": "King Island Scheelite Mine", "lat": -39.93, "lon": 144.00, "country": "Australia", "state": "Tasmania", "type": "Abandoned Mine", "mineral": "Tungsten", "status": "Abandoned", "severity": "Moderate", "issue": "Abandoned tailings leaching fluoride; acidic seepage into local streams", "source": "Tasmanian EPA / AML Register", "year_abandoned": 1992},
]

RARE_EARTH_MINES = [
    # ===== CHINA — ~70% of global REE production =====
    {"name": "Bayan Obo REE-Iron Mine", "lat": 41.80, "lon": 109.97, "country": "China", "state": "Inner Mongolia", "type": "Rare Earth Mine", "mineral": "REE/Niobium/Iron", "status": "Active", "severity": "Critical", "issue": "World's largest REE deposit; 80+ km² radioactive tailings pond leaching thorium/fluoride into Yellow River basin; 10 km² \"black lake\" visible from satellite", "source": "USGS REE Statistics 2023 / Bayan Obo Research Consortium / Science of Total Environment 2017", "production_tpa": 60000, "reserves_mt": 800},
    {"name": "Jiangxi In-Situ Leach REE Mines", "lat": 26.00, "lon": 115.50, "country": "China", "state": "Jiangxi", "type": "Rare Earth Mine", "mineral": "Heavy REE (HREE)", "status": "Active", "severity": "Critical", "issue": "Ammonium sulfate in-situ leaching; 98% of world's HREE; groundwater ammonia contamination; 100+ km² barren hillsides; 2,000+ km² affected per Chinese Academy of Sciences 2012", "source": "USGS REE Statistics / Chinese Academy of Sciences / Earth.org REE Review 2021", "production_tpa": 10000},
    {"name": "Maoniuping REE Mine (Mianning)", "lat": 28.56, "lon": 102.16, "country": "China", "state": "Sichuan", "type": "Rare Earth Mine", "mineral": "REE/Fluorite", "status": "Active", "severity": "High", "issue": "Bastnäsite ore processing; fluoride contamination of Min River tributaries; radioactive waste from thorium byproduct", "source": "USGS / ScienceDirect / CNKI Chinese geology papers", "production_tpa": 15000, "reserves_mt": 1.5},
    {"name": "Dalucao REE Mine", "lat": 28.20, "lon": 102.30, "country": "China", "state": "Sichuan", "type": "Rare Earth Mine", "mineral": "REE/Fluorite", "status": "Active", "severity": "High", "issue": "Shenghe Resources; flotation tailings dam >2 km²; radium and fluoride in surface water", "source": "Shenghe Resources / ScienceDirect 2020", "production_tpa": 8000},
    {"name": "Weishan REE Deposit", "lat": 25.31, "lon": 100.31, "country": "China", "state": "Yunnan", "type": "Rare Earth Mine", "mineral": "REE/Bastnäsite", "status": "Active", "severity": "Moderate", "issue": "Acid leachate into Mekong River headwaters; fluoride risk to downstream Cambodia, Laos, Thailand", "source": "USGS / Yunnan Institute of Environmental Science"},
    {"name": "Zibo REE Processing Hub", "lat": 36.81, "lon": 118.05, "country": "China", "state": "Shandong", "type": "Rare Earth Mine", "mineral": "REE Processing", "status": "Active", "severity": "Moderate", "issue": "Solvent extraction; ammonium sulfate discharge; air fluoride emissions affecting 5+ townships", "source": "CNKI / Shandong EPA Reports"},

    # ===== USA =====
    {"name": "Mountain Pass REE Mine", "lat": 35.48, "lon": -115.53, "country": "United States", "state": "California", "type": "Rare Earth Mine", "mineral": "REE/Bastnäsite", "status": "Active", "severity": "Moderate", "issue": "Only US operating REE mine (MP Materials); 1998 radioactive wastewater spills into Mojave Desert; tailings pond management ongoing", "source": "MP Materials / USGS REE Statistics / EPA California 2002", "production_tpa": 42000, "reserves_mt": 1.5},
    {"name": "Bear Lodge REE Project (WY)", "lat": 44.65, "lon": -104.27, "country": "United States", "state": "Wyoming", "type": "Rare Earth Mine", "mineral": "REE/Carbonatite", "status": "Active", "severity": "Low", "issue": "Permitting stage; potential groundwater impacts to Belle Fourche River; tribal heritage concerns (Lakota)", "source": "Rare Element Resources / USGS", "reserves_mt": 18.2},
    {"name": "Round Top Lithium-REE Project (TX)", "lat": 31.15, "lon": -104.78, "country": "United States", "state": "Texas", "type": "Rare Earth Mine", "mineral": "REE/Lithium/Uranium", "status": "Active", "severity": "Low", "issue": "USA Rare Earth project; rhyolite deposit with co-occurring uranium; water use in arid Chihuahuan Desert", "source": "USA Rare Earth / USGS REE Statistics"},
    {"name": "Pea Ridge Iron-REE Mine (MO)", "lat": 38.00, "lon": -91.10, "country": "United States", "state": "Missouri", "type": "Abandoned Mine", "mineral": "Iron/REE", "status": "Abandoned", "severity": "Low", "issue": "Secondary REE deposit; historical iron production; underground mine abandoned 2001; AMD monitoring required", "source": "USGS MRDS / Missouri Geological Survey", "year_abandoned": 2001},

    # ===== AUSTRALIA =====
    {"name": "Mount Weld REE Mine (Lynas)", "lat": -28.69, "lon": 122.00, "country": "Australia", "state": "Western Australia", "type": "Rare Earth Mine", "mineral": "REE/Carbonatite", "status": "Active", "severity": "Moderate", "issue": "World's highest grade REE deposit; ore shipped to Malaysia LAMP facility for processing; radioactive thorium waste management concerns", "source": "Lynas Rare Earths / ARPANSA / Greenpeace Australia", "production_tpa": 14000, "reserves_mt": 1.8},
    {"name": "Dubbo Polymetallic REE (NSW)", "lat": -32.22, "lon": 148.67, "country": "Australia", "state": "New South Wales", "type": "Rare Earth Mine", "mineral": "REE/Zirconium/Hafnium/Niobium", "status": "Active", "severity": "Low", "issue": "Australian Strategic Materials project; tailings management in dry alkaline conditions; riverine contamination risk", "source": "ASM Ltd / NSW EPA", "reserves_mt": 73.6},
    {"name": "Nolans Bore REE (NT)", "lat": -23.08, "lon": 133.27, "country": "Australia", "state": "Northern Territory", "type": "Rare Earth Mine", "mineral": "REE/Phosphate/Uranium", "status": "Active", "severity": "Moderate", "issue": "Arafura Resources; uranium co-occurrence requires complex waste management; arid zone water usage", "source": "Arafura Resources / NT EPA / USGS", "reserves_mt": 56},

    # ===== INDIA =====
    {"name": "Chavara REE/Monazite Placer (Kerala)", "lat": 9.00, "lon": 76.58, "country": "India", "state": "Kerala", "type": "Rare Earth Mine", "mineral": "REE/Monazite/Ilmenite", "status": "Active", "severity": "High", "issue": "Thorium-rich monazite sands; elevated background radiation (3× normal); Kerala Minerals and Metals Ltd; fishing communities radiation exposure", "source": "IREL India / BARC / Radiation Protection Dosimetry Journal", "production_tpa": 4000},
    {"name": "Manavalakurichi Monazite (Tamil Nadu)", "lat": 8.15, "lon": 77.31, "country": "India", "state": "Tamil Nadu", "type": "Rare Earth Mine", "mineral": "REE/Monazite/Thorium", "status": "Active", "severity": "High", "issue": "Beach sand mining; radioactive monazite tailings; elevated thoron in air near processing plant", "source": "IREL India / AERB / Current Science Journal India 2006"},
    {"name": "Odisha REE Carbonatite (Sung Valley area)", "lat": 25.20, "lon": 91.52, "country": "India", "state": "Meghalaya", "type": "Rare Earth Mine", "mineral": "REE/Carbonatite", "status": "Active", "severity": "Low", "issue": "Exploration stage; tribal land concerns in Garo Hills; acid dissolution risk in high-rainfall area", "source": "GSI India / USGS REE Prospects Report"},

    # ===== MYANMAR/BURMA =====
    {"name": "Kachin REE Ion-Adsorption Mines", "lat": 25.80, "lon": 98.50, "country": "Myanmar", "state": "Kachin", "type": "Rare Earth Mine", "mineral": "HREE (ion-adsorption)", "status": "Active", "severity": "Critical", "issue": "Illegal Chinese-funded operations; ammonium sulfate leaching; deforestation 50,000+ acres; river contamination; no environmental controls; armed group taxation", "source": "Global Witness 2023 / Yale Environment 360 / EJAtlas Myanmar", "production_tpa": 26000},
    {"name": "Shan State REE Mining Zone", "lat": 21.50, "lon": 98.00, "country": "Myanmar", "state": "Shan", "type": "Rare Earth Mine", "mineral": "HREE", "status": "Active", "severity": "Critical", "issue": "Cross-border illegal supply to China; Salween River contamination risk; conflict zone resource extraction", "source": "Global Witness / Stimson Center", "production_tpa": 5000},

    # ===== LAOS =====
    {"name": "Laos REE Mining Areas (Nam Ngiep)", "lat": 18.80, "lon": 103.50, "country": "Laos", "state": "Bolikhamxay", "type": "Rare Earth Mine", "mineral": "REE/Gold", "status": "Active", "severity": "High", "issue": "Chinese-backed operations; Mekong tributary contamination; deforestation; no EIA compliance", "source": "Global Witness / Mekong River Commission"},

    # ===== VIETNAM =====
    {"name": "Dong Pao REE Mine (Lai Chau)", "lat": 22.09, "lon": 103.67, "country": "Vietnam", "state": "Lai Chau", "type": "Rare Earth Mine", "mineral": "REE/Fluorite/Bastnäsite", "status": "Active", "severity": "High", "issue": "Rare Earth Vietnam/Toyota Tsusho JV; tailings in upland area feeding Nam Na River; radioactive dust during dry season", "source": "VIGMR Vietnam / USGS REE Statistics / Vietnam Environment Administration"},
    {"name": "Yen Phu REE Deposit", "lat": 22.30, "lon": 104.30, "country": "Vietnam", "state": "Yen Bai", "type": "Rare Earth Mine", "mineral": "REE/Monazite", "status": "Active", "severity": "Moderate", "issue": "Small artisanal REE extraction; radioactive tailings near Red River tributaries", "source": "Vietnam MONRE / USGS"},

    # ===== MALAYSIA =====
    {"name": "Lynas LAMP REE Processing (Gebeng)", "lat": 3.86, "lon": 103.30, "country": "Malaysia", "state": "Pahang", "type": "Rare Earth Mine", "mineral": "REE Processing (Australian ore)", "status": "Active", "severity": "High", "issue": "Processing of Mount Weld ore; thorium and uranium waste storage controversy; 2012 protests involving 15,000 people; WLP (Water Leaching Purification) residue storage problem", "source": "Lynas Rare Earths / Malaysian AELB / Greenpeace / Nature News 2012"},

    # ===== BRAZIL =====
    {"name": "Araxá Niobium-REE Complex", "lat": -19.59, "lon": -46.94, "country": "Brazil", "state": "Minas Gerais", "type": "Rare Earth Mine", "mineral": "REE/Niobium/Phosphate", "status": "Active", "severity": "Moderate", "issue": "CBMM world's largest niobium mine; co-occurring REE by-product; tailings pond management; radioactive thorium in waste", "source": "CBMM / Brazilian DNPM / USGS REE Statistics", "production_tpa": 3000, "reserves_mt": 10},
    {"name": "São Timóteo REE Exploration (Poços de Caldas)", "lat": -21.79, "lon": -46.57, "country": "Brazil", "state": "Minas Gerais", "type": "Rare Earth Mine", "mineral": "REE/Uranium", "status": "Active", "severity": "Moderate", "issue": "Historical Brazilian nuclear program REE extraction; uranium co-occurrence; acid drainage legacy", "source": "INB Brazil / USGS / IAEA"},

    # ===== GREENLAND/DENMARK =====
    {"name": "Kvanefjeld/Kuannersuit REE-Uranium (Greenland)", "lat": 61.15, "lon": -45.13, "country": "Greenland", "state": "Kujalleq", "type": "Rare Earth Mine", "mineral": "REE/Uranium/Zinc", "status": "Active", "severity": "High", "issue": "Greenland Minerals project; world's 2nd-largest REE deposit; uranium extraction controversial; 2021 Greenlandic parliament banned uranium mining; tailings near Narsaq fjord", "source": "Greenland Minerals Ltd / USGS / Nature Climate Change", "reserves_mt": 1010},

    # ===== RUSSIA =====
    {"name": "Lovozero REE Mine (Kola Peninsula)", "lat": 68.00, "lon": 35.00, "country": "Russia", "state": "Murmansk", "type": "Rare Earth Mine", "mineral": "REE/Loparite", "status": "Active", "severity": "Moderate", "issue": "Loparite ore extraction; radioactive tailings from thorium; Arctic ecosystem sensitivity", "source": "USGS REE Statistics / Russian Geological Institute", "production_tpa": 3000, "reserves_mt": 1.5},
    {"name": "Tomtor REE Deposit (Yakutia)", "lat": 68.50, "lon": 117.00, "country": "Russia", "state": "Sakha Republic", "type": "Rare Earth Mine", "mineral": "REE/Niobium", "status": "Active", "severity": "Moderate", "issue": "Developed by Peak Resources/Russian interests; permafrost thaw risk for tailings; Arctic contamination risk in remote area", "source": "USGS / Geokhi Russian Academy of Sciences", "reserves_mt": 154},

    # ===== CANADA =====
    {"name": "Strange Lake REE Deposit (Quebec/Labrador)", "lat": 56.40, "lon": -63.90, "country": "Canada", "state": "Quebec/Labrador", "type": "Rare Earth Mine", "mineral": "HREE/Zirconium/Hafnium", "status": "Active", "severity": "Moderate", "issue": "Quest Rare Minerals; remote boreal site; tailings management in sub-Arctic; contamination risk to George River system", "source": "USGS / Quest Rare Minerals", "reserves_mt": 278},
    {"name": "Montviel REE Carbonatite (Quebec)", "lat": 49.80, "lon": -75.20, "country": "Canada", "state": "Quebec", "type": "Rare Earth Mine", "mineral": "REE/Carbonatite", "status": "Active", "severity": "Low", "issue": "Exploration; thorium byproduct management required in Quebec regulation", "source": "Commerce Resources / Quebec MERN", "reserves_mt": 96},

    # ===== NORWAY =====
    {"name": "Fen Carbonatite REE (Telemark)", "lat": 59.48, "lon": 9.38, "country": "Norway", "state": "Telemark", "type": "Rare Earth Mine", "mineral": "REE/Niobium", "status": "Active", "severity": "Low", "issue": "REE Norway project; EU Critical Raw Materials Act priority; thorium/uranium co-occurrence in carbonatite; historical radium contamination legacy", "source": "REE Norway AS / NGU / European Commission CRM Act 2023"},

    # ===== SWEDEN =====
    {"name": "Norra Kärr HREE Deposit", "lat": 57.93, "lon": 14.70, "country": "Sweden", "state": "Jönköping", "type": "Rare Earth Mine", "mineral": "HREE/Zirconium", "status": "Active", "severity": "Moderate", "issue": "Tasman Metals / Leading Edge Materials; lake contamination risk; Swedish Environmental Court rejected 2021; critical EU supply chain debate", "source": "Leading Edge Materials / SGU / EU CRM Alliance"},

    # ===== SOUTH AFRICA =====
    {"name": "Steenkampskraal Monazite Mine", "lat": -30.85, "lon": 18.73, "country": "South Africa", "state": "Western Cape", "type": "Rare Earth Mine", "mineral": "REE/Monazite/Thorium", "status": "Active", "severity": "High", "issue": "World's highest-grade REE-monazite deposit; thorium nuclear waste classification dispute; Steenkampskraal Thorium Ltd vs NNR; Great Escarpment water source risk", "source": "Steenkampskraal Thorium Ltd / South Africa NNR / DMRE"},
    {"name": "Glenover Carbonatite (Limpopo)", "lat": -24.07, "lon": 26.98, "country": "South Africa", "state": "Limpopo", "type": "Rare Earth Mine", "mineral": "REE/Phosphate/Vermiculite", "status": "Active", "severity": "Moderate", "issue": "Orion Minerals; phosphate–REE co-processing; Lephalale catchment dust/water impacts", "source": "Orion Minerals / DMRE SA / USGS"},

    # ===== MALAWI =====
    {"name": "Kangankunde REE Carbonatite", "lat": -15.61, "lon": 34.91, "country": "Malawi", "state": "Balaka", "type": "Rare Earth Mine", "mineral": "REE/Monazite", "status": "Active", "severity": "Moderate", "issue": "Mkango Resources; underdeveloped national regulations; Shire River catchment contamination risk; local water use conflicts", "source": "Mkango Resources / USGS REE Statistics", "reserves_mt": 2.8},

    # ===== TANZANIA =====
    {"name": "Ngualla REE Carbonatite", "lat": -9.07, "lon": 33.35, "country": "Tanzania", "state": "Mbeya", "type": "Rare Earth Mine", "mineral": "REE/Bastnäsite", "status": "Active", "severity": "Moderate", "issue": "Peak Resources; thorium waste management; Great Rift Valley water system at risk; land tenure disputes", "source": "Peak Resources / USGS / Tanzania NEMC", "reserves_mt": 214},

    # ===== KAZAKHSTAN =====
    {"name": "Aktogay REE-adjacent Copper", "lat": 46.88, "lon": 79.42, "country": "Kazakhstan", "state": "East Kazakhstan", "type": "Rare Earth Mine", "mineral": "REE/Copper", "status": "Active", "severity": "Moderate", "issue": "Kazakhmys; REE in copper porphyry; tailings dam failure risk in seismic zone; Irtysh River contamination concern", "source": "Kazakhmys / Kazakhstan MNE"},

    # ===== KYRGYZSTAN =====
    {"name": "Kutessay II REE Mine", "lat": 42.73, "lon": 76.03, "country": "Kyrgyzstan", "state": "Chuy", "type": "Rare Earth Mine", "mineral": "REE/Fluorspar", "status": "Active", "severity": "High", "issue": "Soviet-era mine being restarted; radioactive tailings from processing; Chuy River (drinking water for Bishkek) at risk", "source": "USGS / Stans Energy / IAEA TECDOC", "production_tpa": 1500},

    # ===== JAPAN =====
    {"name": "Minamata REE/Heavy Metal Legacy", "lat": 32.22, "lon": 130.40, "country": "Japan", "state": "Kumamoto", "type": "Abandoned Mine", "mineral": "Mercury/REE Processing", "status": "Abandoned", "severity": "Critical", "issue": "Chisso chemical plant processed REE; mercury effluent caused Minamata disease (1956+); 10,000+ deaths/affected; UN Convention on Mercury named after this site", "source": "Kumamoto Prefecture / Minamata Disease Center / UN GEMS", "year_abandoned": 1968},

    # ===== ESTONIA =====
    {"name": "Estonia Oil Shale / REE by-product", "lat": 59.40, "lon": 27.30, "country": "Estonia", "state": "Ida-Viru", "type": "Active Mine", "mineral": "Oil Shale/REE by-product", "status": "Active", "severity": "Moderate", "issue": "World's largest oil shale mining district; REE in ash; water pollution of Lake Peipsi; semicoke dumps >150 km²", "source": "Eesti Energia / Estonian EPA / EJAtlas"},

    # ===== PHILIPPINES =====
    {"name": "Palawan REE Monazite Sands", "lat": 10.50, "lon": 119.50, "country": "Philippines", "state": "Palawan", "type": "Rare Earth Mine", "mineral": "REE/Monazite/Zircon", "status": "Active", "severity": "Moderate", "issue": "Beach sand mining in biodiversity hotspot; coral reef impacts; radioactive monazite dust; UNESCO World Heritage buffer zone encroachment", "source": "DENR Philippines / USGS REE / EJAtlas Philippines"},

    # ===== MADAGASCAR =====
    {"name": "Tantalum-REE Deposits (Ampasindava)", "lat": -13.80, "lon": 47.90, "country": "Madagascar", "state": "Diana", "type": "Rare Earth Mine", "mineral": "REE/Tantalum/Niobium", "status": "Active", "severity": "High", "issue": "Tantalus Rare Earths; intact rainforest loss; lemur habitat destruction; Ambanja Bay contamination risk", "source": "Tantalus Rare Earths / USGS / WWF Madagascar"},

    # ===== MONGOLIA =====
    {"name": "Mushgai Khudag REE-Fluorite", "lat": 43.92, "lon": 104.77, "country": "Mongolia", "state": "South Gobi", "type": "Rare Earth Mine", "mineral": "REE/Fluorite/Phosphate", "status": "Active", "severity": "Moderate", "issue": "Energy Resources / LightPath Technologies; fluoride contamination of Gobi aquifer; nomadic herder water access", "source": "Mongolian Ministry of Mining / USGS"},
]

def get_mine_events():
    """Convert mine data to event format compatible with the map system."""
    events = []
    for m in ABANDONED_MINES:
        events.append({
            "type": "Abandoned Mine" if m.get("status") == "Abandoned" else "Active Mine",
            "title": m["name"],
            "lat": m["lat"],
            "lon": m["lon"],
            "country": m["country"],
            "severity": m.get("severity", "Moderate"),
            "description": m.get("issue", ""),
            "source": m.get("source", "USGS/Research"),
            "mineral": m.get("mineral", ""),
            "status": m.get("status", "Unknown"),
            "date": str(m.get("year_abandoned", "Ongoing")),
            "state": m.get("state", ""),
        })
    return events

def get_rare_earth_events():
    """Convert rare earth mine data to event format compatible with the map system."""
    events = []
    for m in RARE_EARTH_MINES:
        events.append({
            "type": "Rare Earth Mine",
            "title": m["name"],
            "lat": m["lat"],
            "lon": m["lon"],
            "country": m["country"],
            "severity": m.get("severity", "Moderate"),
            "description": m.get("issue", ""),
            "source": m.get("source", "USGS REE Statistics"),
            "mineral": m.get("mineral", ""),
            "status": m.get("status", "Unknown"),
            "date": str(m.get("year_abandoned", "Ongoing")),
            "state": m.get("state", ""),
            "production_tpa": m.get("production_tpa"),
            "reserves_mt": m.get("reserves_mt"),
        })
    return events

def get_mines_by_country(country, limit=20):
    """Get all mine events (abandoned + active + REE) for a specific country."""
    results = []
    for m in ABANDONED_MINES + RARE_EARTH_MINES:
        if m.get("country", "").lower() == country.lower():
            results.append(m)
    return sorted(results, key=lambda x: {"Critical": 4, "High": 3, "Moderate": 2, "Low": 1}.get(x.get("severity", "Low"), 0), reverse=True)[:limit]

def get_mines_by_status(status="Abandoned", limit=50):
    """Get mines filtered by status: Abandoned, Active."""
    return [m for m in ABANDONED_MINES if m.get("status") == status][:limit]

def get_critical_mines(limit=20):
    """Get highest-severity mines across all categories."""
    all_mines = ABANDONED_MINES + RARE_EARTH_MINES
    critical = [m for m in all_mines if m.get("severity") == "Critical"]
    return sorted(critical, key=lambda x: x.get("name", ""))[:limit]
