import os
from subprocess import check_call

from charmhelpers.core.templating import render
from charmhelpers.core.host import service, service_running, service_available
from charmhelpers.core.hookenv import open_port, config
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.hookenv import application_name
from charmhelpers.core.hookenv import log
from charms.reactive import when, when_not, set_flag, set_state, endpoint_from_flag, when_file_changed
from charms.reactive.flags import register_trigger
from charmhelpers.core.hookenv import application_version_set
from charms.layer import snap
from charmhelpers.core.host import service_start, service_stop

@when('snap.installed.flasksnap')
@when_not('flaskapp.port-8080-opened')
def set_available():
    port = 5001
    open_port(port)
    log(f"port {port} opened")
    set_flag('flaskapp.port-8080-opened') 
    status_set('active', 'snap installed')


@when('postgresql.connected')
@when_not('flaskapp.db_requested')
def request_db(pgsql):
    status_set('waiting', 'Requesting database ')
    pgsql.set_database('mydb')
    log(f"database is set!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")
    set_flag('flaskapp.db_requested')


@when('postgresql.master.available')
@when_not('flaskapp.db_configured')
def create_and_config_db():
    pgsql = endpoint_from_flag('postgresql.master.available')
    render(
        source='text-file.tmpl',
        target='/var/snap/flasksnap/common/config/text-file.txt',
        owner='root',
        perms=0o775,
        context={'db': pgsql.master}
    )
    set_flag('flaskapp.db_configured')
    db = pgsql.master
 #   URI_STRING = "postgresql://{}:{}@localhost{}/{}".format(str(db.user), str(db.password), str(db.name))
  #  check_call("snap set flasksnap snap.mode='{}'".format(URI_STRING).split())
  #  check_call("snap set flasksnap snap.mode='apples'".split())
    status_set('active', 'Ready: file rendered')

@when_file_changed('/var/snap/flasksnap/common/config/text-file.txt')
@when('flaskapp.db_configured')
@when_not('flasksnap.restarted')
def restart_snap():
    service_stop('snap.flasksnap.flasksnap')
    service_start('snap.flasksnap.flasksnap')
    set_flag('flasksnap.restarted')
    status_set('active', 'snap reset lets party')
