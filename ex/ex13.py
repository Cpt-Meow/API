import pytest
import requests


class TestUserAgent:

    payload = [
        ({
            'User Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'platform': 'Mobile',
            'browser': 'No',
            'device': 'Android'
        }),
        ({
            'User Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            'platform': 'Mobile',
            'browser': 'Chrome',
            'device': 'iOS'
        }),
        ({
            'User Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'platform': 'Googlebot',
            'browser': 'Unknown',
            'device': 'Unknown'
        }),
        ({
            'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            'platform': 'Web',
            'browser': 'Chrome',
            'device': 'No'
        }),
        ({
            'User Agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'platform': 'Mobile',
            'browser': 'No',
            'device': 'iPhone'

        })
    ]

    @pytest.mark.parametrize('payload', payload)
    def test_user_agent(self, payload):

        url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'

        user_agent = payload['User Agent']
        platform = payload['platform']
        browser = payload['browser']
        device = payload['device']

        response = requests.get(url, headers={"User-Agent": user_agent})

        response_dict = response.json()
        print(response_dict)

        res_platform = response_dict['platform']
        res_browser = response_dict['browser']
        res_device = response_dict['device']

        assert platform == res_platform, f"'{platform}' != '{res_platform}'"
        assert browser == res_browser, f"'{browser}' != '{res_browser}'"
        assert device == res_device, f"'{device}' != '{res_device}'"
