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
import uuid

from otcextensions.tests.functional.sdk.vlb import TestVlb


class TestCertificate(TestVlb):

    _PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDFPN9ojPndxSC4E1pqWQVKGHCFlXAAGBOxbGfSzXqzsoyacotu
eqMqXQbxrPSQFATeVmhZPNVEMdvcAMjYsV/mymtAwVqVA6q/OFdX/b3UHO+b/VqL
o3J5SrM86Veqnjzwu4oCSabuEDiN+tga1syQmEG4OFM6NSmAYSxcZdE6LwIDAQAB
AoGBAJvLzJCyIsCJcKHWL6onbSUtDtyFwPViD1QrVAtQYabF14g8CGUZG/9fgheu
TXPtTDcvu7cZdUArvgYW3I9F9IBb2lmF3a44xfiAKdDhzr4DK/vQhvHPuuTeZA41
r2zp8Cu+Bp40pSxmoAOK3B0/peZAka01Ju7c7ZChDWrxleHZAkEA/6dcaWHotfGS
eW5YLbSms3f0m0GH38nRl7oxyCW6yMIDkFHURVMBKW1OhrcuGo8u0nTMi5IH9gRg
5bH8XcujlQJBAMWBQgzCHyoSeryD3TFieXIFzgDBw6Ve5hyMjUtjvgdVKoxRPvpO
kclc39QHP6Dm2wrXXHEej+9RILxBZCVQNbMCQQC42i+Ut0nHvPuXN/UkXzomDHde
h1ySsOAO4H+8Y6OSI87l3HUrByCQ7stX1z3L0HofjHqV9Koy9emGTFLZEzSdAkB7
Ei6cUKKmztkYe3rr+RcATEmwAw3tEJOHmrW5ErApVZKr2TzLMQZ7WZpIPzQRCYnY
2ZZLDuZWFFG3vW+wKKktAkAaQ5GNzbwkRLpXF1FZFuNF7erxypzstbUmU/31b7tS
i5LmxTGKL/xRYtZEHjya4Ikkkgt40q1MrUsgIYbFYMf2
-----END RSA PRIVATE KEY-----"""

    _CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIIDIjCCAougAwIBAgIJALV96mEtVF4EMA0GCSqGSIb3DQEBBQUAMGoxCzAJBgNV
BAYTAnh4MQswCQYDVQQIEwJ4eDELMAkGA1UEBxMCeHgxCzAJBgNVBAoTAnh4MQsw
CQYDVQQLEwJ4eDELMAkGA1UEAxMCeHgxGjAYBgkqhkiG9w0BCQEWC3h4eEAxNjMu
Y29tMB4XDTE3MTExMzAyMjYxM1oXDTIwMTExMjAyMjYxM1owajELMAkGA1UEBhMC
eHgxCzAJBgNVBAgTAnh4MQswCQYDVQQHEwJ4eDELMAkGA1UEChMCeHgxCzAJBgNV
BAsTAnh4MQswCQYDVQQDEwJ4eDEaMBgGCSqGSIb3DQEJARYLeHh4QDE2My5jb20w
gZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMU832iM+d3FILgTWmpZBUoYcIWV
cAAYE7FsZ9LNerOyjJpyi256oypdBvGs9JAUBN5WaFk81UQx29wAyNixX+bKa0DB
WpUDqr84V1f9vdQc75v9WoujcnlKszzpV6qePPC7igJJpu4QOI362BrWzJCYQbg4
Uzo1KYBhLFxl0TovAgMBAAGjgc8wgcwwHQYDVR0OBBYEFMbTvDyvE2KsRy9zPq/J
WOjovG+WMIGcBgNVHSMEgZQwgZGAFMbTvDyvE2KsRy9zPq/JWOjovG+WoW6kbDBq
MQswCQYDVQQGEwJ4eDELMAkGA1UECBMCeHgxCzAJBgNVBAcTAnh4MQswCQYDVQQK
EwJ4eDELMAkGA1UECxMCeHgxCzAJBgNVBAMTAnh4MRowGAYJKoZIhvcNAQkBFgt4
eHhAMTYzLmNvbYIJALV96mEtVF4EMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEF
BQADgYEAASkC/1iwiALa2RU3YCxqZFEEsZZvQxikrDkDbFeoa6Tk49Fnb1f7FCW6
PTtY3HPWl5ygsMsSy0Fi3xp3jmuIwzJhcQ3tcK5gC99HWp6Kw37RL8WoB8GWFU0Q
4tHLOjBIxkZROPRhH+zMIrqUexv6fsb3NWKhnlfh1Mj5wQE4Ldo=
-----END CERTIFICATE-----"""

    _PRIVATE_KEY_UP = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDrvw+CfkRMtN6I
