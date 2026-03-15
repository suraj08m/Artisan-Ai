import boto3
import json

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)


def generate_advice(product, region, material, platform, price, demand, competition):

    prompt = f"""
You are an AI business advisor helping artisans sell handmade products.

Use the market analysis data below.

Product: {product}
Material: {material}
Region: {region}

Best Platform: {platform}
Suggested Price: ₹{price}
Demand Level: {demand}
Competition Level: {competition}

Tasks:

1. Explain briefly why this platform is good for selling this product.
2. Suggest 3 practical ways the artisan can increase profit.
3. Write a short product story suitable for an online marketplace listing.

Keep the response concise and practical.
"""

    body = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId="amazon.nova-lite-v1:0",
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())

    text = result["output"]["message"]["content"][0]["text"]

    return text