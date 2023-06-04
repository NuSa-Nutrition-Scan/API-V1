# request_ref = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={self.api_key}"
#         headers = {"content-type": "application/json; charset=UTF-8"}

#         if uploaded_photo_url == '':
#             data = json.dumps({
#                 "idToken": user.auth_token,
#                 "displayName": name,
#                 "returnSecureToken": True
#             })

#         else:
#             data = json.dumps({
#                 "idToken": user.auth_token,
#                 "displayName": name,
#                 "photoUrl": uploaded_photo_url,
#                 "returnSecureToken": True
#             })

#         try:
#             response = requests.post(request_ref, headers=headers, data=data)
#             response.raise_for_status()

#             obj = response.json()
#             resp = {
#                 "id": obj["localId"],
#                 "email": obj["email"],
#                 "name": obj["displayName"],
#                 "photo_url": obj['providerUserInfo'][0]["photoUrl"],
#             }

#             return result.OK(resp)