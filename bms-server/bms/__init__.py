import logging
import datetime
import hvac
import os
import sys

from requests import Response
from bms.api import make_server

logger = logging.getLogger("bms")
now = datetime.datetime.now()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s|%(levelname)s:%(name)s:%(message)s',
    datefmt="%Y-%m-%dT%H:%M:%S",
    encoding="utf-8",
    handlers=[
        logging.FileHandler(os.path.join('/bms', 'logs', f"logs_{now.strftime('%Y-%m-%dT%H:%M:%S')}.log")),
        logging.StreamHandler(sys.stdout)
    ]
)

def setup_app():
    try:
        CERTS_DIR=os.environ.get("CERTS_DIR", "/bms/certs")
        crt_path = os.path.join(CERTS_DIR, os.environ.get("SSL_CERT_PATH", "bms.crt"))
        key_path = os.path.join(CERTS_DIR, os.environ.get("SSL_KEY_PATH", "bms.key"))

        # TODO: Fix cert verification => certificate key too weak (_ssl.c:1000)
        # verify_cert_path = os.path.join(CERTS_DIR, os.environ.get("SSL_VERIFY_CERT_PATH", "ca.crt"))
        logging.captureWarnings(True)

        client = hvac.Client(
            url="https://vault:8200",
            token=os.environ.get("VAULT_TOKEN"),
            cert=(crt_path, key_path),
            # verify=verify_cert_path
            verify=False
        )
        del os.environ["VAULT_TOKEN"]

        if client.sys.is_sealed() or not client.sys.is_initialized():
            raise Exception("Vault not running or sealed, please unseal the vault.")

        APPROLE=os.environ.get("APPROLE_PATH", "")

        ROLE_ID=os.environ.get('ROLE_ID', "")
        if not ROLE_ID:
            raise Exception("No Role ID passed")

        result = client.auth.approle.read_role_id(APPROLE)
        if result is Response and result.status_code == 404:
            raise Exception("Server AppRole doesn't exist in the Vault.")

        logger.info("Authenticating")
        result = client.auth.approle.generate_secret_id(
            role_name=APPROLE,
            wrap_ttl="10s",
        )

        result_token = result['wrap_info']['token']
        unwrapped_result = client.sys.unwrap(result_token)
        client.logout()
        client.auth.approle.login(ROLE_ID, unwrapped_result['data']['secret_id'])
        if client.is_authenticated():
            logger.info("Server authenticated successfully")
            print('Setup done!')
            return client
        else:
            raise Exception("Server could not authenticate with Vault")

    except Exception as err:
        logger.error(err)

app = make_server(setup_app())
