from sagemaker.workflow.steps import ProcessingStep
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
from sagemaker.workflow.parameters import ParameterString
from sagemaker.workflow.pipeline_context import PipelineSession

def get_preprocessing_step(role, pipeline_session, raw_data_uri, output_data_uri):

    processor = ScriptProcessor(
        image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3",
        role=role,
        instance_count=1,
        instance_type="ml.m5.large",
        command=["python3"],
        sagemaker_session=pipeline_session
    )

    step = ProcessingStep(
        name="UnemploymentPreprocessing",
        processor=processor,
        # --- FIX STARTS HERE ---
        inputs=[
            ProcessingInput(source=raw_data_uri, destination="/opt/ml/processing/input")
        ],
        outputs=[
            ProcessingOutput(source="/opt/ml/processing/output", destination=output_data_uri)
        ],
        # --- FIX ENDS HERE ---
        code="pipelines/preprocess.py"
    )

    return step