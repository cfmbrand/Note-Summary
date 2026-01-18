"""Microsoft Graph API authentication using MSAL device code flow."""

import sys
from typing import Optional

from msal import PublicClientApplication

from src.auth.token_cache import TokenCache
from src.utils.config import AzureConfig


# Microsoft Graph API scopes required for this application
GRAPH_SCOPES = [
    "User.Read",
    "Mail.Read",
    "Mail.ReadWrite",
    "Notes.Create",
    "Notes.ReadWrite",
]


class GraphAuth:
    """Handle Microsoft Graph API authentication."""

    def __init__(self, config: AzureConfig):
        """Initialize Graph authentication.

        Args:
            config: Azure AD configuration with client_id and tenant_id.
        """
        self._config = config
        self._token_cache = TokenCache()

        # Build authority URL
        authority = f"https://login.microsoftonline.com/{config.tenant_id}"

        self._app = PublicClientApplication(
            client_id=config.client_id,
            authority=authority,
            token_cache=self._token_cache.cache,
        )

    def get_access_token(self, interactive: bool = True) -> Optional[str]:
        """Get an access token for Microsoft Graph API.

        First attempts to use cached credentials. If that fails and
        interactive=True, initiates device code flow.

        Args:
            interactive: If True, prompt for login if no cached token.

        Returns:
            Access token string, or None if authentication failed.
        """
        # Try to get token silently from cache
        accounts = self._app.get_accounts()
        if accounts:
            result = self._app.acquire_token_silent(GRAPH_SCOPES, account=accounts[0])
            if result and "access_token" in result:
                self._token_cache.save()
                return result["access_token"]

        if not interactive:
            return None

        # No cached token, use device code flow
        return self._authenticate_device_code()

    def _authenticate_device_code(self) -> Optional[str]:
        """Authenticate using device code flow.

        Returns:
            Access token string, or None if authentication failed.
        """
        flow = self._app.initiate_device_flow(scopes=GRAPH_SCOPES)

        if "user_code" not in flow:
            print(f"Failed to create device flow: {flow.get('error_description', 'Unknown error')}")
            return None

        # Display instructions to user
        print("\n" + "=" * 60)
        print("AUTHENTICATION REQUIRED")
        print("=" * 60)
        print(f"\n{flow['message']}\n")
        print("=" * 60 + "\n")
        sys.stdout.flush()

        # Wait for user to complete authentication
        result = self._app.acquire_token_by_device_flow(flow)

        if "access_token" in result:
            self._token_cache.save()
            print("Authentication successful!")
            return result["access_token"]
        else:
            print(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
            return None

    def logout(self) -> None:
        """Clear cached credentials."""
        self._token_cache.clear()
        print("Logged out successfully.")

    def is_authenticated(self) -> bool:
        """Check if there are cached credentials available.

        Returns:
            True if cached credentials exist.
        """
        accounts = self._app.get_accounts()
        return len(accounts) > 0
