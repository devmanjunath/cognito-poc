import boto3
from config import fetch_client_id


class S3Config:
    def __init__(self):
        self.client = boto3.client("s3",
                                   "ap-south-1",
                                   aws_access_key_id="AKIAXECO7YDRMASXL3PC",
                                   aws_secret_access_key="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")

    def list_buckets(self):
        try:
            buckets = self.client.list_buckets()
            return {"error": False,
                    "success": True,
                    "message": "fetched buckets",
                    "data": buckets}

        except Exception as e:
            return {"error": False,
                    "success": True,
                    "message": str(e),
                    "data": None}
