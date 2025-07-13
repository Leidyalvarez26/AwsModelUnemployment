from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.parameters import ParameterString
from sagemaker.workflow.pipeline_context import PipelineSession
from pipelines.preprocess_step_config import get_preprocessing_step
from pipelines.train import get_training_step

def create_pipeline(role_arn):
    # Initialize session
    pipeline_session = PipelineSession()
    
    # Define parameters
    raw_data_uri = ParameterString(
        name="RawDataUri",
        default_value="s3://unemployment-ml-processed-data/sagemaker_input_data.csv"
    )
    processed_data_uri = ParameterString(
        name="ProcessedDataUri",
        default_value="s3://unemployment-ml-processed-data"
    )
    model_output_uri = ParameterString(
        name="ModelOutputUri",
        default_value="s3://unemployment-ml-processed-data/model-artifacts"
    )
    
    # Steps
    preprocessing_step = get_preprocessing_step(
        role=role_arn,
        pipeline_session=pipeline_session,
        raw_data_uri=raw_data_uri,
        output_data_uri=processed_data_uri
    )
    
    training_step = get_training_step(
        role=role_arn,
        pipeline_session=pipeline_session,
        processed_data_uri=processed_data_uri,
        model_output_uri=model_output_uri
    )
    
    # Pipeline assembly
    pipeline = Pipeline(
        name="UnemploymentMLPipeline",
        steps=[preprocessing_step, training_step],
        parameters=[raw_data_uri, processed_data_uri, model_output_uri],
        sagemaker_session=pipeline_session
    )
    
    return pipeline
