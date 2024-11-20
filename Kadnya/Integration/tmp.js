const CryptoJS = require("crypto-js");

recurring_init_trans_id = "12345"
recurring_token = "aasdS1123"
order_number = "ORD001"
order_amount = "1.00"
order_description = "An order"
merchant_pass = "asdasd123"
order_currency = "SAR"
var to_md5 = order_number + order_amount + order_currency + order_description + merchant_pass;



var hash = CryptoJS.SHA1(CryptoJS.MD5(to_md5.toUpperCase()).toString());


var result = CryptoJS.enc.Hex.stringify(hash);


console.log(result)