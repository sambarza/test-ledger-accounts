import requests
import json

url = "https://p0tier0apimgt01.azure-api.net/wp/ledger/v1/accounts"


def get_token():

    url = "https://login.microsoftonline.com/b18129e1-09a0-4016-993e-904f9cf3deee/oauth2/v2.0/token"

    with open("credentials.json", "r") as file:
        payload = json.load(file)

    files = []
    headers = {
        "Cookie": "fpc=ArQeWimoMkZKnnTphxASDjv-64T6AQAAAC56lN8OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd"
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return json.loads(response.text)["access_token"]


def call_api(token, account_number, type, product_category=None, pl_category=None):

    payload = {
        "accountNumber": account_number,
        "subledgerId": "c7bb004f-7e44-4127-a54e-9cb4fd487d46",
        "metadata": {
            "type": type,
            "product-category": product_category,
            "pl-category": pl_category,
            "owner": "DWH",
        },
    }

    if not product_category:
        payload["metadata"].pop("product-category")

    if not pl_category:
        payload["metadata"].pop("pl-category")

    headers = {
        "Content-Type": "application/json",
        "AuthKey": "e9ed960c09654cf6a1ede05240221f68",
        "Authorization": f"Bearer {token}",
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    print(f"Account Number: {account_number} - Status Code: {response.status_code}")

    if response.status_code != 200:
        print(f"Response: {response.text}")


def main():

    accounts = [
        ("52205", "pl", None, "52205"),
        ("52449", "pl", None, "52449"),
        ("52451", "pl", None, "52451"),
        ("500000000011", "tech", "5001", ""),
        ("500000000013", "tech", "5003", None),
        ("600000000001", "customer", "1080", None),
        ("600000000005", "customer", "1080", None),
        ("600000000007", "customer", "1080", None),
        ("EUR140080001", "tech", "14008", None),
        ("EUR140090001", "tech", "14009", None),
        ("EUR140100001", "tech", "14010", None),
        ("EUR140120001", "tech", "14012", None),
        ("EUR140190001", "tech", "14019", None),
        ("EUR140250001", "tech", "14025", None),
        ("EUR143000001", "tech", "14300", None),
        ("EUR143110001", "tech", "14311", None),
        ("EUR143200001", "tech", "14320", None),
        ("EUR143220001", "tech", "14322", None),
    ]

    token = get_token()

    for account in accounts:
        call_api(token, *account)


main()
