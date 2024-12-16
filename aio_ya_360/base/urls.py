class Ya360Url:

    @staticmethod
    def organizations_list():
        return "directory/v1/org/"

    @staticmethod
    def users(org_id: str):
        return f'directory/v1/org/{org_id}/users/'

    @staticmethod
    def user(org_id: str, user_id: str):
        return f'directory/v1/org/{org_id}/users/{user_id}'

    @staticmethod
    def user_contacts(org_id: str, user_id: str):
        return f'directory/v1/org/{org_id}/users/{user_id}/contacts/'

    @staticmethod
    def groups(org_id: str):
        return f'directory/v1/org/{org_id}/groups/'

    @staticmethod
    def group(org_id: str, group_id: str):
        return f'directory/v1/org/{org_id}/groups/{group_id}'

    @staticmethod
    def group_members(org_id: str, group_id: str):
        return f'directory/v1/org/{org_id}/groups/{group_id}/members'

    @staticmethod
    def departments(org_id: str):
        return f'directory/v1/org/{org_id}/departments/'

    @staticmethod
    def department(org_id: str, department_id: str):
        return f'directory/v1/org/{org_id}/departments/{department_id}'

    @staticmethod
    def user_2fa(org_id: str, user_id: str):
        return f'directory/v1/org/{org_id}/users/{user_id}/2fa/'

    @staticmethod
    def user_aliases(org_id: str, user_id: str, alias: str = None):
        if alias is None:
            return f'directory/v1/org/{org_id}/users/{user_id}/aliases/'
        else:
            return f'directory/v1/org/{org_id}/users/{user_id}/aliases/{alias}'

    @staticmethod
    def department_aliases(org_id: str, department_id: str):
        return f'directory/v1/org/{org_id}/departments/{department_id}/aliases'

    @staticmethod
    def department_alias(org_id: str, department_id: str, alias: str):
        return f'directory/v1/org/{org_id}/departments/{department_id}/aliases/{alias}'

    @staticmethod
    def group_admins(org_id: str, group_id: str):
        return f'directory/v1/org/{org_id}/groups/{group_id}/admins'
