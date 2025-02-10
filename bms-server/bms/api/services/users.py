import logging
from typing import Annotated
from bms.api.models import users as models
from bms.api.dependencies import AppVault, DBConnection, UserVault
from fastapi import Depends
import sqlglot.expressions as sql

class UsersService:
    TABLE='bms.users'

    def __init__(self,
                 app_vault: Annotated[AppVault, Depends()],
                 db: Annotated[DBConnection, Depends()],
                 ):
        self._db = db
        self._app_vault = app_vault
        self.logger = logging.getLogger("bms.services.Users")

    async def create_user(self, user: models.UserCreate):
        is_new_user = await (await self._db.execute(
            sql.select(sql.to_column('COUNT(*)').as_("user_count"))
            .from_(self.TABLE)
            .where(sql.to_column("username").eq(user.username))
            .sql('postgres')
            .encode('utf-8')
        )).fetchone()
        is_new_user = is_new_user and is_new_user[0] == 0
        if is_new_user:
            async with self._db.transaction():
                stmt = (sql.insert(sql.values([(user.email,user.name, user.username)])
                            , into=self.TABLE
                            , columns=["email", "name", "username"])
                        .returning("id")
                        .sql('postgres')
                        .encode('utf-8'))
                return await (await self._db.execute(stmt)).fetchone()

        return is_new_user


    async def delete_user(self, username: str):
        async with self._db.transaction():
            stmt = (sql.delete(
                        self.TABLE,
                        where=sql.to_column("username").eq(username)
                    ).returning("is_activated")
                    .sql('postgres')
                    .encode('utf-8'))
            user_data = await (await self._db.execute(stmt)).fetchone()
            if user_data and user_data[0]: # User is registered in the vault
                self._app_vault.auth.userpass.delete_user(username)

    async def login(self, user: models.UserCredentials):
        user_data = None
        stmt = (sql.select("is_activated")
                .from_(self.TABLE)
                .where(sql.to_column("username").eq(user.username))
                .sql("postgres")
                .encode('utf-8'))
        is_activated = await (await self._db.execute(stmt)).fetchone()
        if not is_activated or not is_activated[0]:
            response = self._app_vault.auth.userpass.create_or_update_user(user.username, user.password)
            if response.status_code == 204:
                async with self._db.transaction():
                    await self._db.execute(stmt)
                    stmt = (sql.select('name', 'email')
                            .from_(self.TABLE)
                            .where(sql.to_column("username").eq(user.username))
                            .sql('postgres')
                            .encode('utf-8'))
                    user_data = await (await self._db.execute(stmt)).fetchone()
            user_client = UserVault(user)
            if user_client.is_authenticated() and user_data:
                return models.LoginResponse(
                    username=user.username,
                    name=user_data[0],
                    email=user_data[1],
                    token=user_client.token)

        return models.LoginFailedResponse(message="Wrong credentials, please verify")
