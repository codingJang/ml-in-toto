#!/bin/bash

# Check if --corrupt is provided as an argument
CORRUPT=false
DRY_RUN=false
ARGS=()

for arg in "$@"
do
    if [ "$arg" == "--corrupt" ]; then
        CORRUPT=true
    elif [ "$arg" == "--dry-run" ]; then
        DRY_RUN=true
        ARGS+=("$arg")
    else
        ARGS+=("$arg")  # Collect arguments that are not --corrupt
    fi
done

# Set dataset paths based on whether --corrupt is present
if [ "$CORRUPT" = true ]; then
    ORIGINAL_ROOT="./data"
    CORRUPTED_ROOT="./data"
    CHECK_CORRUPTED="--is-corrupted"
else
    ORIGINAL_ROOT="./data"
    CORRUPTED_ROOT="./corrupt_data"
    CHECK_CORRUPTED=""
fi

if [ "$DRY_RUN" = true ]; then
    THRESHOLD=50.0
else
    THRESHOLD=95.0
fi

# Start executing the script
python rsa-keygen.py

cd Alice
python create_layout.py

in-toto-record start --step-name make-dataset --use-dsse --signing-key alice --materials mnist-prep/src/*
cd mnist-prep/
python src/build_dataset.py --original-root "$ORIGINAL_ROOT" --corrupted-root "$CORRUPTED_ROOT"
python src/check_dataset.py --root "$ORIGINAL_ROOT" $CHECK_CORRUPTED
cd ..
in-toto-record stop --step-name make-dataset --use-dsse --signing-key alice --products mnist-prep/src/* mnist-prep/data/* mnist-prep/corrupt_data/* mnist-prep/images/*
cp -r mnist-prep/data ../Bob/mnist-train/
cp -r mnist-prep/data ../Carl/mnist-test/

cd ../Bob/

in-toto-record start --step-name train-model --use-dsse --signing-key bob --materials mnist-train/src/* mnist-train/data/*
cd mnist-train/
python src/train.py "${ARGS[@]}" --save-model
cd ..
in-toto-record stop --step-name train-model --use-dsse --signing-key bob --products mnist-train/src/* mnist-train/models/* mnist-train/data/*
cp -r mnist-train/models ../Carl/mnist-test/
cp -r mnist-train/models ../Diana/mnist-dist/

cd ../Carl/

in-toto-record start --step-name test-model --use-dsse --signing-key carl --materials mnist-test/src/* mnist-test/data/* mnist-test/models/*
cd mnist-test/
python src/test.py --no-mps
cd ..
in-toto-record stop --step-name test-model --use-dsse --signing-key carl --products mnist-test/src/* mnist-test/data/* mnist-test/models/* mnist-test/logs/*
cp -r mnist-test/logs ../Diana/mnist-dist/

cd ../Diana/

in-toto-record start --step-name distribute --use-dsse --signing-key diana --materials mnist-dist/src/* mnist-dist/logs/* mnist-dist/models/*
cd mnist-dist/
python src/dist.py --threshold $THRESHOLD
cd ..
in-toto-record stop --step-name distribute --use-dsse --signing-key diana --products mnist-dist/src/* mnist-dist/logs/* mnist-dist/models/* mnist-dist/build/* mnist-dist/dist/*
cp -r mnist-dist/dist ../EndUser/
cp -r mnist-dist/models ../EndUser/
chmod +x mnist-dist/src/run_app.sh
cp -r mnist-dist/src/run_app.sh ../EndUser/
cp -r mnist-dist/src/download_mnist.sh ../EndUser/

cd ..
cp Alice/root.layout Alice/alice.pub Alice/make-dataset.*.link Bob/train-model.*.link Carl/test-model.*.link Diana/distribute.*.link EndUser/
cd EndUser/
dist/app/app

cd ..
