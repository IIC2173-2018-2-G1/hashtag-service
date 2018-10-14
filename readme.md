# Hashtag Service
This is the hashtag microservice. It will be in charge of creating new hashtags from a message and storing the data in DB.

# This service should allow inbound HTTP requests on port 8085

## Admitted Requests

- Get all hashtags (validate):
> GET /hashtags
```javascript
{}
```

> Response:
```javascript
{
    hashtags: [hashtag_object],
    Error: string (default: "")
}
```

- Add Hashtags (validate):
> POST /hashtags
```javascript
{
    hashtags: [
        {
            hashtag_value: string,
            message_id: integer
        }
    ],
}
```

> Response:
```javascript
{
    Error: string (default: "")
}
```

# Things to note:
- 