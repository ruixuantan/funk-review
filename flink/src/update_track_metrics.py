import config as cfg
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment


def update_track_metrics():
    env = StreamExecutionEnvironment.get_execution_environment()

    t_env = StreamTableEnvironment.create(stream_execution_environment=env)

    job_config = t_env.get_config().get_configuration()
    job_config.set_string("pipeline.name", "update_track_metrics")
    job_config.set_string("pipeline.jars", ";".join(cfg.JARS))

    t_env.execute_sql(cfg.get_sql_query(cfg.ReviewConfig.__name__))
    t_env.execute_sql(cfg.get_sql_query(cfg.ViewConfig.__name__))
    t_env.execute_sql(cfg.get_sql_query(cfg.TrackMetricsPostgresConfig.__name__))

    stmt_set = t_env.create_statement_set()
    stmt_set.add_insert_sql(cfg.get_sql_query(cfg.UpdateTrackMetricsSQL.__name__))
    stmt_set.execute()


if __name__ == "__main__":
    update_track_metrics()
