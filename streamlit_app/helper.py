import streamlit as st
import streamlit.components.v1 as components
import datetime
import joblib
import settings
import xgboost as xgb


# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Use Local js file
def local_js(file_name):
    with open(file_name) as f:
        components.html(f"<script>{f.read()}</script>", height=0, width=0)


# Get model
def load_model():
    model=joblib.load(settings.PREDICTION_MODEL)
    return model

def load_ccsr_model():
    model=joblib.load(settings.PREDICTION_MODEL_CCSR)
    return model

def user_inputs():
    # defining options for feature selection
    hospital_service_area_options = ['New York City', 'Hudson Valley', 'Long Island', 'Western NY','Capital/Adirond', 'Finger Lakes', 'Central NY', 'Southern Tier', 'N/A']

    hospital_county_options = ['Manhattan', 'Bronx', 'Westchester', 'Nassau', 'Queens', 'Kings', 'Erie', 'Otsego', 'Rockland', 'Monroe', 'Albany','Cayuga', 'Columbia', 'Dutchess', 'Onondaga', 'Steuben', 'Orange', 'Richmond', 'Ontario', 'Niagara', 'Suffolk', 'Broome', 'Oneida', 'Chautauqua', 'Franklin', 'Livingston', 'Ulster', 'Putnam', 'Schenectady', 'Genesee', 'Montgomery', 'Warren', 'Jefferson', 'Saratoga', 'Madison', 'Cortland', 'Clinton', 'Yates', 'Tompkins', 'Oswego', 'Chenango', 'Rensselaer', 'Sullivan', 'St Lawrence', 'Wyoming', 'Fulton', 'Wayne', 'Chemung', 'Cattaraugus', 'Essex', 'Schoharie', 'Allegany', 'Delaware', 'Lewis', 'Herkimer', 'Orleans', 'Schuyler', 'N/A']

    facility_name_options = ["Albany Medical Center Hospital",
                            "Albany Memorial Hospital",
                            "Arnot Ogden Medical Center",
                            "Auburn Community Hospital",
                            "Aurelia Osborn Fox Memorial Hospital",
                            "Bellevue Hospital Center",
                            "Benedictine Hospital",
                            "Beth Israel Medical Center/Petrie Campus",
                            "Bronx-Lebanon Hospital Center - Concourse Division",
                            "Brookdale Hospital Medical Center",
                            "Brookhaven Memorial Hospital Medical Center Inc",
                            "Brooklyn Hospital Center - Downtown Campus",
                            "Buffalo General Medical Center",
                            "Calvary Hospital Inc",
                            "Canton-Potsdam Hospital",
                            "Cayuga Medical Center at Ithaca",
                            "Champlain Valley Physicians Hospital Medical Center",
                            "Columbia Memorial Hospital",
                            "Coney Island Hospital",
                            "Corning Hospital",
                            "Cortland Regional Medical Center Inc",
                            "Crouse Hospital",
                            "Ellis Hospital",
                            "Elmhurst Hospital Center",
                            "Erie County Medical Center",
                            "F F Thompson Hospital",
                            "Faxton-St Lukes Healthcare St Lukes Division",
                            "Flushing Hospital Medical Center",
                            "Forest Hills Hospital",
                            "Franklin Hospital",
                            "Geneva General Hospital",
                            "Glen Cove Hospital",
                            "Glens Falls Hospital",
                            "Good Samaritan Hospital Medical Center",
                            "Good Samaritan Hospital of Suffern",
                            "Harlem Hospital Center",
                            "HealthAlliance Hospital Broadway Campus",
                            "Highland Hospital",
                            "Huntington Hospital",
                            "Jacobi Medical Center",
                            "Jamaica Hospital Medical Center",
                            "John T Mather Memorial Hospital of Port Jefferson New York Inc",
                            "Kenmore Mercy Hospital",
                            "Kings County Hospital Center",
                            "Kingsbrook Jewish Medical Center",
                            "Lenox Hill Hospital",
                            "Lincoln Medical & Mental Health Center",
                            "Long Island Jewish Medical Center",
                            "Maimonides Medical Center",
                            "Mary Imogene Bassett Hospital",
                            "Memorial Hospital for Cancer and Allied Diseases",
                            "Mercy Hospital of Buffalo",
                            "Mercy Medical Center",
                            "Metropolitan Hospital Center",
                            "Mid-Hudson Valley Division of Westchester Medical Center",
                            "Millard Fillmore Suburban Hospital",
                            "Montefiore Med Center - Jack D Weiler Hosp of A Einstein College Div",
                            "Montefiore Medical Center - Henry & Lucy Moses Div",
                            "Montefiore Medical Center-Wakefield Hospital",
                            "Montefiore New Rochelle Hospital",
                            "Mount Sinai Brooklyn",
                            "Mount Sinai Hospital",
                            "Mount Sinai Hospital - Mount Sinai Hospital of Queens",
                            "Mount St Marys Hospital and Health Center",
                            "NYU Hospitals Center",
                            "NYU Lutheran Medical Center",
                            "Nassau University Medical Center",
                            "New York - Presbyterian Hospital",
                            "New York - Presbyterian/Queens",
                            "New York Community Hospital of Brooklyn, Inc",
                            "New York Methodist Hospital",
                            "New York Presbyterian Hospital - Columbia Presbyterian Center",
                            "New York Presbyterian Hospital - New York Weill Cornell Center",
                            "New York-Presbyterian/Lower Manhattan Hospital",
                            "NewYork-Presbyterian/Hudson Valley Hospital",
                            "Niagara Falls Memorial Medical Center",
                            "North Shore University Hospital",
                            "Northern Westchester Hospital",
                            "Nyack Hospital",
                            "Olean General Hospital",
                            "Orange Regional Medical Center",
                            "Our Lady of Lourdes Memorial Hospital Inc",
                            "Peconic Bay Medical Center",
                            "Peninsula Hospital Center",
                            "Phelps Memorial Hospital Assn",
                            "Plainview Hospital",
                            "Putnam Hospital Center",
                            "Queens Hospital Center",
                            "Richmond University Medical Center",
                            "Rochester General Hospital",
                            "Rome Memorial Hospital, Inc",
                            "Roswell Park Cancer Institute",
                            "SBH Health System",
                            "SJRH - St Johns Division",
                            "SUNY Downstate Medical Center at LICH",
                            "Samaritan Hospital",
                            "Samaritan Medical Center",
                            "Saratoga Hospital",
                            "Seton Health System-St Mary's Campus",
                            "Sisters of Charity Hospital",
                            "Sisters of Charity Hospital - St Joseph Campus",
                            "South Nassau Communities Hospital",
                            "Southampton Hospital",
                            "Southside Hospital",
                            "St Catherine of Siena Hospital",
                            "St Elizabeth Medical Center",
                            "St Francis Hospital",
                            "St Johns Episcopal Hospital So Shore",
                            "St Josephs Hospital Health Center",
                            "St Luke's Cornwall Hospital/Newburgh",
                            "St Lukes Roosevelt Hospital - St Lukes Hospital Division",
                            "St Lukes Roosevelt Hospital Center - Roosevelt Hospital Division",
                            "St Peters Hospital",
                            "St. Joseph Hospital",
                            "St. Mary's Healthcare",
                            "Staten Island University Hosp-North",
                            "Staten Island University Hosp-South",
                            "Strong Memorial Hospital",
                            "The Unity Hospital of Rochester",
                            "UPSTATE University Hospital at Community General",
                            "United Health Services Hospitals Inc. - Wilson Medical Center",
                            "United Memorial Medical Center North Street Campus",
                            "University Hospital",
                            "University Hospital SUNY Health Science Center",
                            "University Hospital of Brooklyn",
                            "Vassar Brothers Medical Center",
                            "Westchester Medical Center",
                            "White Plains Hospital Center",
                            "Winthrop-University Hospital",
                            "Woman's Christian Association",
                            "Woodhull Medical & Mental Health Center",
                            "Wyckoff Heights Medical Center"]

    age_group_options = ['50 to 69', '70 or Older', '30 to 49', '18 to 29', '0 to 17']

    gender_options = ['Male', 'Female']

    race_options = ['Other Race', 'White', 'Black/African American', 'Multi-racial',
        'Unknown']

    ethnicity_options = ['Not Span/Hispanic', 'Spanish/Hispanic', 'Multi-ethnic', 'Unknown']

    apr_severity_of_illness_code_options = ['Minor', 'Moderate', 'Major', 'Extreme']

    ccsr_procedure_options = ["CARDIAC CHEST COMPRESSION",
                            "UPPER GI THERAPEUTIC PROCEDURES, NEC (ENDOSCOPIC)",
                            "VACCINATIONS",
                            "ELECTROENCEPHALOGRAM (EEG)",
                            "ELECTROCARDIOGRAM (ECG)",
                            "TRANSFUSION OF PLASMA",
                            "PHYSICAL, OCCUPATIONAL, AND RESPIRATORY THERAPY TREATMENT",
                            "MEASUREMENT DURING CARDIAC CATHETERIZATION",
                            "BONE MARROW BIOPSY",
                            "LARYNGOSCOPY (DIAGNOSTIC)",
                            "REGIONAL ANESTHESIA",
                            "RADIATION THERAPY, NEC",
                            "MAGNETIC RESONANCE IMAGING (MRI)",
                            "LUMBAR PUNCTURE",
                            "GI SYSTEM ENDOSCOPY WITHOUT BIOPSY (DIAGNOSTIC)",
                            "INFERIOR VENA CAVA (IVC) FILTER PROCEDURES",
                            "PLAIN RADIOGRAPHY",
                            "CHEST WALL PROCEDURES, NEC",
                            "GASTROSTOMY",
                            "ENDOCRINE SYSTEM BIOPSY",
                            "SUBCUTANEOUS TISSUE, FASCIA, AND MUSCLE BIOPSY",
                            "BLADDER CATHETERIZATION AND DRAINAGE",
                            "AIRWAY INTUBATION",
                            "ESOPHAGOGASTRODUODENOSCOPY (EGD) WITH BIOPSY",
                            "HEMODIALYSIS",
                            "MEDIASTINAL PROCEDURES, NEC",
                            "ADMINISTRATION OF ANTI-INFLAMMATORY AGENTS",
                            "BRONCHOSCOPY (THERAPEUTIC)",
                            "BRONCHOSCOPIC EXCISION AND FULGURATION",
                            "PARACENTESIS",
                            "RESPIRATORY SYSTEM PROCEDURES, NEC",
                            "COMPUTERIZED TOMOGRAPHY (CT) WITHOUT CONTRAST",
                            "PERICARDIAL PROCEDURES",
                            "ADMINISTRATION OF NUTRITIONAL AND ELECTROLYTIC SUBSTANCES",
                            "ISOLATION PROCEDURES",
                            "BONE AND JOINT BIOPSY",
                            "LUNG, PLEURA, OR DIAPHRAGM RESECTION (OPEN AND THORACOSCOPIC)",
                            "PLACEMENT OF TUNNELED OR IMPLANTABLE PORTION OF A VASCULAR ACCESS DEVICE",
                            "COMPUTERIZED TOMOGRAPHY (CT) WITH CONTRAST",
                            "BEAM RADIATION",
                            "MECHANICAL VENTILATION",
                            "VENOUS AND ARTERIAL CATHETER PLACEMENT",
                            "ULTRASONOGRAPHY",
                            "ADMINISTRATION OF ANTIBIOTICS",
                            "CHEMOTHERAPY",
                            "OPEN AND THORACOSCOPIC PLEURAL DRAINAGE",
                            "LYMPH NODE BIOPSY",
                            "LIVER BIOPSY",
                            "NON-INVASIVE VENTILATION",
                            "TRANSFUSION OF BLOOD AND BLOOD PRODUCTS",
                            "ADMINISTRATION OF THERAPEUTIC SUBSTANCES, NEC",
                            "THORACENTESIS (DIAGNOSTIC)",
                            "LUNG, PLEURA, OR DIAPHRAGM BIOPSY (NON-ENDOSCOPIC)",
                            "BRONCHOSCOPY (DIAGNOSTIC)",
                            "CHEST TUBE PLACEMENT AND THERAPEUTIC THORACENTESIS",
                            "NO PROCEDURE"]

    # form layout
    with st.container():
        st.subheader('Patient information')
        col1, col2 = st.columns(2)
        with col1:
            age                                  = st.number_input('Enter your age:', min_value=0)
            if age >= 0 and age <= 17:
                age_group = '0 to 17'
            elif age >= 18 and age <= 29:
                age_group = '18 to 29'
            elif age >= 30 and age <= 49:
                age_group = '30 to 49'
            elif age >= 50 and age <= 69:
                age_group = '50 to 69'
            else:
                age_group = '70 or Older'

            sex                                  = st.selectbox('Select your gender', gender_options)
            if sex == 'Male':
                gender = 'M'
            else:
                gender = 'F'

        with col2:
            race                                 = st.selectbox('Select your race', race_options)
            ethnicity                            = st.selectbox('Select your ethnicity', ethnicity_options)
 
        st.subheader('Medical information')
        col1, col2 = st.columns(2)
        with col1:
            severity_of_illness_code             = st.selectbox('What is the severity of illness?', apr_severity_of_illness_code_options, help="Severity of illness refers to how serious a patient's medical condition is. Please select what stage of Cancer you are diagnosed with.")
            if severity_of_illness_code == 'Minor':
                apr_severity_of_illness_code = "1"
            elif severity_of_illness_code == 'Modarate':
                apr_severity_of_illness_code = "2"
            elif severity_of_illness_code == 'Major':
                apr_severity_of_illness_code = "3"
            else:
                apr_severity_of_illness_code = "4"

        with col2:
            current_year = datetime.datetime.now().year
            discharge_year                  = st.selectbox('Select estimated discharge year:', list(range(current_year, current_year + 2)))

        ccsr_info                               = st.radio('Do you have treatment plan information', ['No', 'Yes'], help="A treatment plan is a step-by-step process that healthcare professionals follow to provide medical care or therapy to a patient. Select Yes if you have the diagnosis information provided by your doctor.")
        if ccsr_info == 'Yes':
            ccsr_procedure                      = st.selectbox('Select treatment procedure', ccsr_procedure_options)
            if ccsr_procedure == 'NO PROCEDURE':
                ccsr_procedure = 'NO PROC'
        else:
            ccsr_procedure = 'No'
        
        st.subheader('Hospital information')
        col1, col2 = st.columns(2)
        with col1:
            facility_name                        = st.selectbox('Select Hospital / Medical Center Name:', facility_name_options)

            length_of_stay                       = st.slider('Enter estimated Length of stay in days', min_value=1, max_value=35, step=1, help="Use this slider to vary the estimated expense based on the duration you choose for the stay in the hospital. If your estimated length of stay is longer than 35 days, please select 35 using slider.")

        with col2:
            hospital_county                      = st.selectbox('Select Hospital County', hospital_county_options)

    ny_data = {"columns":["county","facility_name","age_group" ,"gender","race","ethnicity", "ccsr_procedure_desc", "length_of_stay","year","severity_of_illness_code"],
            "data":[hospital_county, facility_name, age_group, gender, race, ethnicity, ccsr_procedure, length_of_stay, discharge_year, apr_severity_of_illness_code]}
    return ny_data