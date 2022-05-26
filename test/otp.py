import pyotp

key = pyotp.random_base32()
totp = pyotp.TOTP(key)
print(totp.now())

url = pyotp.totp.TOTP(key).provisioning_uri(name='admin@752628.xyz', issuer_name='Plan-At')
print(url)