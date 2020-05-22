
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Basic CDM solutionManager capabilities check.
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-16327
    +timeout: 120
    +asset: CDM
    +test_framework: TUF
    +name: test_getSolutionManagerCapabilities
    +test:
        +title: test_getSolutionManagerCapabilities
        +guid:d54d329f-4b7b-4dc9-8e50-f4ac37cf3e69
        +dut:
            +type:Simulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
# =============================================================================

def test_getSolutionManagerCapabilities(cdm):    
    import re
    import pytest
    import requests
    import json        

    URL = "cdm/solutionManager/v1/capabilities"  
    #  Need to change above URL to use fixture or passed in parameter of IP
    # sending get request and saving the response as response object 
    r = cdm.get_raw(URL)  
    assert r.status_code ==200

   # You can extract json two ways: via json.loads of the text or built in functions
    jsonLoad = json.loads(r.text)
    jsonResponse = r.json() 
    # Validate each dictionary pair in JSON response is identical in both extract methods above
    # Debug Code: step through loops and validate both methods are identical
    i = 1
    for key, value in jsonResponse.items():
        i = i + 1
    # Validate each dictionary pair in JSON load
    i = 1
    for key, value in jsonLoad.items():
        i = i + 1

    # ========================================================================
    # validate response contains right version # and capability text 
    # These are the minimum tests to pass
    # ========================================================================
    apiVersion = jsonResponse["apiVersion"]
    assert apiVersion == "1.0.0"

    implVersion = jsonResponse["implVersion"]
    assert implVersion == "1.0.0.alpha-8"
    
    # ========================================================================
    # Added Bonus tests:
    # Validate the body of the links in the response
    # adding these tests since will be needed in future.
    # ========================================================================

    # validate links on response body ['self', 'installer', 'solutions']
    jsonLink = extract_values(r.json(), "rel")
   
    linkSelf = jsonLink[0]                 # 'self'
    assert linkSelf == 'self'
    linkInstaller = jsonLink[1]            # 'installer'
    assert linkInstaller == 'installer'
    linkSolutions = jsonLink[2]            # 'solutions'
    assert linkSolutions == 'solutions'

    # validate href in response body
    # ['/solutionManager/v1/capabilities', '/solutionManager/v1/installer', '/solutionManager/v/solutions']
    jsonHref = extract_values(r.json(), "href")
    hrefCapabilities = jsonHref[0]             # '/solutionManager/v1/capabilities'
    assert hrefCapabilities == '/solutionManager/v1/capabilities'
    hrefInstaller = jsonHref[1]                # '/solutionManager/v1/installer'
    assert hrefInstaller    == '/solutionManager/v1/installer'
    hrefSolutions = jsonHref[2]                # '/solutionManager/v1/solutions'
    assert hrefSolutions    ==  '/solutionManager/v1/solutions'
    print ("Test End")