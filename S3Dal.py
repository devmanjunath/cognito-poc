import boto3
from config import fetch_client_id


class S3Config:
    def __init__(self):
        self.client = boto3.client("s3",
                                   "ap-south-1")

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
