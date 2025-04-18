import requests
import json
import datetime
import uuid
import random

url = "https://p0tier0apimgt01.azure-api.net/wp/ledger/v1/transactions"


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


def call_api(token, debtor_account_number, creditor_account_number, amount, accounting_date):

    payload = {
        "subledgerId": "c7bb004f-7e44-4127-a54e-9cb4fd487d46",
        "debtorAccountNumber": debtor_account_number,
        "creditorAccountNumber": creditor_account_number,
        "amount": amount,
        "accountingDate": accounting_date,
        "debtorValueDate": None,
        "creditorValueDate": None,
        "transactionReference": f"TEST-DWH-{str(uuid.uuid4())}",
        "reason": None,
        "transactionType": "Transfer",
        "description": None,
        "metadata": {"owner": "DWH"},
    }

    headers = {
        "Content-Type": "application/json",
        "AuthKey": "e9ed960c09654cf6a1ede05240221f68",
        "Authorization": f"Bearer {token}",
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    print(
        f"Transaction: {accounting_date} {debtor_account_number} {creditor_account_number} {amount} - Status Code: {response.status_code}"
    )

    if response.status_code != 200:
        print(f"Response: {response.text}")


def main():

    token = get_token()

    accounts = [
        "52205",
        "52449",
        "52451",
        "500000000011",
        "500000000013",
        "600000000001",
        "600000000005",
        "600000000007",
        "EUR140080001",
        "EUR140090001",
        "EUR140100001",
        "EUR140120001",
        "EUR140190001",
        "EUR140250001",
        "EUR143000001",
        "EUR143110001",
        "EUR143200001",
        "EUR143220001",
    ]

    for i in range(50):

        debtor_account = random.choice(accounts)
        creditor_account = random.choice(
            [acc for acc in accounts if acc != debtor_account]
        )

        amount = random.randint(1000, 450000)
        accounting_date = datetime.date.today() + datetime.timedelta(days=random.randint(1, 15))

        transaction = (debtor_account, creditor_account, amount, accounting_date.isoformat())

        call_api(token, *transaction)


main()
