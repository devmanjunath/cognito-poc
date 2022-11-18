import boto3
import botocore.exceptions
from config import fetch_client_id

class UserConfig:
    def __init__(self):
        self.client = boto3.client("cognito-idp", "ap-south-1")
    
    def user_signup(self, username, email, password):
        kwargs = {
            "ClientId": fetch_client_id(),
            "Username": username,
            "Password": password,
            "UserAttributes": [
                {
                    'Name': "email",
                    'Value': email
                }
            ]
        }
        try:
            self.client.sign_up(**kwargs)
            return {"error": False,
                    "success": True,
                    "message": "Please confirm your signup, \
                            check Email for validation code",
                    "data": None}
        except self.client.exceptions.UsernameExistsException as e:
            return {"error": False,
                    "success": True,
                    "message": "This username already exists",
                    "data": None}
        except self.client.exceptions.InvalidPasswordException as e:

            return {"error": False,
                    "success": True,
                    "message": "Password should have Caps,\
                            Special chars, Numbers",
                    "data": None}
        except self.client.exceptions.UserLambdaValidationException as e:
            return {"error": False,
                    "success": True,
                    "message": "Email already exists",
                    "data": None}

        except Exception as e:
            return {"error": False,
                    "success": True,
                    "message": str(e),
                    "data": None}

    def confirm_signup(self, username, code):
        kwargs = {
            "ClientId": fetch_client_id(),
            "Username": username,
            "ConfirmationCode": code
        }
        try:
            self.client.confirm_sign_up(**kwargs)
            return {"error": False,
                    "success": True,
                    "message": f"User {username} is enabled, is now available for login",
                    "data": None}
        except self.client.exceptions.UserNotFoundException:
            return {"error": True, "success": False, "message": "Username doesnt exists"}
        except self.client.exceptions.CodeMismatchException:
            return {"error": True, "success": False, "message": "Invalid Verification code"}

        except self.client.exceptions.NotAuthorizedException:
            return {"error": True, "success": False, "message": "User is already confirmed"}

        except Exception as e:
            return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}

    def user_signin(self, username, password):
        kwargs = {
            "ClientId": fetch_client_id(),
            "AuthFlow": "USER_PASSWORD_AUTH",
            "AuthParameters": {"USERNAME": username, "PASSWORD": password}
        }
        try:
            response = self.client.initiate_auth(**kwargs)
            return {"error": False,
                    "success": True,
                    "message": "Logged in successfully!",
                    "data": response}
        except self.client.exceptions.UsernameExistsException as e:
            return {"error": False,
                    "success": True,
                    "message": "This username already exists",
                    "data": None}
        except self.client.exceptions.InvalidPasswordException as e:

            return {"error": False,
                    "success": True,
                    "message": "Password should have Caps,\
                            Special chars, Numbers",
                    "data": None}
        except self.client.exceptions.UserLambdaValidationException as e:
            return {"error": False,
                    "success": True,
                    "message": "Email already exists",
                    "data": None}

        except Exception as e:
            return {"error": False,
                    "success": True,
                    "message": str(e),
                    "data": None}
