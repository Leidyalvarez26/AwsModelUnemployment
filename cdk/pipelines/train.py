from sagemaker.workflow.steps import TrainingStep
from sagemaker.estimator import Estimator
from sagemaker.workflow.functions import Join
import sagemaker


def get_training_step(role, pipeline_session, processed_data_uri, model_output_uri):
    estimator = Estimator(
        image_uri="683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.5-1",
        role=role,
        instance_count=1,
        instance_type="ml.m5.large",
        output_path=model_output_uri,
        sagemaker_session=pipeline_session,
        hyperparameters={
            "objective": "reg:linear",
            "num_round": "100",
            "max_depth": "5",
            "eta": "0.2",
            "subsample": "0.8",
            "min_child_weight": "3",
            "verbosity": "1"
        }
    )

    step = TrainingStep(
        name="UnemploymentMLTraining",
        estimator=estimator,
        inputs={
            "train": sagemaker.inputs.TrainingInput(
                s3_data=Join(on="/", values=[processed_data_uri, "processed", "processed_data.csv"]),
                content_type="text/csv"
            )
        }
    )
    return step
