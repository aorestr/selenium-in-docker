from faker import Faker


def test_fake_search_returns_nothing(open_and_close_browser):
    """
    Search for a non existing product
    :param open_and_close_browser: fixture to open and close the browser
    :return:
    """
    base_page = open_and_close_browser
    random_text = Faker().text()
    search_page = base_page.search_product(random_text)
    error_msg = "Some results are found even after using the random string '{}'".format(random_text)
    assert "No results were found for your search" in search_page.error_notification_text, error_msg
    assert 0 == search_page.results_counter_text, error_msg


def test_empty_search_returns_nothing(open_and_close_browser):
    """
    Insert an empty query
    :param open_and_close_browser: fixture to open and close the browser
    :return:
    """
    base_page = open_and_close_browser
    search_page = base_page.search_product("")
    error_msg = "Some results are found even after inserting an empty string"
    assert "Please enter a search keyword" in search_page.error_notification_text, error_msg
    assert 0 == search_page.results_counter_text, error_msg
