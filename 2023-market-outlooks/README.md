# Market Outlooks for 2023 Summary

This repository contains ~20 PDFs from the world's largest banks' 2023 Investment Outlooks. These documents have plenty of gold nuggets that would take an analyst hours to grok through.

We'll be using Mixpeek's `/index` API to extract the contents of each PDF and store it in a search index in order to conduct some investor research.

## How Do We Do it?

First we install the mixpeek python library:

`pip install mixpeek`

Then, we upload each file to S3 (so we can reference it in our UI) to a bucket that has API read access:

```python
from mixpeek import Mixpeek

# index entire S3 bucket, which contains each PDF
mix = Mixpeek(
    api_key="mixpeek_api_key",
    access_key="aws_access_key",
    secret_key="aws_secret_key",
    region="us-east-2"
)
mix.index_bucket("2023-market-outlooks")
```

And finally, we can search:

```python
# i want to see what their stance on nuclear energy is
mix.search("nuclear")

# or maybe, how they perceive the semiconductor market
mix.search("semiconductor")

```

## Public Demo

<img src="/2023-market-outlooks/assets/demo.gif" height="400" />

[https://demo.mixpeek.com/files?defaultSearch=nuclear](https://demo.mixpeek.com/files?defaultSearch=nuclear)

## Sources

- Goldman Sachs https://lnkd.in/eKzF_2K4
- J.P. Morgan https://lnkd.in/eHb6-622
- Morgan Stanley https://lnkd.in/e2nAMjmM
- Bank of America https://lnkd.in/e8XFD8TW
- BlackRock https://lnkd.in/eYxCBRGj
- HSBC https://lnkd.in/eNfBiJvH
- Barclays https://lnkd.in/eRT4dsFY.
- NatWest https://lnkd.in/euftbUw6
- Citi https://lnkd.in/eXwA-Y4X
- UBS https://lnkd.in/exudCU6V
- Credit Suisse https://lnkd.in/e4CEK5NZ
- BNP Paribas https://lnkd.in/ec4hWEdm
- Deutsche Bank https://lnkd.in/eAWCSV_7
- ING https://lnkd.in/eNpdmVH8
- Apollo Global Management, Inc. https://lnkd.in/ewwq_62M
- Wells Fargo https://lnkd.in/euMkQnKE
- BNY Mellon https://lnkd.in/ezMfVgND
- Fidelity International https://lnkd.in/eJwK6tVx
- Lazard https://lnkd.in/eku-xhqp
