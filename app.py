import asyncio
import secrets
import string

from environs import Env

from aio_ya360_client.aio_ya360_client import AIOYa360Client, Yandex360ClientSecret, Yandex360Exception


async def main():
    env = Env()
    env.read_env()
    client = None
    try:
        client = AIOYa360Client(
            client_secret=Yandex360ClientSecret.from_json(
                data={
                    'client_id': env.str('CLIENT_ID'),
                    'client_secret': env.str('CLIENT_SECRET')
                }
            )
        )
        await client.start_work()

        organizations = await client.get_organizations_list()
        # for organization in organizations:
        #     print(organization)

        users = await client.get_users_list(org_id=env.int('ORGANISATION_ID'))
        # for user in users:
        #     print(user)

        current_user = await client.get_current_user(
            org_id=env.int('ORGANISATION_ID'),
            user_id='1130000067921268'
        )
        # print(current_user)

        groups = await client.get_groups_list(
            org_id=env.int('ORGANISATION_ID'),
        )
        # for group in groups:
        #     print(group.id, ':', group.name)

        current_group = await client.get_current_group(
            org_id=env.int('ORGANISATION_ID'),
            group_id='19'
        )
        # print(current_group)

        group_members = await client.get_group_members(
            org_id=env.int('ORGANISATION_ID'),
            group_id='19'
        )
        # for departments in group_members.departments:
        #     print(departments)
        # for groups in group_members.groups:
        #     print(groups)
        # for users in group_members.users:
        #     print(users)

        departments = await client.get_departments_list(
            org_id=env.int('ORGANISATION_ID'),
        )
        # for department in departments:
        #     print(department.id, ':', department.name)

        current_department = await client.get_current_department(
            org_id=env.int('ORGANISATION_ID'),
            department_id='11'
        )
        # print(current_department)

        edited_user_id = ''
        for user in users:
            if user.name.first == 'KAV' and user.name.last == 'KAV':
                edited_user_id = user.id
        new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(20))
        # print(new_password)
        edited_user = await client.edit_user(
            org_id=env.int('ORGANISATION_ID'),
            user_id=edited_user_id,
            # params=Yandex360UserEditQueryParams(
            #     password=new_password,
            #     passwordChangeRequired=True
            # )
        )
        # print(edited_user)

    except Yandex360Exception as e:
        pass
    await client.close_session()


if __name__ == "__main__":
    asyncio.run(main())
