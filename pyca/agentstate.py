# -*- coding: utf-8 -*-
'''
    python-capture-agent
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: 2014-2017, Lars Kiesow <lkiesow@uos.de>
    :license: LGPL – see license.lgpl for more details.
'''

from pyca.utils import set_service_status, update_agent_state, timestamp
from pyca.config import config
from pyca.db import Service, ServiceStatus
import logging
import time


terminate = False


def control_loop():
    '''Main loop, updating the capture agent state.
    '''
    set_service_status(Service.AGENTSTATE, ServiceStatus.BUSY)
    while not terminate:
        update_agent_state()

        next_update = timestamp() + config()['agent']['update_frequency']
        while not terminate and timestamp() < next_update:
            time.sleep(0.1)

    logging.info('Shutting down agentstate service')
    set_service_status(Service.AGENTSTATE, ServiceStatus.STOPPED)


def run():
    '''Start the capture agent state process.
    '''
    control_loop()
