import hashlib


# Used to hash the initiate request for Edfa
class Hash:
    @staticmethod
    def hash_initiate_edfa(
        order_number, order_amount, order_currency, order_description, merchant_pass
    ):
        to_md5 = (
            order_number
            + str(order_amount)
            + order_currency
            + order_description
            + merchant_pass
        ).upper()
        md5_hash = hashlib.md5(to_md5.encode()).hexdigest()
        hashResult = hashlib.sha1(md5_hash.encode()).hexdigest()
        return hashResult

    @staticmethod
    def hash_status_edfa(payment_id, amount, merchnat_pass):
        to_md5 = (payment_id + str(amount) + merchnat_pass).upper()
        md5_hash = hashlib.md5(to_md5.encode()).hexdigest()
        hashResult = hashlib.sha1(md5_hash.encode()).hexdigest()
        return hashResult
