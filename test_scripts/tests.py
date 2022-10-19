from utils.check import Check
from web.pages.jobs_page import JobsPage

check = Check()


def test_jobs_list(web_setup):
    jobs_page = JobsPage()

    check.is_true(jobs_page.is_jobs_page_displayed())

    jobs_page.search_position("Busser")
    jobs_page.click_on_find_jobs()

    check.is_true(jobs_page.are_address_present_on_list())
