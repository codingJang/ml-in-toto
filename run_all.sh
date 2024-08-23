cd Alice
python create_layout.py

in-toto-record start --step-name make-dataset --use-dsse --signing-key alice --materials mnist-prep/src/*
cd mnist-prep/
python src/build_dataset.py
python src/check_dataset.py
cd ..
in-toto-record stop --step-name make-dataset --use-dsse --signing-key alice --products mnist-prep/src/* mnist-prep/data/* mnist-prep/corrupt_data/* mnist-prep/images/*
cp -r mnist-prep/data ../Bob/mnist-train/
cp -r mnist-prep/data ../Carl/mnist-test/

cd ../Bob/

in-toto-record start --step-name train-model --use-dsse --signing-key bob --materials mnist-train/src/* mnist-train/data/*
cd mnist-train/
python src/train.py --dry-run --save-model
cd ..
in-toto-record stop --step-name train-model --use-dsse --signing-key bob --products mnist-train/src/* mnist-train/models/* mnist-train/data/*
cp -r mnist-train/models ../Carl/mnist-test/
cp -r mnist-train/models ../Diana/mnist-dist/

cd ../Carl/

in-toto-record start --step-name test-model --use-dsse --signing-key carl --materials mnist-test/src/* mnist-test/data/* mnist-test/models/*
cd mnist-test/
python src/test.py --no-mps
cd ..
in-toto-record stop --step-name test-model --use-dsse --signing-key carl --products mnist-test/src/* mnist-test/logs/*
cp -r mnist-test/logs ../Diana/mnist-dist/

cd ../Diana/
in-toto-record start --step-name distribute --use-dsse --signing-key diana --materials mnist-dist/src/* mnist-dist/logs/* mnist-dist/models/*
cd mnist-dist/
python src/dist.py
cd ..
in-toto-record stop --step-name distribute --use-dsse --signing-key diana --products mnist-dist/src/* mnist-dist/logs/* mnist-dist/models/* mnist-dist/build/* mnist-dist/dist/*

cd ..
mkdir -p FinalProduct
cp Alice/root.layout Alice/alice.pub Alice/make-dataset.*.link Bob/train-model.*.link Carl/test-model.*.link Diana/distribute.*.link FinalProduct
cd FinalProduct
in-toto-verify -v --layout root.layout --verification-keys alice.pub
