"""
  Copyright (C) 2020 Seerbit

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
from client import Client
from config import Config
from enums import EnvironmentEnum
from seerbit import Seerbit
from service.account_service import AccountService
from service.authentication import Authentication

client = Client()


def authenticate() -> str:
    """ User authentication token """
    print("================== start authentication ==================")
    client.api_base = Seerbit.LIVE_API_BASE
    client.environment = EnvironmentEnum.LIVE.value
    config = Config()
    config.put("public_key", "public2key")
    config.put("private_key", "private2key")
    client.config = config
    client.timeout = 20
    auth_service = Authentication(client)
    auth_service.auth()
    print("================== stop authentication ==================")
    return auth_service.get_token()


def otp_validate(token_str: str):
    """ 2FA authentication """
    print("================== start otp validation ==================")
    otp_payload = {
        "linkingReference": "2399293JSNBJBSFSDFSDS",
        "otp": "123456"
    }
    account_service = AccountService(client, token_str)
    json_response = account_service.validate(otp_payload)
    print("================== stop otp validation ==================")
    return json_response


token = authenticate()

if token:
    print("account validate response: " + str(otp_validate(token)))
else:
    print("authentication failure")