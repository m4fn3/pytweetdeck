# --- First, login w/ your username/email + password --- #
import pytweetdeck
client = pytweetdeck.Client(name_or_email="USERNAME", password="PASSWORD")
client.dump_auth()
# -> {
#   "x-csrf-token": "0123456789asdfghjklzxcvbnm",
#   "cookie": "auth_token=asdfghjkl; ct0=0123456789asdfghjkl"
# }

# --- And you can login with this auth data next time --- #
import pytweetdeck
auth = {
  "x-csrf-token": "0123456789asdfghjklzxcvbnm",
  "cookie": "auth_token=asdfghjkl; ct0=0123456789asdfghjkl"
}
client = pytweetdeck.Client(auth)  # auth login
