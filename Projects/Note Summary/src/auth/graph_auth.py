"""Microsoft Graph API authentication using MSAL interactive browser flow."""

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

        # No cached token, use interactive browser flow
        return self._authenticate_interactive()

    def _authenticate_interactive(self) -> Optional[str]:
        """Authenticate using interactive browser flow.

        Opens the system browser for authentication and handles
        the redirect to localhost automatically.

        Returns:
            Access token string, or None if authentication failed.
        """
        print("\n" + "=" * 60)
        print("AUTHENTICATION REQUIRED")
        print("=" * 60)
        print("\nOpening browser for authentication...")
        print("=" * 60 + "\n")
        sys.stdout.flush()

        try:
            result = self._app.acquire_token_interactive(
                scopes=GRAPH_SCOPES,
                prompt="select_account",
            )
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None

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
