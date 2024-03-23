import analytics_engine.settings as st
from firebase_admin import credentials, storage, initialize_app


def connect_firebase():
    """
    Conects to the Firebase for further use
    :return: None
    """
    cred = credentials.Certificate(st.VENTURA_FIREBASE_PRIVATE_KEY)
    initialize_app(cred, {'storageBucket': 'gs://ventura-bfe66.appspot.com'})
    # start the storage client in firebase. It is saved in
    st.FIREBASE_BUCKET = storage.bucket("ventura-bfe66.appspot.com")
    print("Connection to Firebase and bucket created.")
    print(type(st.FIREBASE_BUCKET))
