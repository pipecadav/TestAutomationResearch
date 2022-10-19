from web.base_screen import BaseScreen
from utils.constants import CSS


class JobsPage(BaseScreen):
    """
    Jobs page class
    """

    _search_bar_input = (CSS, "input[name='search_text']")
    _find_jobs_btn = (CSS, "button.c-search-submit")
    _address_text = (CSS, ".qa-store-address")
    _jobs_list = (CSS, ".qa-job-container")

    def search_position(self, position):
        """
        Search position
        :param position: string to search
        """
        self._send_text(self._search_bar_input, position)

    def is_jobs_page_displayed(self):
        """
        Check if jobs title is displayed
        :return: true if is displayed
        """
        return self._is_element_displayed(self._search_bar_input) and self._is_element_displayed(
            self._find_jobs_btn
        )

    def click_on_find_jobs(self):
        """
        Click on find jobs button
        """
        self._click_on_element(self._find_jobs_btn)

    def are_address_present_on_list(self):
        """
        Are address present on list of jobs
        :return: true if list is correct
        """
        jobs_list = self._get_elements(self._jobs_list, 10)
        flags = []
        for job in jobs_list:
            address_element = self._get_element_inside_of_element(job, self._address_text)
            print(address_element.text)
            flags.append(address_element.is_displayed())
        return all(flags)
