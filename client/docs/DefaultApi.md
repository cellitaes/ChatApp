# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ban_user_user_ban_put**](DefaultApi.md#ban_user_user_ban_put) | **PUT** /user/ban | Ban User
[**create_message_from_user_message_receiver_id_post**](DefaultApi.md#create_message_from_user_message_receiver_id_post) | **POST** /message/{receiver_id}/ | Create Message From User
[**create_user_users_post**](DefaultApi.md#create_user_users_post) | **POST** /users/ | Create User
[**delete_message_by_id_message_message_id_delete**](DefaultApi.md#delete_message_by_id_message_message_id_delete) | **DELETE** /message/{message_id} | Delete Message By Id
[**get_users_by_status_users_status_status_get**](DefaultApi.md#get_users_by_status_users_status_status_get) | **GET** /users/status/{status} | Get Users By Status
[**kick_user_user_kick_get**](DefaultApi.md#kick_user_user_kick_get) | **GET** /user/kick | Kick User
[**login_user_users_login_post**](DefaultApi.md#login_user_users_login_post) | **POST** /users/login | Login User
[**read_all_messages_message_get**](DefaultApi.md#read_all_messages_message_get) | **GET** /message/ | Read All Messages
[**read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get**](DefaultApi.md#read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get) | **GET** /message/{receiver_id}/{sender_id}/{from_date} | Read Messages To User From Date
[**read_messages_to_user_from_message_receiver_id_sender_id_get**](DefaultApi.md#read_messages_to_user_from_message_receiver_id_sender_id_get) | **GET** /message/{receiver_id}/{sender_id}/ | Read Messages To User From
[**read_user_users_user_id_get**](DefaultApi.md#read_user_users_user_id_get) | **GET** /users/{user_id} | Read User
[**read_users_users_get**](DefaultApi.md#read_users_users_get) | **GET** /users/ | Read Users
[**update_user_status_users_status_put**](DefaultApi.md#update_user_status_users_status_put) | **PUT** /users/status | Update User Status


# **ban_user_user_ban_put**
> User ban_user_user_ban_put(user_ban)

Ban User

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user import User
from openapi_client.model.user_ban import UserBan
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    user_ban = UserBan(
        id=1,
        is_banned=True,
    ) # UserBan | 

    # example passing only required values which don't have defaults set
    try:
        # Ban User
        api_response = api_instance.ban_user_user_ban_put(user_ban)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->ban_user_user_ban_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_ban** | [**UserBan**](UserBan.md)|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_message_from_user_message_receiver_id_post**
> Message create_message_from_user_message_receiver_id_post(receiver_id, message_create)

Create Message From User

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.message_create import MessageCreate
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.message import Message
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    receiver_id = 1 # int | 
    message_create = MessageCreate(
        msg_content="msg_content_example",
        from_usr=1,
    ) # MessageCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Create Message From User
        api_response = api_instance.create_message_from_user_message_receiver_id_post(receiver_id, message_create)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->create_message_from_user_message_receiver_id_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **receiver_id** | **int**|  |
 **message_create** | [**MessageCreate**](MessageCreate.md)|  |

### Return type

[**Message**](Message.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_users_post**
> User create_user_users_post(user_create)

Create User

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user import User
from openapi_client.model.user_create import UserCreate
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    user_create = UserCreate(
        login="login_example",
        password="password_example",
    ) # UserCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Create User
        api_response = api_instance.create_user_users_post(user_create)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->create_user_users_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_create** | [**UserCreate**](UserCreate.md)|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_message_by_id_message_message_id_delete**
> bool, date, datetime, dict, float, int, list, str, none_type delete_message_by_id_message_message_id_delete(message_id)

Delete Message By Id

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    message_id = 1 # int | 

    # example passing only required values which don't have defaults set
    try:
        # Delete Message By Id
        api_response = api_instance.delete_message_by_id_message_message_id_delete(message_id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->delete_message_by_id_message_message_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_id** | **int**|  |

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users_by_status_users_status_status_get**
> bool, date, datetime, dict, float, int, list, str, none_type get_users_by_status_users_status_status_get(status)

Get Users By Status

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    status = "status_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get Users By Status
        api_response = api_instance.get_users_by_status_users_status_status_get(status)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_users_by_status_users_status_status_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **str**|  |

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **kick_user_user_kick_get**
> User kick_user_user_kick_get(receiver_id)

Kick User

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user import User
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    receiver_id = 1 # int | 

    # example passing only required values which don't have defaults set
    try:
        # Kick User
        api_response = api_instance.kick_user_user_kick_get(receiver_id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->kick_user_user_kick_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **receiver_id** | **int**|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login_user_users_login_post**
> User login_user_users_login_post(user_create)

Login User

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user import User
from openapi_client.model.user_create import UserCreate
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    user_create = UserCreate(
        login="login_example",
        password="password_example",
    ) # UserCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Login User
        api_response = api_instance.login_user_users_login_post(user_create)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->login_user_users_login_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_create** | [**UserCreate**](UserCreate.md)|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_all_messages_message_get**
> [Message] read_all_messages_message_get()

Read All Messages

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.message import Message
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    skip = 0 # int |  (optional) if omitted the server will use the default value of 0
    limit = 100 # int |  (optional) if omitted the server will use the default value of 100

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Read All Messages
        api_response = api_instance.read_all_messages_message_get(skip=skip, limit=limit)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->read_all_messages_message_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] if omitted the server will use the default value of 0
 **limit** | **int**|  | [optional] if omitted the server will use the default value of 100

### Return type

[**[Message]**](Message.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get**
> [Message] read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get(receiver_id, sender_id, from_date)

Read Messages To User From Date

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.message import Message
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    receiver_id = 1 # int | 
    sender_id = 1 # int | 
    from_date = dateutil_parser('1970-01-01T00:00:00.00Z') # datetime | 
    skip = 0 # int |  (optional) if omitted the server will use the default value of 0
    limit = 100 # int |  (optional) if omitted the server will use the default value of 100

    # example passing only required values which don't have defaults set
    try:
        # Read Messages To User From Date
        api_response = api_instance.read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get(receiver_id, sender_id, from_date)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Read Messages To User From Date
        api_response = api_instance.read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get(receiver_id, sender_id, from_date, skip=skip, limit=limit)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **receiver_id** | **int**|  |
 **sender_id** | **int**|  |
 **from_date** | **datetime**|  |
 **skip** | **int**|  | [optional] if omitted the server will use the default value of 0
 **limit** | **int**|  | [optional] if omitted the server will use the default value of 100

### Return type

[**[Message]**](Message.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_messages_to_user_from_message_receiver_id_sender_id_get**
> [Message] read_messages_to_user_from_message_receiver_id_sender_id_get(receiver_id, sender_id)

Read Messages To User From

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.message import Message
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    receiver_id = 1 # int | 
    sender_id = 1 # int | 
    skip = 0 # int |  (optional) if omitted the server will use the default value of 0
    limit = 100 # int |  (optional) if omitted the server will use the default value of 100

    # example passing only required values which don't have defaults set
    try:
        # Read Messages To User From
        api_response = api_instance.read_messages_to_user_from_message_receiver_id_sender_id_get(receiver_id, sender_id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->read_messages_to_user_from_message_receiver_id_sender_id_get: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Read Messages To User From
        api_response = api_instance.read_messages_to_user_from_message_receiver_id_sender_id_get(receiver_id, sender_id, skip=skip, limit=limit)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->read_messages_to_user_from_message_receiver_id_sender_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **receiver_id** | **int**|  |
 **sender_id** | **int**|  |
 **skip** | **int**|  | [optional] if omitted the server will use the default value of 0
 **limit** | **int**|  | [optional] if omitted the server will use the default value of 100

### Return type

[**[Message]**](Message.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_user_users_user_id_get**
> User read_user_users_user_id_get(user_id)

Read User

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user import User
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    user_id = 1 # int | 

    # example passing only required values which don't have defaults set
    try:
        # Read User
        api_response = api_instance.read_user_users_user_id_get(user_id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->read_user_users_user_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_users_users_get**
> [User] read_users_users_get()

Read Users

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user import User
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    skip = 0 # int |  (optional) if omitted the server will use the default value of 0
    limit = 100 # int |  (optional) if omitted the server will use the default value of 100

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Read Users
        api_response = api_instance.read_users_users_get(skip=skip, limit=limit)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->read_users_users_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] if omitted the server will use the default value of 0
 **limit** | **int**|  | [optional] if omitted the server will use the default value of 100

### Return type

[**[User]**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_status_users_status_put**
> User update_user_status_users_status_put(user)

Update User Status

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.user import User
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    user = User(
        login="login_example",
        id=1,
        is_active=True,
        is_banned=True,
    ) # User | 

    # example passing only required values which don't have defaults set
    try:
        # Update User Status
        api_response = api_instance.update_user_status_users_status_put(user)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->update_user_status_users_status_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**User**](User.md)|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

