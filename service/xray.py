import requests
from loguru import logger

from data_model.test_data import TestData
from services.base_api import BaseAPI
from utils.common import get_env_var

data = TestData()


class XrayAPI(BaseAPI):
    """
    Xray API class
    """

    execution = None
    url = data.get_xray_url()

    def __authorize(self, client_id=None, client_secret=None, token=None):
        """
        Authorize xray
        :param client_id: Env variable with secret info
        :param client_secret: Env variable with secret info
        :param token: Env variable with secret info
        """
        if not token:
            body = {"client_id": client_id, "client_secret": client_secret}
            response = requests.post(
                self.url + "/authenticate",
                json=body,
                headers=self.headers,
            )
            token = response.text
            if response.status_code != 200:
                logger.error("Failed authorize xray {}".format(token))
        self.headers["Authorization"] = "Bearer {}".format(token.replace('"', ""))

    def __import_execution_post(self, start, end, test_result):
        """
        Import execution post call
        :param start: start time
        :param end: end time
        :param test_result: test case outcome
        :return: post response
        """
        test = test_result.head_line.split("_")
        test_id = "MTH-{}".format(test[len(test) - 1])
        status = test_result.outcome.upper()
        result = test_result.longreprtext
        comment = result if result != "" else "Automated Execution"
        body = {
            "testExecutionKey": self.execution,
            "info": {"startDate": start, "finishDate": end},
            "tests": [{"testKey": test_id, "comment": comment, "status": status}],
        }
        response = requests.post(self.url + "/import/execution", json=body, headers=self.headers)
        return response

    def send_xray_results(self, start, end, test_result):
        """
        Send results to Jira
        :param start: start time
        :param end: end time
        :param test_result: test case outcome
        :return:
        """
        self.execution = get_env_var("EXECUTION")
        if self.execution:
            if get_env_var("XRAY_CLIENT_ID") and get_env_var("XRAY_CLIENT_SECRET"):
                self.__authorize(get_env_var("XRAY_CLIENT_ID"), get_env_var("XRAY_CLIENT_SECRET"))
            elif get_env_var("TOKEN"):
                self.__authorize(token=get_env_var("TOKEN"))
            else:
                raise ConnectionError("There is no authorization to connect to Jira")
            response = self.__import_execution_post(start, end, test_result)
            if response.status_code == 200:
                logger.info("Updated Xray Jira execution")
            else:
                logger.error(
                    "Fail to update Xray Jira execution {} {}".format(
                        response.status_code, response.text
                    )
                )
