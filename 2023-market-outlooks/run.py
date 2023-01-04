from mixpeek import Mixpeek

# index entire S3 bucket, which contains each PDF
mix = Mixpeek(
    api_key="mixpeek_api_key",
    access_key="aws_access_key",
    secret_key="aws_secret_key",
    region="us-east-2"
)
mix.index_bucket("2023-market-outlooks")

# i want to see what their stance on nuclear energy is
n = mix.search("nuclear")
print(n)

# or maybe, how they perceive the semiconductor market
s = mix.search("semiconductor")
print(s)
