import asyncio
import secrets
import string

from environs import Env

from aio_ya_360 import AioYa360Client, Ya360ClientSecrets, Ya360Organization, Ya360Department, \
    Ya360Group, Ya360User, Ya360UserCreationParams, Ya360UserRequestParams, Ya360User2fa, Ya360DepartmentParams, \
    Ya360UserName, Ya360GroupParams, Ya360ShortGroupMembers, Ya360GroupMember, Ya360GroupMemberGroupMemberType
from aio_ya_360.exceptions import Ya360Exception


#
# async def main():
#     env = Env()
#     env.read_env()
#     client = None
#     try:
#         client = AIOYa360Client(
#             client_secret=Yandex360ClientSecret.from_json(
#                 data={
#                     'client_id': env.str('CLIENT_ID'),
#                     'client_secret': env.str('CLIENT_SECRET')
#                 }
#             )
#         )
#         await client.start_work()
#
#         organizations = await client.get_organizations_list()
#         # for organization in organizations:
#         #     print(organization)
#
#         users = await client.get_users_list(org_id=env.int('ORGANISATION_ID'))
#         # for user in users:
#         #     print(user)
#
#         current_user = await client.get_current_user(
#             org_id=env.int('ORGANISATION_ID'),
#             user_id='1130000067921268'
#         )
#         # print(current_user)
#
#         groups = await client.get_groups_list(
#             org_id=env.int('ORGANISATION_ID'),
#         )
#         # for group in groups:
#         #     print(group.id, ':', group.name)
#
#         current_group = await client.get_current_group(
#             org_id=env.int('ORGANISATION_ID'),
#             group_id='19'
#         )
#         # print(current_group)
#
#         group_members = await client.get_group_members(
#             org_id=env.int('ORGANISATION_ID'),
#             group_id='19'
#         )
#         # for departments in group_members.departments:
#         #     print(departments)
#         # for groups in group_members.groups:
#         #     print(groups)
#         # for users in group_members.users:
#         #     print(users)
#
#         departments = await client.get_departments_list(
#             org_id=env.int('ORGANISATION_ID'),
#         )
#         # for department in departments:
#         #     print(department.id, ':', department.name)
#
#         current_department = await client.get_current_department(
#             org_id=env.int('ORGANISATION_ID'),
#             department_id='11'
#         )
#         # print(current_department)
#
#         edited_user_id = ''
#         for user in users:
#             if user.name.first == 'KAV' and user.name.last == 'KAV':
#                 edited_user_id = user.id
#         new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(20))
#         # print(new_password)
#         edited_user = await client.edit_user(
#             org_id=env.int('ORGANISATION_ID'),
#             user_id=edited_user_id,
#             # params=Yandex360UserEditQueryParams(
#             #     password=new_password,
#             #     passwordChangeRequired=True
#             # )
#         )
#         # print(edited_user)
#
#         sender_info = await client.get_user_main_email_and_signs(
#             org_id=env.int('ORGANISATION_ID'),
#             user_id=edited_user_id
#         )
#         print(sender_info)
#
#     except Yandex360Exception as e:
#         pass
#     await client.close_session()
#

