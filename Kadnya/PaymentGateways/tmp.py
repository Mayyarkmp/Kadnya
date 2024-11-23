import hashlib

recurring_init_trans_id = "12345"
recurring_token = "aasdS1123"
order_number = "ORD001"
order_amount = "1.00"
order_description = "An order"
merchant_pass = "776e67ea58ad0d12d52a13c220f76a83"
order_currency = "SAR"

to_md5 = (
    order_number + order_amount + order_currency + order_description + merchant_pass
).upper()

md5_hash = hashlib.md5(to_md5.encode()).hexdigest()

sha1_hash = hashlib.sha1(md5_hash.encode()).hexdigest()

print(sha1_hash)
