import firebase_admin
from firebase_admin import auth, credentials, firestore

# Load Firebase credentials securely
try:
    cred = credentials.Certificate("./firebase-adminsdk.json")  
    if not firebase_admin._apps:  # Prevents re-initialization errors
        firebase_admin.initialize_app(cred)
except FileNotFoundError:
    print("[ERROR] Firebase service account file not found. Ensure 'firebase-adminsdk.json' exists in the backend folder.")
    exit(1)
except Exception as e:
    print(f"[ERROR] Firebase initialization failed: {e}")
    exit(1)

# Firestore client
db = firestore.client()

def verify_firebase_token(token):
    """Verify Firebase Auth Token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # Returns user details (email, uid, role)
    except auth.ExpiredIdTokenError:
        print("[ERROR] Token has expired.")
        return None
    except auth.InvalidIdTokenError:
        print("[ERROR] Invalid token provided.")
        return None
    except Exception as e:
        print(f"[ERROR] Token verification failed: {e}")
        return None
