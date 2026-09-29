import json
from joyverse.config import r2_client, BUCKET_NAME, get_bio_key

def get_bio(user: dict) -> str:
    """Reads the user biography from R2."""
    username = user["username"]
    try:
        key = get_bio_key(username)
    except ValueError as e:
        return json.dumps({"error": f"Invalid username: {e}"})

    try:
        response = r2_client.get_object(Bucket=BUCKET_NAME, Key=key)
        return response["Body"].read().decode("utf-8")
    except Exception as e:
        if "NoSuchKey" in str(e):
            return json.dumps({"error": f"No bio found for {username}. Run setup_bio first."})
        return json.dumps({"error": f"R2 error: {str(e)}"})

def update_bio(content: str, user: dict) -> str:
    """Updates the user biography on R2.
    
    Replaces the entire bio.md content.
    """
    username = user["username"]
    try:
        key = get_bio_key(username)
    except ValueError as e:
        return f"Error: Invalid username: {e}"

    try:
        r2_client.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=content.encode("utf-8"),
            ContentType="text/markdown"
        )
        return "Bio updated successfully"
    except Exception as e:
        return f"Error writing to R2: {str(e)}"
