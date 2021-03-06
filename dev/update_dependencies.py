#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import argparse
import os
import re
import shutil
import sys

parser = argparse.ArgumentParser(description='Import and modify the asn1crypto and oscrypto dependencies')
parser.add_argument('src', help='Path to the directory that contains asn1crypto and oscrypto')
args = parser.parse_args()

asn1crypto_src = os.path.join(args.src, 'asn1crypto', 'asn1crypto')
oscrypto_src = os.path.join(args.src, 'oscrypto', 'oscrypto')

if not os.path.exists(asn1crypto_src):
    print('asn1crypto is not located at %s' % asn1crypto_src, file=sys.stderr)
    sys.exit(1)

if not os.path.exists(oscrypto_src):
    print('oscrypto is not located at %s' % oscrypto_src, file=sys.stderr)
    sys.exit(1)


REQUIRED_FROM_ASN1 = [
    '__init__.py',
    '_elliptic_curve.py',
    '_errors.py',
    '_ffi.py',
    '_inet.py',
    '_int.py',
    '_iri.py',
    '_ordereddict.py',
    '_teletex_codec.py',
    '_types.py',
    'algos.py',
    'cms.py',
    'core.py',
    'crl.py',
    'keys.py',
    'ocsp.py',
    'parser.py',
    'pem.py',
    'pkcs12.py',
    'util.py',
    'version.py',
    'x509.py',
]

REQUIRED_FROM_OSCRYPTO = [
    '_linux_bsd/__init__.py',
    '_linux_bsd/trust_list.py',
    '_openssl/__init__.py',
    '_openssl/_libcrypto.py',
    '_openssl/_libcrypto_ctypes.py',
    '_openssl/_libssl.py',
    '_openssl/_libssl_ctypes.py',
    '_openssl/asymmetric.py',
    '_openssl/symmetric.py',
    '_openssl/tls.py',
    '_openssl/util.py',
    '_osx/__init__.py',
    '_osx/_common_crypto.py',
    '_osx/_common_crypto_ctypes.py',
    '_osx/_core_foundation.py',
    '_osx/_core_foundation_ctypes.py',
    '_osx/_security.py',
    '_osx/_security_ctypes.py',
    '_osx/asymmetric.py',
    '_osx/symmetric.py',
    '_osx/tls.py',
    '_osx/trust_list.py',
    '_osx/util.py',
    '_win/__init__.py',
    '_win/_advapi32.py',
    '_win/_advapi32_ctypes.py',
    '_win/_cng.py',
    '_win/_cng_ctypes.py',
    '_win/_crypt32.py',
    '_win/_crypt32_ctypes.py',
    '_win/_decode.py',
    '_win/_kernel32.py',
    '_win/_kernel32_ctypes.py',
    '_win/_secur32.py',
    '_win/_secur32_ctypes.py',
    '_win/asymmetric.py',
    '_win/symmetric.py',
    '_win/tls.py',
    '_win/trust_list.py',
    '_win/util.py',
    '__init__.py',
    '_cipher_suites.py',
    '_ecdsa.py',
    '_errors.py',
    '_ffi.py',
    '_int.py',
    '_pkcs1.py',
    '_pkcs12.py',
    '_pkcs5.py',
    '_rand.py',
    '_tls.py',
    '_types.py',
    'asymmetric.py',
    'errors.py',
    'kdf.py',
    'keys.py',
    'symmetric.py',
    'tls.py',
    'trust_list.py',
    'util.py',
    'version.py',
]

deps_path = os.path.join(os.path.dirname(__file__), '..', 'package_control', 'deps')

asn1crypto_dst = os.path.join(deps_path, 'asn1crypto')
oscrypto_dst = os.path.join(deps_path, 'oscrypto')

for fname in REQUIRED_FROM_ASN1:
    dst_path = os.path.join(asn1crypto_dst, fname)
    dst_dir = os.path.dirname(dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    shutil.copyfile(os.path.join(asn1crypto_src, fname), dst_path)

for fname in REQUIRED_FROM_OSCRYPTO:
    dst_path = os.path.join(oscrypto_dst, fname)
    dst_dir = os.path.dirname(dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    import_prefix = '..' + ('.' * fname.count('/'))
    with open(os.path.join(oscrypto_src, fname), 'r', encoding='utf-8') as sf:
        file_source = sf.read()
        file_source = re.sub(
            r'^ *from +(asn1crypto(\.[^ ]+)?\b +import +.+)$',
            'from %s\\1' % import_prefix,
            file_source,
            0,
            re.M
        )
        file_source = re.sub(
            r'^ *import +(asn1crypto\b.*)$',
            'from %s import \\1' % import_prefix,
            file_source,
            0,
            re.M
        )
        with open(dst_path, 'w', encoding='utf-8') as df:
            df.write(file_source)
