from playwright.sync_api import expect
from app import password_complexity


def test_signup_rejects_password_mismatch(
    page,
    test_web_address
):
    page.goto(f"http://{test_web_address}/signup")

    page.fill("input[name='username']", "newuser")
    page.fill("input[name='password']", "password!")
    page.fill("input[name='confirm_password']", "different!")

    page.click("text='Sign up'")

    expect(page.locator("body")).to_contain_text(
        "Passwords did not match"
    )

def test_password_complexity_accepts_valid_password():
    assert password_complexity("password!")

def test_password_complexity_rejects_short_password():
    assert password_complexity("pass!") is False

def test_password_complexity_rejects_missing_special_char():
    assert password_complexity("password123") is False

# def test_book_gig_rejects_non_integer_ticket_count(
#     logged_in_page_username,
#     test_web_address
# ):
#     logged_in_page_username.goto(
#         f"http://{test_web_address}/gigs/2"
#     )

#     logged_in_page_username.fill(
#         "input[name='ticket_count']",
#         3
#     )

#     logged_in_page_username.click("text='Book gig'")

#     expect(
#         logged_in_page_username.locator("body")
#     ).to_contain_text("Non-integer ticket number requested")

def test_signup_blank_username(page, test_web_address):
    page.goto(f"http://{test_web_address}/signup")
    page.fill("input[name='username']", "")
    page.fill("input[name='password']", "Password!")
    page.fill("input[name='confirm_password']", "Password!")
    page.click("text='Sign up'")
    expect(page.locator("body")).to_contain_text("Username cannot be blank")
    
def test_signup_admin_username(page, test_web_address):
    page.goto(f"http://{test_web_address}/signup")
    page.fill("input[name='username']", "admin")
    page.fill("input[name='password']", "Password!")
    page.fill("input[name='confirm_password']", "Password!")
    page.click("text='Sign up'")
    expect(page.locator("body")).to_contain_text("cannot be 'admin'")
    
def test_signup_weak_password(page, test_web_address):
    page.goto(f"http://{test_web_address}/signup")
    page.fill("input[name='username']", "user2")
    page.fill("input[name='password']", "abc")
    page.fill("input[name='confirm_password']", "abc")
    page.click("text='Sign up'")
    expect(page.locator("body")).to_contain_text("requirements not met")


# API tests
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