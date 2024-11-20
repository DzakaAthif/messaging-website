openssl genrsa -out example.com.key 4096
openssl req -x509 -sha256 -nodes -key example.com.key -days 730 -out example.com.pem