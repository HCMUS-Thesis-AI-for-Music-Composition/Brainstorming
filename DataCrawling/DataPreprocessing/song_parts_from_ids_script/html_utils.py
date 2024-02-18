import xmltodict
import json

import utils as ut

class ResponseType:
    JSON = "json"
    XML = "xml"
    UNKNOWN = "unknown"

def response_data_parser(response_json):
    metadata = None
    main_data_type = None
    main_data = None

    if "jsonData" in response_json and response_json["jsonData"] is not None:
        main_data_type = ResponseType.JSON
        main_data = json.loads(response_json["jsonData"])
    elif "xmlData" in response_json and response_json["xmlData"] is not None:
        main_data_type = ResponseType.XML
        main_data = xmltodict.parse(response_json["xmlData"])
    else:
        main_data_type = ResponseType.UNKNOWN
        main_data = response_json

        print(f"WARNING: response_data_parser: Unknown response type: {response_json}")

    try:
        del response_json["jsonData"]
        del response_json["xmlData"]
    except:
        print(f"WARNING: response_data_parser: Unable to delete jsonData or xmlData from response_json: {response_json}")

    metadata = response_json

    return metadata, main_data_type, main_data

def make_request(session, url, parameters: dict = None, headers: dict = None):
    print(f"--------> REQUESTING: {url}")

    status_code = None
    metadata = None
    main_data_type = None
    main_data = None
    
    try:
        response = session.get(url, params=parameters)
        status_code = response.status_code

        if status_code != 200:
            print(f"-----------> FAIL: make_request - status_code: {status_code}: {ut.http_status_code[status_code]} - {url}")
        else:        
            if response.headers['Content-Type'] == 'application/json; charset=UTF-8':
                metadata, main_data_type, main_data = response_data_parser(response.json())
            else:
                print(f"-----------> FAIL: make_request - unknown format: {url}")
        
    except Exception as e:
        print(f"-----------> FAIL: make_request - exception: {e} - {url}")

    if main_data is None or len(main_data) == 0:
        print(f"-----------> WARNING: make_request - empty main_data: {url}")

    return {
        'status_code' : status_code,
        'metadata' : metadata,
        'main_data_type' : main_data_type,
        'main_data' : main_data # Tương ứng với phần jsonData hoặc xmlData
    }
