import threading
from typing import Annotated
from fastapi import Depends
import hvac
import os
import logging

from contextlib import asynccontextmanager
import psycopg_pool as pg
from requests import Response
from bms.api.telemetry import api_vault_connection


class AppVault(hvac.Client):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppVault, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        logger = logging.getLogger("bms.dependencies.AppVault")
        try:
            CERTS_DIR=os.environ.get("CERTS_DIR", "/bms/certs")
            crt_path = os.path.join(CERTS_DIR, os.environ.get("SSL_CERT_PATH", "bms.crt"))
            key_path = os.path.join(CERTS_DIR, os.environ.get("SSL_KEY_PATH", "bms.key"))

            # TODO: Fix cert verification => certificate key too weak (_ssl.c:1000)
            # verify_cert_path = os.path.join(CERTS_DIR, os.environ.get("SSL_VERIFY_CERT_PATH", "ca.crt"))
            logging.captureWarnings(True)

            super().__init__(
                url="https://vault:8200",
                token=os.environ.get("VAULT_TOKEN"),
                cert=(crt_path, key_path),
                # verify=verify_cert_path
                verify=False
            )

            if self.sys.is_sealed() or not self.sys.is_initialized():
                raise Exception("Vault not running or sealed, please unseal the vault.")

            APPROLE=os.environ.get("APPROLE_PATH", "")

            ROLE_ID=os.environ.get('ROLE_ID', "")
            if not ROLE_ID:
                raise Exception("No Role ID passed")

            result = self.auth.approle.read_role_id(APPROLE)
            if result is Response and result.status_code == 404:
                raise Exception("Server AppRole doesn't exist in the Vault.")

            result = self.auth.approle.generate_secret_id(
                role_name=APPROLE,
                wrap_ttl="10s",
            )

            result_token = result['wrap_info']['token']
            unwrapped_result = self.sys.unwrap(result_token)
            self.logout()
            self.auth.approle.login(ROLE_ID, unwrapped_result['data']['secret_id'])
            if self.is_authenticated():
                logger.info('Vault initialized!')
                api_vault_connection.inc()
            else:
                raise Exception("Server could not authenticate with Vault")

        except Exception as err:
            logger.error(err)

class UserVault(hvac.Client):
    def __init__(self, user):
        CERTS_DIR=os.environ.get("CERTS_DIR", "/bms/certs")
        crt_path = os.path.join(CERTS_DIR, os.environ.get("SSL_CERT_PATH", "bms.crt"))
        key_path = os.path.join(CERTS_DIR, os.environ.get("SSL_KEY_PATH", "bms.key"))

        # TODO: Fix cert verification => certificate key too weak (_ssl.c:1000)
        # verify_cert_path = os.path.join(CERTS_DIR, os.environ.get("SSL_VERIFY_CERT_PATH", "ca.crt"))
        super().__init__(
                url="https://vault:8200",
                cert=(crt_path, key_path),
                # verify=verify_cert_path
                verify=False
            )
        self.auth.userpass.login(user.username, user.password)

class DBConnection():
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, app_vault: Annotated[AppVault, Depends()]):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DBConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, app_vault: AppVault):
        self.logger = logging.getLogger("bms.dependencies.Database")
        credentials = app_vault.secrets.kv.v2.read_secret_version(
            raise_on_deleted_version=False,
            mount_point="kv",
            path="postgres"
        )['data']['data']
        self._conninfo = (
            f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}")
        self.logger.info('Database Pool Initialized')



    async def execute(self, query):
        async with self.connection() as connection:
            return await connection.execute(query)

    @asynccontextmanager
    async def connection(self):
        async with pg.AsyncConnectionPool(self._conninfo) as pool:
            async with pool.connection() as connection:
                yield connection

    @asynccontextmanager
    async def transaction(self):
        async with self.connection() as connection:
            yield connection.transaction()
