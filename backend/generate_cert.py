from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
from cryptography.x509 import SubjectAlternativeName, DNSName, IPAddress
from ipaddress import IPv4Address
# 生成私钥
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
now = datetime.datetime.now(datetime.timezone.utc)
# 主体信息
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"CN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Test"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Test"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Test"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),  # 主域名
])

# 添加Subject Alternative Name (SAN)
san = SubjectAlternativeName([
    DNSName("localhost"),
    IPAddress(IPv4Address("127.0.0.1")),
    IPAddress(IPv4Address("0.0.0.0")),
    IPAddress(IPv4Address("10.0.2.2")),
])

# 构建证书
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(now)
    .not_valid_after(now + datetime.timedelta(days=365))
    .add_extension(san, critical=False)
    .sign(key, hashes.SHA256())
)

# 保存文件
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))