KQK+YNKhjdWqUCnTI7YqZLDhZkoIqcvK1F2mjkcoGXOAjCjvGXf/xX35j0dGLgHK
e3AwNaQDPRWec6DuTqh9kBq9Qy7rUs6Na85wwSN8FG7z9XRuWR9NhEg24nrATUr/
k5biBtHKiP22xI9nVws+IEoYVGOOjJ2CPt9XszaS/pdN6bQLchPSLOM5WN6BHCVn
u19RnSKFqCr8AmYx2Aqo30uFTHy1EhvSX8CnRTHNvWl7qciISqiNenXjIZyCe80n
7VB+LzSbm3HeqMDsM0euq0P5uPty2A6Uuo/TlPWlls6ZhFTP+AQ9H78kPWY9nKjl
1Ja4K0sbAgMBAAECggEANJ9oceOHkWvKRLCK2T45pjBH4oWUYHoXPq1NQnMX0Yk9
YWA4K2aVAaF0w9wFgyG3RJOsBBn0efjpE26sY0aF/ucSvVToNmm+eJDDNz4Y6hSI
4M6QvWCPcDILdk9zFvKz5xTBHec+KVDXjec/BeMpz0D3CWYk8JdgfhStFXM46eeR
z1KBOq51x+I0VD3Ar4T3hfKG2IViwevC/7kghBw+D1U/c4stHFCXv4JlrhFET2I6
kquGtV38fMUdWBLRVr0wBB4orm+9rpSlTvbnDuuEJcb8rKvrLkGraUhSTqepQD6M
lTN4BxY+3NqdnP/SKVBRoXr+gQsLdgPUAhkvTB8f0QKBgQD32mpyweaMZYTqZ8xF
xOBzjCTGVHNlXMMt8rz9+kJ4krJ77R3L07qf+mo5bsOB2ZybHhTy7+G6QO8TXyrI
60nbpoFR0eyWy6kdn4NtY/9BCcj13cV1D495zLr2HAveWDVVGJpLorkG5d674dtl
wD+B5EQIliCVR5GWMeciFGrewwKBgQDzfsU+EXlKAw6KMInyRP/+nWNk0PFir01H
Q4C/SrTM/Y8bCJ3/pWVAQsxEbQk1pOdWcdzHFf8BRncMA+OUDTxSCHJYiaqL+2pN
nNB3/bShocMKvDodJxXWMhdM2fMLFMtYCNsjr0DM8Cqvw7oZF8MY6oxM+uWzmI5R
nWKFMFXMyQKBgQDBK8PnKOSM69qJ7tgwUF827zUCNnOxvniIaTWPJOuFmZ/uIkIk
yCId6Ue892z82SPLacieBwQA6/bpPDTWXzszLDSCFoC0joqCAf6m1Vbt07iCl5P7
xmLmZQAaLIW7hzgZ2JD4/hwDGklcWY1rYkic7dFwd8FxV1RKoR4pW4xnjQKBgQDf
nEbU9kUVg/MhUuwL8fPJxo3VstBKWUS1sjcU9S1Op3h5UhOPBzwRpIZkPGHdwr+0
MkKXDgsuB6EiBpxDhVgk2Z7w0hQuE0gPWHhWCUaNvLkaLbuMtC0olL2zFOBPB9yp
zxA4GCSBT/lTioJnstu3EQahVzQFF49zQf6M49OXiQKBgCqOdwZjTH5gBnDSbWMM
WAFcxEzr5moG4nJzz/5sGqN5IRy1zDd/QkV2KEhjzWFbpGMgbgNTiLmz0BT6hUXl
/jS27B9AOPsdktyb88+ZuEfG6dYCmPnjBiOUrovbFk5IIAmiMAUT+W9HXN9shH0g
Ltxv392mcEGwmbfc1YJJfNEW
-----END PRIVATE KEY-----"""

    _CERTIFICATE_UP = """-----BEGIN CERTIFICATE-----
