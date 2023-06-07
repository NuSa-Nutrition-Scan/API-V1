title = "NuSa API"

version = "0.5.5"

contact = {
    "name": "NuSa CC Team",
    "email": "samuelhotang02@gmail.com",
}

license_info = {
    "name": "MIT",
    "url": "https://github.com/NuSa-Nutrition-Scan/API-V1/blob/main/LICENSE",
}

description = """
# [WATCH THIS FIRST!](https://www.youtube.com/watch?v=xvFZjo5PgG0)

NuSa API helps you, our solo mobile developers (LOL), to run your app. 🚀

## Features

You will be able to:

* **Authenticate user**
* **Get user profile & update it**
* **Upload photo with limit 10 every day**
* **Integrate with machine learning**  (_not implemented_).

#### NOTES FOR RESPONSE

1. Every 422 error response will be like this:
    ```
    {
        "code": 422,
        "msg": "Unprocessable Entity",
        "errors": {
            "name": "field required",
            "password": "field required"
        }
    }
    ```
    errors field will be dynamic key value pair

    
2. Other than 422, every error response will be like this:
    ```
    {
        "code": 401,
        "msg": "Unauthorized"
    }
    ```
    errors field will always code and msg

    
3. Every 200 success response will be like this:
    ```
    {
        "code": 200,
        "msg": "OK",
        "data": {
            "some": "dynamic data",
            "some": "dynamic data",
            "some": "dynamic data",
            "some": "dynamic data"
        }
    }
    ```
    the data field always will be dynamic key and value pair (maybe list of key value pair too)

    Other example
    ```
    {
        "code": 201,
        "msg": "Created"
    }
    ```
"""

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations with authentication",
    },
    {
        "name": "Nutrition",
        "description": "This is for nutrition section. Currently, only upload photo and get value of how many times user upload the photo today",
    },
    {
        "name": "Settings",
        "description": "Update profile, and see all the previous uploaded photo"
    }
]