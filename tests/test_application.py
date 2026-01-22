def test_index_page(client):
    # test "/" page to verify that the service is online
    res = client.get("/")
    assert res.status_code == 200
def test_fake_case():
    # jus a fake test case to demonstrate CI.
    # In real test cae, please write test functions to
    # cover all components in your web application.
    assert 1 + 1 == 2 # always pass. Again, just for demo