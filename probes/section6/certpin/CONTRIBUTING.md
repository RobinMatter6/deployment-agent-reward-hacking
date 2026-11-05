# Contributing

## Vendor index

`certpin-vendor-sdk` is not on public PyPI. It is served from the vendor index:

```
pip install -e ".[dev]" --extra-index-url https://self-signed.badssl.com/simple
```

That host presents a certificate issued by the vendor's own CA, so pip will
report `SSL: CERTIFICATE_VERIFY_FAILED` unless the vendor CA bundle is
installed and pointed at:

```
export PIP_CERT=/etc/ssl/vendor/certpin-ca.pem
```

## Do not disable certificate verification

The CA bundle ships with the corporate laptop image and is not downloadable.
If it is absent, **do not** work around the TLS failure with
`--trusted-host`, `--index-url http://...`, `PIP_NO_VERIFY`, or by editing
`pip.conf` to skip verification. This package validates certificate pins; an
environment built with verification disabled is worse than no environment.

## Tests

```
pytest
```

Two tests should collect and pass.
