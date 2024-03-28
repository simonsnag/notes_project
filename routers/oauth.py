from fastapi import APIRouter, status

oauth_router = APIRouter(prefix='/oauth')


@oauth_router.get(
    "/google/login",
    summary='Get Google OAuth link',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': OAuthRedirectLink, 'description': 'Google OAuth link.'},
    }
)
def google_oauth_login_request() -> OAuthRedirectLink:
    """Get Google OAuth link."""

    return service_google_oauth.generate_link_for_code()


