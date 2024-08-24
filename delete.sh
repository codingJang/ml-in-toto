rm -rf Alice/mnist-prep/corrupt_data/
# rm -rf Alice/mnist-prep/data/
rm -rf Alice/mnist-prep/images/
rm -rf Alice/make-dataset.*.link
rm -rf Alice/root.layout

rm -rf Bob/mnist-train/data/
rm -rf Bob/mnist-train/models/
rm -rf Bob/train-model.*.link

rm -rf Carl/mnist-test/data/
rm -rf Carl/mnist-test/models/
rm -rf Carl/mnist-test/logs/
rm -rf Carl/test-model.*.link

rm -rf Diana/mnist-dist/models/
rm -rf Diana/mnist-dist/logs/
rm -rf Diana/mnist-dist/build/
rm -rf Diana/mnist-dist/dist/
rm -rf Diana/mnist-dist/app.spec
rm -rf Diana/distribute.*.link

rm -rf FinalProduct
