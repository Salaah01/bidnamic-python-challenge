# API
This app will help maintain a consistent API structure for all applications.

It does this by providing functions for retuning API responses and exceptions. This therefore would mean that all APIs would look and feel the same as they will would all conform to a set standard. This ultimately means that APIs can be more easily maintained as well as providing a more consistent experience to API consumers.

## Usage
Let's suppose we have a `/users/` endpoint.
This endpoint will return a list of usernames.
We would normally have a view that would render this information by doing something similar to the following:

```python
from django.http import JsonResponse
from django.contrib.auth.models import User

def users(request):
    users = User.objects.values_list('username', flat=True)
    return JsonResponse(users)
```

In order to make our APIs consistent, we can make the following changes:
```python
from django.contrib.auth.models import User
from api import response as api_response

def users(request):
    users = User.objects.all()
    return api_response.success(request, users)
```
This will generate the following response:
```json
{
    "metadata": {
        "query_params": {}
    },
    "data": ["username1", "username2", "username3"]
}
```

### Adding Metadata
When calling the `success` function, you have the option to add additional metadata to the response. It will also take any query parameters that were passed with the request and add them to `metadata.query_params`.

Lets imagine we have a `/users/:username/` endpoint which returns a user's information.
```python
from django.contrib.auth.models import User
from api import response as api_response

def users(request, username):
    # We will assume that the username is valid.
    user = User.objects.get(username=username)
    return api_response.success(
      request,
      data={
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
      },
      metadata={'success': True}
    )
```

This will generate the following response:
```json
{
    "metadata": {
        "query_params": {"usnername": "<username>"},
        "success": true
    },
    "data": {
        "username": "<user.username>",
        "email": "<user.email>",
        "first_name": "<user.first_name>",
        "last_name": "<user.last_name>"
      }
}
```

### Raising an Exception
In the previous example, when fetching a specific user, we did not check if the user exists.
The app provides functions for raising exceptions. Let's amend our previous example to raise an exception if the user does not exist.

```python
from django.contrib.auth.models import User
from api import response as api_response, exceptions as api_exceptions

def users(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise api_exceptions.NotFoundError(
          request,
          metadata={'success': False},
          error="User does not exist"
        )
    ...
```

This will return the following 404 response:
```json
{
    "metadata": {
        "query_params": {"username": "<username>"},
        "success": false,
    },
    "error": "User does not exist",
    "data": null
}
```

Other exceptions can be raised. These exceptions can be found in the `exceptions` module.

## Customising the App
The basic response and exceptions can be customised by updating `response.base_response` and `exceptions.base_exception` respectively. These two functions are responsible for dictating the structure of the response and exceptions.
