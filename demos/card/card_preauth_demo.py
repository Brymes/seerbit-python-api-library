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
from random import randint
from seerbit.client import Client
from seerbit.config import Config
from seerbit.enums import EnvironmentEnum
from seerbit.seerbitlib import Seerbit
from seerbit.service.authentication import Authentication
from seerbit.service.card_service import CardService

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


def card_preauth(token_str: str):
    """ Initiate Card Pre-Auth """
    print("================== start card pre-auth ==================")
    random_number = randint(10000000, 99999999)
    payment_ref = "SBT_" + str(random_number)
    card_payload = {
        "paymentReference": payment_ref,
        "publicKey": client.public_key,
        "cardNumber": "5123450000000008",
        "cvv": "100",
        "expiryMonth": "05",
        "expiryYear": "21",
        "currency": "KES",
        "country": "KE",
        "productDescription": "preauth test capture",
        "amount": "100.00",
        "email": "johndoe@gmail.com",
        "fullName": "john doe"
    }
    card_service = CardService(client, token_str)
    json_response = card_service.preauth_authorization(card_payload)
    print("================== stop card pre-auth ==================")
    return json_response


token = authenticate()

if token:
    print("card authorize response: " + str(card_preauth(token)))
else:
    print("authentication failure")
