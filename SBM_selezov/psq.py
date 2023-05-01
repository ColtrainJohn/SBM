authentication = "host=localhost dbname=yuh4 user=django password=cafebabe"

sql_alchemy_auth = 'postgresql://django:cafebabe@localhost:5432/yuh4'

datapointColumns = ["patient_uuid", "original_id", "age", "birthdate", "sex", "observation_uuid", "date", "datapoint_uuid", "value", "city_id", "district_id", "parameter_id", "region_id", "dataset_id"]


birthDayCorrectionFile = '/mnt/disk1/PROJECTS/EPID_STAGE2/DATA/RAW_DATA/CMD/Результаты РПН/birth_correct.xlsx'
nonValidPatientsFile = '/mnt/disk1/PROJECTS/EPID_STAGE2/DATA/RAW_DATA/CMD/Результаты РПН/patients_delete.xlsx'

getGeography = """
SELECT 
    city.id as city_id, 
    city.name_ru AS city, 
    dist.id AS district_id, 
    dist.name_ru AS district, 
    city.region_id, 
    reg.name_ru AS region 
FROM 
    yuh_general_city AS city 
JOIN 
    yuh_general_district AS dist 
ON 
    city.district_id = dist.id 
JOIN 
    yuh_general_region AS reg 
ON 
    city.region_id = reg.id;
"""

parameters = """
SELECT 
    id AS parameter_id, name_en 
FROM 
    yuh_general_parameter;
"""

paramMapper = """
SELECT 
    * 
FROM 
    parameter_name_mapping 
WHERE 
    lab_id={dataset_id};
"""


insert_to_YUH_wc = """
COPY 
    yuh_general_datapoint(
        patient_uuid, 
        original_id, 
        age, 
        birthdate, 
        sex, 
        observation_uuid, 
        date, 
        datapoint_uuid, 
        value, 
        city_id, 
        district_id, 
        parameter_id, 
        region_id, 
        dataset_id
    )
FROM PROGRAM 
    'zcat {prep_loc}' 
DELIMITER 
    ',' 
CSV HEADER
"""

file_path_wc = '../../DATA/RAW_DATA/CMD/2023/{filename}.csv'
result_file_path_wc = '/mnt/disk1/PROJECTS/EPID_STAGE2/DATA/PREP_DATA/CMD/{filename}.csv.gz'


createRegionsTable = """
CREATE TABLE 
    region_name_mapping (
        id BIGSERIAL PRIMARY KEY, 
        city_id int,
        city varchar(255), 
        region_id int, 
        region varchar(255), 
        district_id int, 
        district varchar(255)
    );
"""

litechFeatures = [
    'Протр. вр.',
    'Протр. инд. по Квику', 'D-дим', 'Лейкоц', 'Эритроц', 'Гемогл',
    'Гематокрит', 'Сред.Vэритр.(MCV)', 'Ср.содерж.гемогл.в эрит.(MCH)',
    'Ср.конц. гемоглоб. в эритр.(MCHC)', 'RDW', 'Тромбоциты', 'MPV',
    'Бласты', 'Промиелоциты', 'Пролимфоциты', 'Миелоц', 'Метамиелоц',
    'Палочкояд.нейтр.', 'Сегментояд.нейтр.', 'Эозиноф%', 'Базоф',
    'Лимфоц(%)', 'Лимфоц(абс)', 'Моноциты', 'Плазмат.клетки', 'СОЭ',
    'АЛТ', 'ACT', 'Билир. общ', 'Креат-н (606)', 'К-та моч',
    'СРБ', 'NT-proBNP', 'РЭА', 'СА-19.9', 'СА-125', 'СА-15.3',
    'ПСАо. (292)', 'ПСА св.', 'ПСАсв.(%)', 'ЛГ', 'ФСГ'
]


test_cmd_datapoints = "/mnt/disk1/PROJECTS/EPID_STAGE2/DATA/RAW_DATA/CMD/2023/results_20230412_20230416.csv"

test_patients_invitro = "/mnt/disk1/PROJECTS/EPID_STAGE2/DATA/RAW_DATA/INVITRO/Актуальные_справочники_02Feb2023/patients.csv"
test_datapoints_invitro = "/mnt/disk1/PROJECTS/EPID_STAGE2/DATA/RAW_DATA/INVITRO/27.12.2022_17.01.2023/data_20230117.csv"

test_datapoints_litech = "/mnt/disk1/PROJECTS/EPID_STAGE2/DATA/RAW_DATA/Liteh_Center/2023/08.02-15.02.xlsx"