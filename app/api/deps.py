# from fastapi import Header, HTTPException, Security
# from starlette import status

# # Mocking a database check for now
# VALID_API_KEYS = {"test_key_123": "project_abc"}

# async def get_api_key(x_api_key: str = Header(...)):
#     if x_api_key not in VALID_API_KEYS:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid API Key"
#         )
#     return VALID_API_KEYS[x_api_key] # Returns the project_id