class Ya360Url:

    @staticmethod
    def organizations_list():
        return "directory/v1/org/"

    @staticmethod
    def users_list(org_id: str):
        return f'directory/v1/org/{org_id}/users/'

    @staticmethod
    def user(org_id: str, user_id: str):
        return f'directory/v1/org/{org_id}/users/{user_id}'

    @staticmethod
    def user_contacts(org_id: str, user_id: str):
        return f'directory/v1/org/{org_id}/users/{user_id}/contacts/'

    @staticmethod
    def groups_list(org_id: str):
        return f'directory/v1/org/{org_id}/groups/'

    @staticmethod
    def group(org_id: str, group_id: str):
        return f'directory/v1/org/{org_id}/groups/{group_id}'

    @staticmethod
    def department_list(org_id: str):
        return f'directory/v1/org/{org_id}/departments/'

    @staticmethod
    def department(org_id: str, department_id: str):
        return f'directory/v1/org/{org_id}/departments/{department_id}'
