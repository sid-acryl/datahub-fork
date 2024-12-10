from dataclasses import dataclass

from tableauserverclient import Server, UserItem

from datahub.ingestion.source.tableau import tableau_constant as c


@dataclass
class LoggedInUser:
    user_name: str
    site_role: str
    site_id: str

    def is_site_administrator_explorer(self):
        return self.site_role == c.SITE_ROLE


class UserSiteInfo:
    @staticmethod
    def from_server(server: Server) -> "LoggedInUser":
        assert server.user_id, "make the connection with tableau"

        user: UserItem = server.users.get_by_id(server.user_id)

        assert user.site_role, "site_role is not available"  # to silent the lint

        assert user.name, "user name is not available"  # to silent the lint

        assert server.site_id, "site identifier is not available"  # to silent the lint

        return LoggedInUser(
            user_name=user.name,
            site_role=user.site_role,
            site_id=server.site_id,
        )
