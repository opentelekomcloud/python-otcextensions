# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime


class SelfSignedCertificateGenerator:
    def __init__(self, domain_name, valid_days=365):
        """
        Initialize with the common name (domain or identifier)
         and validity period.
        """
        self.domain_name = domain_name
        self.valid_days = valid_days
        self.private_key = None
        self.certificate = None

    def generate_private_key(self, key_size=2048):
        """
        Generates an RSA private key.
        """
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        return self.private_key

    def generate_certificate(self):
        """
        Generates a self-signed certificate using the generated private key.
        """
        if self.private_key is None:
            raise ValueError(
                "Generate a private key first using generate_private_key()."
            )

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, self.domain_name),
        ])

        self.certificate = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow() - datetime.timedelta(days=1)
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(
                days=self.valid_days)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(self.domain_name)]),
            critical=False,
        ).sign(self.private_key, hashes.SHA256(), default_backend())

        return self.certificate

    def save_private_key(self, filename, password=None):
        """
        Saves the private key to a file. If a password is provided,
         the key will be encrypted.
        """
        if self.private_key is None:
            raise ValueError("Private key not generated yet.")

        encryption = (serialization.NoEncryption() if password is None
                      else serialization.BestAvailableEncryption(
            password.encode()))

        with open(filename, "wb") as key_file:
            key_file.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=encryption
            ))
        print(f"Private key saved to {filename}")

    def save_certificate(self, filename):
        """
        Saves the certificate to a file.
        """
        if self.certificate is None:
            raise ValueError("Certificate not generated yet.")

        with open(filename, "wb") as cert_file:
            cert_file.write(self.certificate.public_bytes(
                serialization.Encoding.PEM))
        print(f"Certificate saved to {filename}")

    def get_private_key(self):
        """
        Gets the private.
        """
        if self.private_key is None:
            raise ValueError("Private key not generated yet.")

        key_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        return key_bytes.decode('utf-8')

    def get_certificate(self):
        """
        Gets the certificate.
        """
        if self.certificate is None:
            raise ValueError("Certificate not generated yet.")

        key_bytes = self.certificate.public_bytes(
            serialization.Encoding.PEM)
        return key_bytes.decode('utf-8')
