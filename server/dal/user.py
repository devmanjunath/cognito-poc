from datetime import datetime
import boto3
from server.config import fetch_client_id, fetch_template_url, fetch_userpool_id


class UserConfig:
    def __init__(self):
        self.cogn_client = boto3.client("cognito-idp", "ap-south-1")
        self.cfn_client = boto3.client("cloudformation", "ap-south-1")
        self.template_URL = fetch_template_url()

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
            self.cogn_client.sign_up(**kwargs)
            return {"success": True, "message": "Please confirm your signup, check Email for validation code"}
        except self.client.exceptions.UsernameExistsException:
            return {"success": False, "message": "Username already exists"}
        except self.client.exceptions.InvalidPasswordException:
            return {"success": False, "message": "Invalid Password"}
        except self.client.exceptions.UserLambdaValidationException:
            return {"success": False, "message": "Email already exists"}
        except Exception as error:
            return {"success": False, "message": str(error)}

    def confirm_signup(self, username, code):
        kwargs = {
            "ClientId": fetch_client_id(),
            "Username": username,
            "ConfirmationCode": code
        }
        try:
            self.cogn_client.confirm_sign_up(**kwargs)
            return {"error": False,
                    "success": True,
                    "message": f"User {username} is enabled, is now available for login",
                    "data": None}
        except self.cogn_client.exceptions.UserNotFoundException:
            return {"error": True, "success": False, "message": "Username doesnt exists"}
        except self.cogn_client.exceptions.CodeMismatchException:
            return {"error": True, "success": False, "message": "Invalid Verification code"}

        except self.cogn_client.exceptions.NotAuthorizedException:
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
            response = self.cogn_client.initiate_auth(**kwargs)
            return {"error": False,
                    "success": True,
                    "message": "Logged in successfully!",
                    "data": response}
        except self.cogn_client.exceptions.UsernameExistsException as error:
            return {"error": False,
                    "success": True,
                    "message": "This username already exists",
                    "data": error}
        except self.cogn_client.exceptions.InvalidPasswordException as error:

            return {
                "error": False,
                "success": True,
                "message": "Password should have Caps,\
                            Special chars, Numbers",
                "data": error
            }
        except self.cogn_client.exceptions.UserLambdaValidationException as error:
            return {
                "error": False,
                "success": True,
                "message": "Email already exists",
                "data": error
            }

        except Exception as error:
            return {
                "error": False,
                "success": True,
                "message": str(error),
                "data": error
            }

    def attach_user_group(self, username, group_name):
        current_ts = datetime.now().isoformat().split('.')[0].replace(':', '-')
        stackname = group_name + current_ts
        capabilities = ['CAPABILITY_IAM', 'CAPABILITY_AUTO_EXPAND']
        try:
            template_params = [
                {
                    'ParameterKey': 'UserName',
                    'ParameterValue': username
                },
                {
                    'ParameterKey': 'GroupName',
                    'ParameterValue': group_name
                },
                {
                    'ParameterKey': 'UserPoolID',
                    'ParameterValue': fetch_userpool_id()
                }]
            stackdata = self.cfn_client.create_stack(
                StackName=stackname,
                DisableRollback=True,
                TemplateURL=self.template_URL,
                Parameters=template_params,
                Capabilities=capabilities)
        except Exception as e:
            print(str(e))
        return stackdata
