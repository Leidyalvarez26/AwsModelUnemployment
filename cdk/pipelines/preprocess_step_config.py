from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.workflow.functions import Join

def get_preprocessing_step(role, pipeline_session, raw_data_uri, output_data_uri):
    # Create processor with explicit configuration
    processor = ScriptProcessor(
        image_uri="683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3",
        role=role,
        instance_count=1,
        instance_type="ml.t3.medium",
        command=["python3"],
        sagemaker_session=pipeline_session,
        volume_size_in_gb=30
    )

    # Create processing step with minimal configuration
    step = ProcessingStep(
        name="UnemploymentPreprocessing",
        processor=processor,
        inputs=[
            ProcessingInput(
                source=raw_data_uri,
                destination="/opt/ml/processing/input",
                input_name="raw-input"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="processed_data",
                source="/opt/ml/processing/output",
                destination=Join(on="/", values=[output_data_uri, "processed"]),
                s3_upload_mode="EndOfJob"
            )
        ],
        code="pipelines/preprocess.py",
        job_arguments=[
            "--input-path", "/opt/ml/processing/input/sagemaker_input_data.csv",
            "--output-path", "/opt/ml/processing/output/processed_data.csv"
        ]
    )
    return step