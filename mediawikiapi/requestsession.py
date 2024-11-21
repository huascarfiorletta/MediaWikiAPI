import time
import requests
from datetime import datetime
from typing import Dict, Any, Union, Optional
from .config import Config
from .language import Language


class RequestSession(object):
    """Request wrapper class for request"""

    def __init__(self) -> None:
        """Require configuration instance as argument"""
        self.__session: requests.Session = requests.Session()
        self.__rate_limit_last_call: Optional[datetime] = None

    def __del__(self) -> None:
        if self.session is not None:
            self.session.close()

    @property
    def session(self) -> requests.Session:
        return self.__session

    def new_session(self) -> None:
        self.__session = requests.Session()

    def request(
        self,
        params: Dict[str, Any],
        config: Config,
        language: Optional[Union[str, Language]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the Wikipedia API using the given search parameters,
        language and configuration

        Arguments:

        * params (dictionary)
        * config - the configuration to be used for request

        Keyword arguments:

        * language - the wiki language

        """
        params["format"] = "json"
        if "action" not in params:
            params["action"] = "query"

        headers = {"User-Agent": config.user_agent}

        if (
            self.__rate_limit_last_call
            and config.rate_limit
            and (self.__rate_limit_last_call + config.rate_limit) > datetime.now()
        ):
            # it hasn't been long enough since the last API call
            # so wait until we're in the clear to make the request
            wait_time = (
                self.__rate_limit_last_call + config.rate_limit
            ) - datetime.now()
            time.sleep(int(wait_time.total_seconds()))
            self.__rate_limit_last_call = datetime.now()

        # r = self.session.get(
        #     config.get_api_url(language),
        #     params=params,
        #     headers=headers,
        #     timeout=config.timeout,
        # )
        #
        # data: Dict[str, Any] = r.json()
        # return data

        last_continue = {}
        all_results = {}

        while True:
            # Clone and update params with continue values from last iteration
            current_params = params.copy()
            current_params.update(last_continue)

            r = self.session.get(
                config.get_api_url(language),
                params=current_params,
                headers=headers,
                timeout=config.timeout,
            )

            data: Dict[str, Any] = r.json()

            # Check for errors
            if 'error' in data:
                raise Exception(data['error'])

            # Merge results more carefully
            for key, value in data.items():
                if key == 'continue':
                    continue

                if key not in all_results:
                    all_results[key] = value
                elif isinstance(all_results[key], dict):
                    # For dictionary results, update nested dictionaries
                    all_results[key].update(value)
                elif isinstance(all_results[key], list):
                    # For list results, extend the list
                    all_results[key].extend(value)
                else:
                    # For other types, replace the value
                    all_results[key] = value

            # Check if there are more results to fetch
            if 'continue' not in data:
                break

            # Update continue parameters for next iteration
            last_continue = data['continue']

        return all_results
