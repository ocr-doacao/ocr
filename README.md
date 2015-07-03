Servidor para inserção e validação de imagens de cupons fiscais
========


Utilização
========

Para subir o servidor localmente, execute o comando "python manage.py runserver" dentro da raiz do projeto.

Para cadastrar uma ong no sistema, é preciso cadastrá-la manualmente no banco de dados.

Para enviar imagens para a ong, utilize o caminho '/ong/<nome_da_ong>/'

Para cadastrar as informações das notas, utilize o caminho '/ong/<nome_da_ong>/cadastro'

Instalação
========

Instale as dependências do projeto listadas em ocrDoacao/requirements.txt

Se o programa pip estiver instalado na sua máquina, execute "pip install -r ocrDoacao/requirements.txt"

Crie um banco 'ocr' e altere as variáveis 'USER' e 'PASSWORD' em ocrDoacao/settings.py para um usuário e senha do mysql.

Em seguida, execute os comandos 'python manage.py makemigrations' e 'python manage.py syncdb', respectivamente. 


