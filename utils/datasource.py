from utils import sys_utils
from sqlalchemy import create_engine

MYSQL_HOST = sys_utils.get_env('MYSQL_HOST', '192.168.1.60')
MYSQL_PORT = sys_utils.get_env('MYSQL_PORT', '3306')
CLICKHOUSE_HOST = sys_utils.get_env('CLICKHOUSE_HOST', '192.168.1.60')
CLICKHOUSE_PORT = sys_utils.get_env('CLICKHOUSE_PORT', '9000')
LOCAL_CLICKHOUSE_HOST = sys_utils.get_env('CLICKHOUSE_HOST', '192.168.1.57')
LOCAL_CLICKHOUSE_PORT = sys_utils.get_env('CLICKHOUSE_PORT', '9000')

class DbEngineFactory:
    cached_engine_ref = {}

    @staticmethod
    def url():
        return f'mysql+pymysql://root:Thanatos%40mysql_0102@{MYSQL_HOST}:{MYSQL_PORT}'

    @staticmethod
    def clickhouse_url():
        return f'clickhouse+native://default:Kitten_dongli_0102@{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}'

    @staticmethod
    def clickhouse_url_local():
        url = f'clickhouse+native://default:Kitten_dongli_0102@{LOCAL_CLICKHOUSE_HOST}:{LOCAL_CLICKHOUSE_PORT}'
        return url

    @staticmethod
    def engine_by_key(key):
        if key not in DbEngineFactory.cached_engine_ref:
            # build cached engine
            if key == 'mktdata_intraday':
                engine = create_engine(
                    DbEngineFactory.url() + '/mktdata_intraday',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'mktdata':
                engine = create_engine(
                    DbEngineFactory.url() + '/mktdata',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'TBF':
                engine = create_engine(
                    DbEngineFactory.url() + '/TBF',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'FW':
                engine = create_engine(
                    DbEngineFactory.url() + '/FW',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'rqdata':
                engine = create_engine(
                    DbEngineFactory.url() + '/rqdata_cbonds',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'rqdata_future':
                engine = create_engine(
                    DbEngineFactory.url() + '/rqdata_future',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'databus':
                engine = create_engine(
                    DbEngineFactory.url() + '/databus',
                    pool_recycle=3600,
                    pool_size=10,
                    max_overflow=20,
                    echo=False
                )
            elif key == 'strategy_tbf':
                engine = create_engine(
                    DbEngineFactory.url() + '/strategy_tbf',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'cal_inds':
                engine = create_engine(
                    DbEngineFactory.url() + '/cal_inds',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'clickhouse_rqdata':
                engine = create_engine(
                    DbEngineFactory.clickhouse_url() + '/rqdata_cbond',
                    pool_recycle=3600,
                    echo=False
                )

            elif key == 'clickhouse_strategy_tbf':
                engine = create_engine(
                    DbEngineFactory.clickhouse_url() + '/strategy_tbf',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'clickhouse_rqdata_future':
                engine = create_engine(
                    DbEngineFactory.clickhouse_url() + '/rqdata_future',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'rqdata_future_clickhouse':
                engine = create_engine(
                    DbEngineFactory.clickhouse_url() + '/rqdata_future',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'clickhouse_rqdata_future_local':
                engine = create_engine(
                    DbEngineFactory.clickhouse_url_local() + '/rqdata_future',
                    pool_recycle=3600,
                    echo=False
                )

            else:
                raise ValueError('不支持的数据库Engine')
            DbEngineFactory.cached_engine_ref[key] = engine
        return DbEngineFactory.cached_engine_ref[key]

    @staticmethod
    def engine_mktdata_intraday():
        return DbEngineFactory.engine_by_key('mktdata_intraday')

    @staticmethod
    def engine_mktdata():
        return DbEngineFactory.engine_by_key('mktdata')

    @staticmethod
    def engine_rqdata():
        return DbEngineFactory.engine_by_key('rqdata')

    @staticmethod
    def engine_databus():
        return DbEngineFactory.engine_by_key('databus')

    @staticmethod
    def engine_clickhouse_rqdata():
        return DbEngineFactory.engine_by_key('clickhouse_rqdata')

    @staticmethod
    def engine_clickhouse_rqdata_future():
        return DbEngineFactory.engine_by_key('clickhouse_rqdata_future')

    @staticmethod
    def engine_clickhouse_rqdata_future_local():
        return DbEngineFactory.engine_by_key('clickhouse_rqdata_future_local')

    @staticmethod
    def engine_clickhouse_strategy_tbf():
        return DbEngineFactory.engine_by_key('clickhouse_strategy_tbf')

    @staticmethod
    def engine_strategy_tbf():
        return DbEngineFactory.engine_by_key('strategy_tbf')

    @staticmethod
    def engine_rqdata_future():
        return DbEngineFactory.engine_by_key('rqdata_future')

    @staticmethod
    def engine_TBF():
        return DbEngineFactory.engine_by_key('TBF')

    @staticmethod
    def engine_cal_inds():
        return DbEngineFactory.engine_by_key('cal_inds')

    @staticmethod
    def engine_FW():
        return DbEngineFactory.engine_by_key('FW')
