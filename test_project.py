import os
from project import is_valid, detect_anomalies, convert_json
def test_is_valid():
    assert is_valid("2026-09-23 20:41:00")==True
    assert is_valid("23-09-2026 20:41:00")==False
    assert is_valid("00:23")==False
    assert is_valid("text")==False

def test_detect_anomalies():
    data=[{"timestamp": "2026-09-23 20:41:00", "speed": "150", "altitude": "2000"},{"timestamp": "2026-09-23 20:42:00", "speed": "250", "altitude": "2000"},{"timestamp": "2026-09-23 20:43:00", "speed": "150", "altitude": "500"},{"timestamp": "Bozuk_Veri", "speed": "150", "altitude": "2000"}]
    anomalies=detect_anomalies(data,max_speed=200,min_altitude=1000)
    assert len(anomalies)==3
    assert anomalies[0]["error_type"]=="Rule Violation"
    assert anomalies[2]["error_type"]=="Invalid timestamp"

def test_convert_json():
    anomalies=[{"timestamp":"2026-09-23","error_type":"Test Error"}]
    f="test.json"
    convert_json(anomalies,f)
    assert os.path.exists(f)==True
    if os.path.exists(f):
        os.remove(f)
