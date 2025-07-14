!/bin/bash

REGION="us-east-1"
BUCKET="unemployment-ml-processed-data"
KEEP_TRAINING_JOB="pipelines-908jgu1dn7xz-UnemploymentMLTraini-eyv470hBI9"

echo "🧹 Cleaning up old model artifacts in S3..."

# List and delete old model artifacts, keeping the successful one
aws s3 ls s3://$BUCKET/model-artifacts/ --recursive --region $REGION | awk '{print $4}' | while read -r path; do
    if [[ $path != *"$KEEP_TRAINING_JOB"* ]]; then
        echo "🗑️ Deleting s3://$BUCKET/model-artifacts/$path"
        aws s3 rm s3://$BUCKET/model-artifacts/$path --region $REGION
    fi
done

echo "✅ Model artifacts cleanup done."

echo "🧹 Cleaning up old processed data CSVs..."

# aws s3 rm s3://$BUCKET/processed/ --recursive --region $REGION

echo "✅ Processed data cleanup done."

echo "🧹 Cleaning up old CloudWatch logs (TrainingJobs and Endpoints)..."

# List log groups containing 'TrainingJobs' or 'Endpoints' and delete them (safe if no longer needed)
aws logs describe-log-groups --region $REGION --query 'logGroups[].logGroupName' --output text | tr '\t' '\n' | grep "/aws/sagemaker/" | while read -r log_group; do
    echo "🗑️ Deleting log group: $log_group"
    aws logs delete-log-group --log-group-name "$log_group" --region $REGION
done

echo "✅ CloudWatch logs cleanup done."

echo "🎉 All cleanups complete. Working resources remain untouched."

