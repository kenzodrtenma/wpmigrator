from database.connection import Connection

class User:
    def __init__(self):
        self.id = int(input('ID do usuário na origem:'))
        self.metadata = []
    
    def run(self):
        print('\n\nIniciando migração do usuário...\n\n')
        user = Connection().queryBy({'id': self.id}, 'users', 1)
        if not user:
            raise Exception('Usuário não existe na base de dados de origem.')
        
        (
            self.id,
            self.user_login, 
            self.user_pass, 
            self.user_nicename,
            self.user_email,
            self.user_url,
            self.user_registered,
            self.user_activation_key,
            self.user_status,
            self.display_name
        ) = user[0]

        user_exists = Connection('destiny').queryBy({
            'user_login': self.user_login,
            'user_email': self.user_email
        }, 'users', relation='OR')
        if user_exists:
            raise Exception('Usuário com os mesmos dados existe na base de dados de destino.')

        usermetas = Connection().queryBy({'user_id': self.id}, 'usermeta')

        for (umeta_id, user_id, meta_key, meta_value) in usermetas:
            self.metadata.append({
                'meta_key': meta_key,
                'meta_value': meta_value
            })
        
        destiny_user_id = Connection('destiny').insert('users', {
            'user_login': self.user_login,
            'user_pass': self.user_pass,
            'user_nicename': self.user_nicename,
            'user_email': self.user_email,
            'user_url': self.user_url,
            'user_registered': self.user_registered,
            'user_activation_key': self.user_activation_key,
            'user_status': self.user_status,
            'display_name': self.display_name
        })

        for meta in self.metadata:
            meta['user_id'] = destiny_user_id
            Connection('destiny').insert('usermeta', meta)