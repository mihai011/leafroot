"""Module for an empty python dags."""

import datetime
from datetime import timezone

from airflow import DAG
from airflow.models.baseoperator import chain, cross_downstream
from airflow.operators.empty import EmptyOperator

my_dag = DAG(
    dag_id="my_dag_name",
    start_date=datetime.datetime(2021, 1, 1, tzinfo=timezone.utc),
    schedule="@daily",
)
t1 = EmptyOperator(task_id="task1", dag=my_dag)
t2 = EmptyOperator(task_id="task2", dag=my_dag)
t3 = EmptyOperator(task_id="task3", dag=my_dag)
t4 = EmptyOperator(task_id="task4", dag=my_dag)
t5 = EmptyOperator(task_id="task5", dag=my_dag)
t6 = EmptyOperator(task_id="task6", dag=my_dag)
t7 = EmptyOperator(task_id="task7", dag=my_dag)
t8 = EmptyOperator(task_id="task8", dag=my_dag)
t9 = EmptyOperator(task_id="task9", dag=my_dag)
t10 = EmptyOperator(task_id="task10", dag=my_dag)


t1 >> t2
cross_downstream([t1, t2], [t3, t4])
chain(t5, [t6, t7], [t8, t9], t10)

my_dag.test()
