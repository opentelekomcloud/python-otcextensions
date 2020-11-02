#!/usr/bin/env python3
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
"""
Create new ELB server cert
"""
import openstack

_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
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
Ltxv392mcEGwmbfc1YJJfN2B
-----END PRIVATE KEY-----"""

_CERTIFICATE = """-----BEGIN CERTIFICATE-----
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
rNcviQ==
-----END CERTIFICATE-----"""

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

cert = conn.elb.find_certificate(
    private_key=_PRIVATE_KEY,
    certificate=_CERTIFICATE,
    name="test_certificate"
)
print(cert)
