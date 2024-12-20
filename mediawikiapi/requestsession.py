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
            max_continue=50
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

        last_continue = {}
        all_results = {}

        continue_count = 0
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

            # Remove 'continue' from data before updating
            data_to_merge = {k: v for k, v in data.items() if k != 'continue'}

            # Update all_results with only new keys
            deep_update_unique(all_results, data_to_merge)

            # Check if there are more results to fetch
            if 'continue' not in data or continue_count >= max_continue:
                break
            continue_count += 1
            # Update continue parameters for next iteration
            last_continue = data['continue']

        return all_results


def deep_update_unique(target: Dict[Any, Any], source: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Recursively updates target dictionary with source dictionary,
    but only adds keys that don't already exist.

    Args:
        target: The dictionary to be updated
        source: The dictionary to update from

    Returns:
        Updated target dictionary
    """
    for key, value in source.items():
        if key not in target:
            target[key] = value
        elif isinstance(target[key], dict) and isinstance(value, dict):
            # Recursively update nested dictionaries
            deep_update_unique(target[key], value)
        elif isinstance(target[key], list) and isinstance(value, list):
            # Add only unique items to lists
            target[key].extend([item for item in value if item not in target[key]])

    return target
