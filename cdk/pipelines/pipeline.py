from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.parameters import ParameterString
from sagemaker.workflow.pipeline_context import PipelineSession
from .preprocess import get_preprocessing_step
from .train import get_training_step

def create_pipeline(role):

    pipeline_session = PipelineSession()

    # Parameters for paths
    raw_data_uri = ParameterString(
        name="RawDataUri",
        default_value="s3://unemployment-ml-processed-data/unemployment_data.csv"
    )

    processed_data_uri = "s3://unemployment-ml-processed-data/processed/"
    model_output_uri = "s3://unemployment-ml-processed-data/model-artifacts/"

    # Preprocessing step
    preprocessing_step = get_preprocessing_step(
        role, pipeline_session, raw_data_uri, processed_data_uri
    )

    # Training step
    training_step = get_training_step(
        role, pipeline_session, processed_data_uri, model_output_uri
    )

    # Define Pipeline
    pipeline = Pipeline(
        name="UnemploymentMLPipeline",
        parameters=[raw_data_uri],
        steps=[preprocessing_step, training_step],
        sagemaker_session=pipeline_session
    )

    return pipeline

