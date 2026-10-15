"""
Question 5: Session window with 5-minute gap on PULocationID,
using lpep_pickup_datetime as the event time.

Before running, create the PostgreSQL table:

    CREATE TABLE session_pickup_counts (
        session_start TIMESTAMP(3),
        session_end TIMESTAMP(3),
        PULocationID INT,
        num_trips BIGINT,
        PRIMARY KEY (session_start, PULocationID) NOT ENFORCED
    );

Submit with:

    docker exec -it workshop-jobmanager-1 \
        flink run -py /opt/src/job/session_job.py

Then query results:

    SELECT PULocationID, num_trips, session_start, session_end
    FROM session_pickup_counts
    ORDER BY num_trips DESC
    LIMIT 3;
"""

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def create_source(t_env):
    table_name = "green_trips_session"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            passenger_count INTEGER,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name


def create_sink(t_env):
    table_name = "session_pickup_counts"
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            session_start TIMESTAMP(3),
            session_end TIMESTAMP(3),
            PULocationID INT,
            num_trips BIGINT,
            PRIMARY KEY (session_start, PULocationID) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    source_table = create_source(t_env)
    sink_table = create_sink(t_env)

    t_env.execute_sql(f"""
        INSERT INTO {sink_table}
        SELECT
            window_start AS session_start,
            window_end AS session_end,
            PULocationID,
            COUNT(*) AS num_trips
        FROM TABLE(
            SESSION(TABLE {source_table} PARTITION BY PULocationID, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTE)
        )
        GROUP BY window_start, window_end, PULocationID;
    """).wait()


if __name__ == '__main__':
    main()
