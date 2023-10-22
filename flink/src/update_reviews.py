import config as cfg
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment


def update_reviews():
    env = StreamExecutionEnvironment.get_execution_environment()

    t_env = StreamTableEnvironment.create(stream_execution_environment=env)
    t_env.get_config().get_configuration().set_string(
        "pipeline.jars", ";".join(cfg.JARS)
    )
    t_env.execute_sql(cfg.get_sql_query(cfg.ReviewConfig.__name__))
    t_env.execute_sql(cfg.get_sql_query(cfg.TrackConfig.__name__))
    t_env.execute_sql(cfg.get_sql_query(cfg.TracksPostgresConfig.__name__))

    t_env.execute_sql(cfg.get_sql_query(cfg.UpdateReviewsSQL.__name__)).print()


if __name__ == "__main__":
    update_reviews()
