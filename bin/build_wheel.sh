#!/bin/bash

# Activate OpenDR
source venv/bin/activate

# Clean existing packages
rm dist/*
rm src/*egg-info -rf

# Build OpenDR packages
while read p; do
  echo "Building wheel for $p"
  echo "exec(open('src/opendr/_setup.py').read())" > setup.py
  echo "build_package('$p')" >> setup.py
  python3 setup.py sdist
done < packages.txt

rm setup.py
rm MANIFEST.in

# Install the built packages
#pip install dist/opendr-toolkit-engine-1.0.tar.gz
#pip install dist/opendr-toolkit-face-recognition-1.0.tar.gz
#pip install dist/opendr-toolkit-pose-estimation-1.0.tar.gz
#pip install dist/opendr-toolkit-hyperparameter-tuner-1.0.tar.gz
#pip install dist/opendr-toolkit-semantic-segmentation-1.0.tar.gz
#pip install dist/opendr-toolkit-speech-recognition-1.0.tar.gz
#pip install dist/opendr-toolkit-compressive-learning-1.0.tar.gz
#pip install dist/opendr-toolkit-facial-expression-recognition-1.0.tar.gz
#pip install dist/opendr-toolkit-heart-anomaly-detection-1.0.tar.gz
#pip install dist/opendr-toolkit-human-model-generation-1.0.tar.gz
#pip install dist/opendr-toolkit-multimodal-human-centric-1.0.tar.gz
#pip install dist/opendr-toolkit-skeleton-based-action-recognition-1.0.tar.gz
#pip install dist/opendr-toolkit-activity-recognition-1.0.tar.gz
#pip install dist/opendr-toolkit-object-detection-2d-1.0.tar.gz


