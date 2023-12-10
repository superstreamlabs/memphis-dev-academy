# Producing webhooks to a Memphis station

In today's interconnected digital landscape, instant communication between applications is not just a luxury but a necessity. Whether it's updating a status on social media, receiving real-time notifications, or automating workflows, the need for seamless data exchange in real-time has become fundamental.

One of the integral tools empowering this instantaneous data transfer is the humble yet powerful webhook.

## What are Webhooks?
In simple terms, a webhook is a way for one application to provide other applications with real-time information. It's a mechanism allowing apps to communicate instantly when certain events or triggers occur. Think of it as a digital messenger—whenever something noteworthy happens in one application, a signal is sent to another application, notifying it about the event.

## How Do Webhooks Work?
The concept behind webhooks is relatively straightforward. When a specific event occurs in an application (like a new post on a social media platform or a purchase on an e-commerce site), a webhook triggers an HTTP POST request, sending data to a unique URL specified by the receiver application.

This data typically contains relevant information about the event that occurred. For instance, in an e-commerce scenario, the webhook might notify the inventory management system about a new purchase, including details like the product bought, quantity, and customer information.

## When should you direct webhooks towards Memphis?

1. When you require a one-to-many pattern: This means notifying multiple systems simultaneously based on specific webhook triggers.

2. For webhook transformation and processing: Redirecting webhooks through Memphis allows for alterations or processing before they reach the intended client.

3. For webhook persistence: Memphis serves as a persisted message broker, making it ideal for storing webhooks, ensuring their durability and availability.

4. When implementing a pull mechanism: Instead of your service handling the push-based delivery of webhooks and potentially experiencing back pressure, Memphis can absorb this load. Your service then consumes the webhooks from Memphis, alleviating the pressure on your system.

## How to send webhooks to a Memphis Station

### Step 1: Generate a JWT token
The full Memphis REST Gateway can be found [here](https://github.com/memphisdev/memphis-rest-gateway?tab=readme-ov-file#getting-started).

Please create a JWT token, which will be part of each produce/consume request. For authentication purposes.

* The generated JWT will encapsulate all the needed information for the broker to ensure the requester is authenticated to communicate with Memphis.
* JWT token (by design) has an expiration time. Token refreshment can take place progrematically, but as it is often used to integrate memphis with other systems which are not supporting JWT refreshment, a workaround to overcome it would be to set a very high value in the `token_expiry_in_minutes`.
* The default expiry time is 15 minutes.

**For Memphis.dev Cloud Users (Using body params)**<br>
* Please replace the [Cloud], [Region], Username, Password, and Account ID with your parameters.
```bash
curl --location --request POST 'https://[Cloud]-[Region].restgw.cloud.memphis.dev/auth/authenticate' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "CLIENT_TYPE_USERNAME",
    "password": "CLIENT_TYPE_PASSWORD",
    "account_id": 123456789,
    "token_expiry_in_minutes": 6000000000,
    "refresh_token_expiry_in_minutes": 100000
}'
```

**For Memphis.dev Cloud Users (Using query params)**<br>
* Please replace the [Cloud], [Region], Username, Password, and Account ID with your parameters.
```bash
curl --location --request POST 'https://[Cloud]-[Region].restgw.cloud.memphis.dev/auth/authenticate?accountId=123456789' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "CLIENT_TYPE_USERNAME",
    "password": "CLIENT_TYPE_PASSWORD",
    "token_expiry_in_minutes": 6000000000,
    "refresh_token_expiry_in_minutes": 100000
}'
```

**Open-source**
```bash
curl --location --request POST 'https://REST_GW_URL:4444/auth/authenticate' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "CLIENT_TYPE_USERNAME",
    "password": "CLIENT_TYPE_PASSWORD,
    "token_expiry_in_minutes": 6000000000,
    "refresh_token_expiry_in_minutes": 100000
}'
```

Expected output:&#x20;

```JSON
{"expires_in":3600000,"jwt":"eyJhbGciO***************nR5cCI6IkpXVCJ9.eyJleHAiOjE2NzQ3MTg0MjV9._A************UFoWZjp21UYVcjXwGWiYtacYPZR8","jwt_refresh_token":"eyJhbGciOiJIUzI1N***************kpXVCJ9.eyJleHAiOjIy*********************7csm-jmJv0J45YrD_slvlEOKu2rs7Q","refresh_token_expires_in":600005520000}
```
<hr>

### Step 2: Configure the webhook in some 3rd party tool

**Supported content types:**

* text
* application/json
* application/x-protobuf

**For Memphis.dev Cloud Users**
* Please replace the `region`, `STATION_NAME`, `JWT token` with your parameters.

```bash
https://aws-region.restgw.cloud.memphis.dev/stations/STATION_NAME/produce/single?authorization=eyJhbGciOiJIU**********.e30.4KOLKsvHo33u3UdJ0qYP0kI
```

**Open-source**
* Please replace the `rest_gateway`, `STATION_NAME`, `JWT token` with your parameter.

```bash
rest_gateway:4444/stations/STATION_NAME/produce/single?authorization=ey*****
```

Expected output:

```json
{"error":null,"success":true}
```

Schema error example:

```json
{"error":"Schema validation has failed: jsonschema: '' does not validate with file:///Users/user/memphisdev/memphis-rest-gateway/123#/required: missing properties: 'field1', 'field2', 'field3'","success":false}
```
<hr>

### Example with Stripe (Similar to most systems support webhooks)
**Step 1: Create a new webhook (https://dashboard.stripe.com/webhooks/create)**<br>
![Screenshot 2023-12-10 at 16 04 59](https://github.com/memphisdev/memphis-dev-academy/assets/70286779/31063aac-6ce4-402b-b5e5-60cd9b7b24e9)<br>
**Step 2: After you generate a JWT token, paste the Memphis webhook URL in the Stripe's Endpoint URL input**<br>
```
https://aws-eu-central-1.restgw.cloud.memphis.dev/stations/stripe-notifications/produce/single?authorization=eyJhbGciO*******************N0MyJ9.qLM3c-********3Uo0
```
