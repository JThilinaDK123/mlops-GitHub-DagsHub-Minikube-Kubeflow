import kfp
from kfp import dsl

# @dsl.container_component
# def data_ingestion_step():
#     return dsl.ContainerSpec(
#         image='thilina9718/mlops-project-09-app:latest',
#         command=['python', 'src/data_ingestion.py'],
#     )


@dsl.container_component
def data_processing_step():
    return dsl.ContainerSpec(
        image='thilina9718/mlops-project-09-app:latest',
        command=['python', 'src/data_preprocessing.py'],
    )


@dsl.container_component
def model_training_step():
    return dsl.ContainerSpec(
        image='thilina9718/mlops-project-09-app:latest',
        command=['python', 'src/model_training.py'],
    )


## Define the pipeline
@dsl.pipeline(
    name='MLOps-Pipeline-Project-09',
    description='Kubeflow Pipeline - 09'
)
def mlops_pipeline():
    # data_ingestion = data_ingestion_step()
    # data_processing = data_processing_step().after(data_ingestion)
    data_processing = data_processing_step()
    model_training = model_training_step().after(data_processing)


## Compile the pipeline 
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        pipeline_func=mlops_pipeline,
        package_path='mlops-pipeline.yaml'
    )
