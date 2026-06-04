from playwright.sync_api import expect
from app import password_complexity

def test_get_index(page, test_web_address):
    page.goto(f"http://{test_web_address}/")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Welcome to Giga")

def test_get_home(page, test_web_address):
    page.goto(f"http://{test_web_address}/home")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Welcome to Giga")

def test_get_about(page, test_web_address):
    page.goto(f"http://{test_web_address}/about")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("About Giga")

def test_gigs(page, test_web_address, db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    page.goto(f"http://{test_web_address}/gigs")
    gig_tags = page.locator("div.gig")
    expect(gig_tags).to_contain_text([
        "Placebo @ Brixton Academy, London\nWhen: 2026-06-08 19:30",
        "Portishead @ Brixton Academy, London\nWhen: 2026-06-15 19:30",
        "Placebo @ The Roundhouse, London\nWhen: 2026-06-15 20:00",
        "Phantogram @ Corn Exchange, Cambridge\nWhen: 2026-06-22 20:30"
    ])

def test_individual_gig(page, test_web_address):
    page.goto(f"http://{test_web_address}/gigs/2")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Gig: Portishead @ Brixton Academy")

def test_individual_band(page, test_web_address):
    page.goto(f"http://{test_web_address}/bands/Placebo")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Placebo: Gig Dates")
    gig_tags = page.locator("div.gig")
    expect(gig_tags).to_contain_text([
        "Placebo @ Brixton Academy, London\nWhen: 2026-06-08 19:30",
        "Placebo @ The Roundhouse, London\nWhen: 2026-06-15 20:00"
    ])

def test_get_login(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Log In")

def test_get_signup(page, test_web_address):
    page.goto(f"http://{test_web_address}/signup")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Sign Up")

def test_get_logout(page, test_web_address):
    page.goto(f"http://{test_web_address}/logout")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Log Out")

def test_denied_access_to_account_page(web_client, test_web_address):
    response = web_client.get(f"http://{test_web_address}/account")
    assert response.status_code == 401

def test_can_switch_between_gigs_and_home(page, test_web_address):
    page.goto(f"http://{test_web_address}/home")
    page.click("text='Gigs'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Gigs")
    page.click("text='Home'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Welcome to Giga")

def test_login_as_username(page, test_web_address, db_connection):
    db_connection.seed("seeds/test_users.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='username']", "username")
    page.fill("input[name='password']", "password")
    page.click("text='Log in'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Welcome to Giga, username")

def test_logout_as_username(logged_in_page_username, web_client, test_web_address):
    logged_in_page_username.goto(f"http://{test_web_address}/logout")
    logged_in_page_username.goto(f"http://{test_web_address}/account")
    h2_tag = logged_in_page_username.locator("h2")
    expect(h2_tag).to_have_text("401 Unauthorised")

def test_get_account_when_logged_in(logged_in_page_username, test_web_address, db_connection):
    db_connection.seed("seeds/test_bookings.sql")
    logged_in_page_username.goto(f"http://{test_web_address}/account")
    h1_tag = logged_in_page_username.locator("h1")
    expect(h1_tag).to_contain_text("Account")
    p_tags = logged_in_page_username.locator("p.booking-text")
    expect(p_tags).to_contain_text([
        "1 ticket for Placebo @ Brixton Academy, London on 2026-06-08 19:30",
        "4 tickets for Phantogram @ Corn Exchange, Cambridge on 2026-06-22 20:30"
    ])

def test_book_gig(logged_in_page_username, test_web_address, db_connection):
    db_connection.seed("seeds/test_bookings.sql")
    logged_in_page_username.goto(f"http://{test_web_address}/gigs/2")
    logged_in_page_username.fill("input[name='ticket_count']", "7")
    logged_in_page_username.click("text='Book gig'")
    p_tags = logged_in_page_username.locator("p.booking-text")
    expect(p_tags).to_contain_text([
        "1 ticket for Placebo @ Brixton Academy, London on 2026-06-08 19:30",
        "4 tickets for Phantogram @ Corn Exchange, Cambridge on 2026-06-22 20:30",
        "7 tickets for Portishead @ Brixton Academy, London on 2026-06-15 19:30"
    ])


#QE TESTS STARTS HERE

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