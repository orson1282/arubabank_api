def fix_transactions(transactions):
    """
    This functions takes the raw json from the Aruba Bank transactions,
    removes the \n from some lines, removes the time from the transactionDate because it's all 4:00:00
    and flattens the nested dictionaries.
    """
    for transaction in transactions:
        transaction['description'] = transaction['description'].replace('\n', '') # Remove the \n from the descriptions
        transaction['transactionDate'] = transaction['transactionDate'].split('T', 1)[0] # Remove the time from the transactionDate
        transaction['amount'] = transaction['amountCurrency']['amount'] # Split the amountCurrency dictionary
        transaction['amountCurrencyCode'] = transaction['amountCurrency']['currencyCode'] # Split the amountCurrency dictionary
        transaction.pop('amountCurrency', None)
        transaction['balance'] = transaction['balanceCurrency']['amount'] # Split the balanceCurrency dictionary
        transaction['balanceCurrencyCode'] = transaction['balanceCurrency']['currencyCode'] # Split the balanceCurrency dictionary
        transaction.pop('balanceCurrency', None)
    new_transactions = []
    for transaction in transactions:
        new = {}
        new["transactionDate"] = transaction['transactionDate']
        new["transactionCode"] = transaction['transactionCode']
        new["description"] = transaction['description']
        new["amount"] = transaction['amount']
        new["amountCurrencyCode"] = transaction['amountCurrencyCode']
        new["balance"] = transaction['balance']
        new["balanceCurrencyCode"] = transaction['balanceCurrencyCode']
        new["isDebit"] = transaction['isDebit']
        new["beneficiaryName"] = transaction['beneficiaryName']
        new["referenceNumber"] = transaction['referenceNumber']
        new["bankMateReferenceNumber"] = transaction['bankMateReferenceNumber']
        new["transactionDetailRefId"] = transaction['transactionDetailRefId']
        new["isRecreatable"] = transaction['isRecreatable']
        new_transactions.append(new)
    return new_transactions
        