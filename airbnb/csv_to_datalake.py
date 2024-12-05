from dotenv import load_dotenv
import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

load_dotenv()
tenant_id = os.getenv("TENANT_ID")
client_id_sp2 = os.getenv("CLIENT_ID_SP2")
client_secret_sp2 = os.getenv("CLIENT_SECRET_SP2")
keyvault_url = os.getenv("KEYVAULT_URL")
secret_name = os.getenv("SECRET_NAME")
client_id_sp1 = os.getenv("CLIENT_ID_SP1")
blob_storage_url = os.getenv("BLOB_STORAGE_URL")
container_name = os.getenv("CONTAINER_NAME")
file_path = os.getenv("FILE_PATH")
blob_name = os.getenv("BLOB_NAME")


sp2_credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id_sp2, client_secret=client_secret_sp2)

keyvault_client = SecretClient(vault_url=keyvault_url, credential=sp2_credential)

secret_sp1 = keyvault_client.get_secret(secret_name)

client_secret_sp1 = secret_sp1.value

sp1_credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id_sp1, client_secret=client_secret_sp1)

blob_service_client = BlobServiceClient(account_url=blob_storage_url, credential=sp1_credential)

container_client = blob_service_client.get_container_client(container=container_name)

blob_client = container_client.get_blob_client(blob=blob_name)

with open(file_path, 'rb') as file:
    blob_client.upload_blob(file, overwrite=True)