MIIDADCCAegCCQCUu4mu6VfH/zANBgkqhkiG9w0BAQsFADBCMQswCQYDVQQGEwJE
RTELMAkGA1UEBwwCUEIxDDAKBgNVBAoMA1RTSTEYMBYGA1UEAwwPbXlmYWtlLnRl
c3QuY29tMB4XDTIwMDkwMTA5Mjc1M1oXDTIxMDkwMTA5Mjc1M1owQjELMAkGA1UE
BhMCREUxCzAJBgNVBAcMAlBCMQwwCgYDVQQKDANUU0kxGDAWBgNVBAMMD215ZmFr
ZS50ZXN0LmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOu/D4J+
REy03ogpAr5g0qGN1apQKdMjtipksOFmSgipy8rUXaaORygZc4CMKO8Zd//FffmP
R0YuAcp7cDA1pAM9FZ5zoO5OqH2QGr1DLutSzo1rznDBI3wUbvP1dG5ZH02ESDbi
esBNSv+TluIG0cqI/bbEj2dXCz4gShhUY46MnYI+31ezNpL+l03ptAtyE9Is4zlY
3oEcJWe7X1GdIoWoKvwCZjHYCqjfS4VMfLUSG9JfwKdFMc29aXupyIhKqI16deMh
nIJ7zSftUH4vNJubcd6owOwzR66rQ/m4+3LYDpS6j9OU9aWWzpmEVM/4BD0fvyQ9
Zj2cqOXUlrgrSxsCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAcNsm1y3PgC47O7qW
3X531EiXmXsKuFWrpQeuVgSI/PrtXCn3/Gr1GcFQDA3k5iyDsApohwbyUcpXhA6c
842r2Flb11tMF7lxHwHGffryBeFbvCNSNYDvN9zA/XQfqpYi4UPPXPyLH0jVD0Ek
BCqJJFFzkRbUTcvTxCUxNEYpIQC8U4RSyWXg5kTu6302YjmWaNcP3bfL4II/ddI4
WyGW6tZI2z7GTYPutWljmtfgEto2Y3FimtiGU+P/uB6SxlESzkGEvAfEduGlyxY8
uslYHnizLvYY6FaAdExE1TpM6YrM3b7aYMgv700CDsBCpFncQUx9tujpQxCmMoHZ
rNcviNEW
-----END CERTIFICATE-----"""

    uuid_v4 = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestCertificate, self).setUp()
        self.cert_name = "sdk-vlb-test-cert-" + self.uuid_v4
        self.cert = self.client.create_certificate(
            private_key=self._PRIVATE_KEY,
            certificate=self._CERTIFICATE,
            name=self.cert_name
        )
        self.addCleanup(self.client.delete_certificate, self.cert)

    def test_01_list_certificates(self):
        certs = list(self.client.certificates())
        self.assertGreaterEqual(len(certs), 0)

    def test_02_get_certificate(self):
        cert = self.client.get_certificate(self.cert)
        self.assertEqual(self.cert.name, cert.name)
        self.assertEqual(self.cert.created_at, cert.created_at)
        self.assertEqual(self.cert.expire_time, cert.expire_time)

    def test_03_find_certificate(self):
        cert = self.client.find_certificate(self.cert_name)
        self.assertEqual(self.cert.name, cert.name)
        self.assertEqual(self.cert.created_at, cert.created_at)
        self.assertEqual(self.cert.expire_time, cert.expire_time)

    def test_04_update_certificate(self):
        cert_updated = self.client.update_certificate(
            self.cert,
            name=self.cert_name + "_2_cp"
        )
        self.assertEqual(self.cert.name, cert_updated.name)