async def main():
    env = Env()
    env.read_env()
    client = AioYa360Client(
        client_secrets=Ya360ClientSecrets.from_json(
            data={
                'client_id': env.str('CLIENT_ID'),
                'client_secret': env.str('CLIENT_SECRET')
            }
        )
    )
    try:
        organizations: list[Ya360Organization] = await Ya360Organization.from_api(client=client)

        org_id = None
        for organization in organizations:
            if organization.name == env.str('ORGANISATION_NAME'):
                org_id = organization.id

        # users: list[Ya360User] = await Ya360User.from_api(client=client, org_id=org_id)
        # for user in users:
        #     print(user)
        #
        # current_users: list[Ya360User] = (
        #     await Ya360User.from_api(
        #         client=client,
        #         org_id=org_id,
        #         user_ids=['1130000067921413']
        #     )
        # )
        # for current_user in current_users:
        #     print("Current user is", current_user)
        #
        # groups: list[Ya360Group] = await Ya360Group.from_api(client=client, org_id=org_id)
        # for group in groups:
        #     print(group)
        #
        # current_groups: list[Ya360Group] = (
        #     await Ya360Group.from_api(
        #         client=client,
        #         org_id=org_id,
        #         group_ids=['25']
        #     )
        # )
        # for current_group in current_groups:
        #     print("Current group", current_group)
        #
        # user_groups: list[Ya360Group] = await Ya360Group.member_of_groups(
        #     client=client, org_id=org_id,
        #     user_id='1130000067943192'
        # )
        # for group in user_groups:
        #     print("Group", group)
        #
        # departments: list[Ya360Department] = await Ya360Department.from_api(client=client, org_id=org_id)
        # for department in departments:
        #     print(department)
        #
        # current_departments: list[Ya360Department] = await Ya360Department.from_api(
        #     client=client,
        #     org_id=org_id,
        #     department_ids=['1']
        # )
        # for department in current_departments:
        #     print("Current department", department)
        #
        # new_password = ''.join(secrets.choice(Ya360UserCreationParams.allowed_password_symbols()) for i in range(20))
        #
        # edited_user: Ya360User = await Ya360User.edit_info(
        #     client=client,
        #     org_id=org_id,
        #     user_id='1130000067921413',
        #     params=Ya360UserRequestParams(
        #         password=new_password,
        #         passwordChangeRequired=True
        #     )
        # )
        # print("New password is", new_password)
        # print(edited_user)
        #
        # new_user: Ya360User = await Ya360User.add_user(
        #     client=client,
        #     org_id=org_id,
        #     params=Ya360UserCreationParams(
        #         departmentId=current_departments[0].id,
        #         name=Ya360UserName(
        #             first='Test',
        #             last='User',
        #             middle='Testovich'
        #         ),
        #         nickname='test_user',
        #         password=new_password,
        #         passwordChangeRequired=True
        #     )
        # )
        # print('New user is', new_user)
        # print("New password is", new_password)
        # current_user_2fa_status: Ya360User2fa = await Ya360User.user_2fa_status(
        #     client=client,
        #     org_id=org_id,
        #     user_id='1130000067921413'
        # )
        # print('Current user 2FA status is', current_user_2fa_status)
        #
        # print(
        #     await Ya360User.user_2fa_reset(
        #         client=client,
        #         org_id=org_id,
        #         user_id='1130000067921413')
        # )
        #
        # new_department: Ya360Department = await Ya360Department.create_department(
        #     client=client,
        #     org_id=org_id,
        #     params=Ya360DepartmentParams(
        #         name='Test Department',
        #         parentId='1',
        #         label='test_department'
        #     )
        # )
        # print('New department is: ', new_department)
        #
        # new_group: Ya360Group = await Ya360Group.create_group(
        #     client=client,
        #     org_id=org_id,
        #     params=Ya360GroupParams(
        #         name='Test',
        #         label='test'
        #     )
        # )
        # print('New group', new_group)
        #
        # add_user: bool = await Ya360Group.add_user_to_group(
        #     client=client,
        #     org_id=org_id,
        #     group_id=new_group.id,
        #     user=Ya360GroupMember(
        #         id=current_users[0].id,
        #         type=Ya360GroupMemberGroupMemberType.user
        #     )
        # )
        # print('Added user', add_user)
        #
        # delete_user: bool = await Ya360Group.delete_group_member(
        #     client=client,
        #     org_id=org_id,
        #     group_id=new_group.id,
        #     user=Ya360GroupMember(
        #         id=current_users[0].id,
        #         type=Ya360GroupMemberGroupMemberType.user
        #     )
        # )
        # print('Deleted user', delete_user)
        #
        # deleted_group = await Ya360Group.delete_group(
        #     client=client,
        #     org_id=org_id,
        #     group_id=new_group.id
        # )
        # print('Deleted group', deleted_group)

        # group_members: Ya360ShortGroupMembers = await Ya360Group.group_members(
        #     client=client,
        #     org_id=org_id,
        #     group_id='25'
        # )
        # print('Group members', group_members)

    except Ya360Exception:
        pass


if __name__ == "__main__":
    asyncio.run(main())
