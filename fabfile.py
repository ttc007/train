from fabric.api import *

ENV = 'api' # Choices ['uat','production','development']
#ENV = 'production'
SERVERS = {
    'development': '192.168.1.31',
    # 'uat': '49.156.53.49',
    'production' : '49.156.53.49',
    'api' : '49.156.53.49'
}
BRANCH = {
    'development': 'develop',
    # 'uat': 'uat',
    'production': 'production',
    'api': 'production',
}

USERS = {
    'development': 'vooc',
    # 'uat': 'thangv',
    'production': 'thangv',
    'api': 'thangv'
}

PASSWORDS = {
    'development': 'vooc@min',
    # 'uat': 'ThangV@@123',
    'production': 'ThangV@@123',
    'api': 'ThangV@@123'
}

VIRTUAL_ENVS = {
    'development': 'source /home/vooc/envs_root/helio_web_env/bin/activate',
    # 'uat': 'source /home/thangv/envs/helio_web_env/bin/activate',
    'production': 'source /home/thangv/envs/helio_web_env/bin/activate',
    'api': 'source /home/thangv/envs/api_helio_web_env/bin/activate'
}

PATHS = {
    'development': '/home/vooc/projects/helio_web',
    # 'uat': '/home/thangv/projects/helio_web/',
    'production': '/home/thangv/projects/helio_web/',
    'api' : '/home/thangv/projects/api_source/helio_web'
}

PROCESS_ID = {
    'development': '/tmp/helio_web.pid',
    # 'uat': '/home/thangv/projects/helio_web/',
    'production': '/tmp/helio_web.pid',
    'api' : '/tmp/helio_api_web.pid'
}

env.hosts = [SERVERS[ENV]]
env.user = USERS[ENV]
env.password = PASSWORDS[ENV]
env.activate = VIRTUAL_ENVS[ENV]


PROJECT_PATH = PATHS[ENV]
DEBUG = True

VERBOSITY = ('', '') if DEBUG else ('-q', '-v 0')

def restart_app_server():
    """ Restarts remote nginx and uwsgi.4
    """
    sudo("uwsgi --reload /tmp/helio_web.pid")

def deploy():
    with cd(PROJECT_PATH):
        sudo('git checkout %s'%BRANCH[ENV])
        sudo('git fetch {0} origin {1}'.format('' , BRANCH[ENV]))
        sudo('git reset --hard origin/%s'%BRANCH[ENV])
        # run('git reset --hard origin/master')
        sudo('find . -name "*.pyc" -exec rm -rf {} \;')
        
        with cd('websites'):
            with prefix(env.activate):
                run('pip install -r ../requirements.txt')
                sudo('python manage.py collectstatic --noinput')
                sudo('su -s /bin/bash www-data -c "%s;%s" '%(env.activate,"uwsgi --reload %s"%PROCESS_ID[ENV]))

        

