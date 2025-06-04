import httpx
import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel

from models.models import Schedule


class JwtResponse(BaseModel):
    token: str


class ExecutorService:
    def __init__(self, http_client: httpx.AsyncClient, logger: logging.Logger):
        self._http_client = http_client
        self._logger = logger
        self._thingsboard_base_url = "http://100.86.185.63"
        self._username = "sysadmin@thingsboard.org"
        self._password = "sysadmin"
        # self._thingsboard_base_url = "https://demo.thingsboard.io"
        # self._username = "mustafahamad116aa@gmail.com"
        # self._password = "mustafa@1031998"
        self._tenant_password = "tenant"

    async def execute_schedule(self, schedule: Schedule):
        self._logger.info(f"Starting execution for schedule: {schedule.name}")
        tenant_id = schedule.tenant_id
        admin_token = await self.get_jwt_token(self._username, self._password)

        try:
            if not admin_token:
                self._logger.error("Failed to get ThingsBoard token.")
                return

            tenant_user = await self.get_tenant_user_email(tenant_id, admin_token)
            if not tenant_user:
                self._logger.error("Failed to get ThingsBoard tenant user.")
                return

            token = await self.get_jwt_token(tenant_user, self._tenant_password)
            if not token:
                self._logger.error("Failed to get ThingsBoard token.")
                return

            for device_setting in schedule.device_settings:
                for attr in device_setting.attributes:
                    attributes = {attr.key: attr.value}
                    self._logger.info(
                        f"Sending attributes to device {device_setting.device_id}: {attributes}"
                    )
                    await self.send_attribute_to_device(device_setting.device_id, attributes, token)

            self._logger.info(f"Finished execution for schedule: {schedule.name}")

        except Exception as ex:
            self._logger.error(f"Error executing schedule: {schedule.name}", exc_info=ex)

    async def get_jwt_token(self, name: str, password: str) -> Optional[str]:
        self._logger.info("Authenticating with ThingsBoard...")
        login_url = f"{self._thingsboard_base_url}/api/auth/login"
        payload = {"username": name, "password": password}

        try:
            response = await self._http_client.post(login_url, json=payload)
            if not response.is_success:
                self._logger.error(f"Authentication failed with status code: {response.status_code}")
                return None

            self._logger.info("Authentication succeeded.")
            jwt_response = JwtResponse(**response.json())
            return jwt_response.token

        except Exception as ex:
            self._logger.error("Exception occurred during authentication.", exc_info=ex)
            return None

    async def send_attribute_to_device(self, device_id: str, attributes: Dict[str, Any], token: str):
        self._logger.info(f"Preparing to send attributes to device {device_id}.")
        url = f"{self._thingsboard_base_url}/api/plugins/telemetry/DEVICE/{device_id}/attributes/SHARED_SCOPE"

        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = await self._http_client.post(url, headers=headers, json=attributes)
            if response.is_success:
                self._logger.info(f"Attributes sent successfully to device {device_id}.")
            else:
                content = response.text
                self._logger.error(
                    f"Failed to send attributes to device {device_id}. "
                    f"StatusCode: {response.status_code}, Response: {content}"
                )
        except Exception as ex:
            self._logger.error(
                f"Exception occurred while sending attributes to device {device_id}.", exc_info=ex
            )

    async def get_tenant_user_email(self, tenant_id: str, token: str) -> Optional[str]:
        url = f"{self._thingsboard_base_url}/api/tenant/{tenant_id}/users?pageSize=100&page=0"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = await self._http_client.get(url, headers=headers)
            if response.is_success:
                users = response.json().get("data", [])
                for user in users:
                    email = user.get("email", "")
                    if email.lower().startswith("tenant"):
                        return email
                return None
            else:
                self._logger.error(f"Request failed with status code: {response.status_code}")
                return None
        except Exception as ex:
            self._logger.error("Exception occurred while fetching tenant users.", exc_info=ex)
            return None
