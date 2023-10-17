class ErrorMessage:
    @staticmethod
    def unexpected_error(): return {'error': 'Unexpected error'}, 400

    @staticmethod
    def user_not_exist(): return {'error': 'User not exist'}, 400

    @staticmethod
    def entry_not_exist(entry): return {'error': '{} not exist'.format(entry)}, 400

    @staticmethod
    def user_exist(params): return {'error': 'User with username=<{}> exist'.format(params)}, 409

    @staticmethod
    def login_or_pass_error(): return {'error': 'Login or Password error'}, 409


class InfoMessage:

    @staticmethod
    def user_delete(): return {'message': 'User deleted'}, 200

    @staticmethod
    def entry_delete(entry): return {'message': '{} deleted'.format(entry)}, 200

    @staticmethod
    def user_update(): return {'message': 'User updated'}, 200

    @staticmethod
    def user_logout(): return {'message': 'User logout success'}, 200

    @staticmethod
    def no_data(): return {'message': 'No data to display'}, 200