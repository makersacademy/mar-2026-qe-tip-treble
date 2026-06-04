import json

def test_get_existing_gig_returns_200(web_client, test_web_address ):
    response = web_client.get(f"http://{test_web_address}/api/gigs/1")
    assert response.status_code == 200
    
def test_get_nonexistent_gig(web_client, test_web_address):
    response = web_client.get(f"http://{test_web_address}/api/gigs/9999")
    assert response.status_code in [200, 404]
    
def test_api_unknown_path_returns_404(web_client, test_web_address):
    response = web_client.get(f"http://{test_web_address}/api/notarealpath")
    assert response.status_code == 404
   
def test_api_accounts_requires_login(web_client, test_web_address):
    response = web_client.get(f"http://{test_web_address}/api/accounts/1")
    assert response.status_code == 401
    

def test_api_gigs_returns_list(web_client, db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    response = web_client.get("/api/gigs")
    assert response.status_code == 200
   
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    
def test_api_band_returns_matching_gigs(web_client, db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    response = web_client.get("/api/bands/Placebo")
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data) == 2
