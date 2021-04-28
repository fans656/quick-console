import importlib
import traceback

from logger import logger


def run_tmp_script():
    try:
        module = importlib.import_module('tmp_script')
        reload(module)
        module.main()
    except:
        logger.info(traceback.format_exc())
