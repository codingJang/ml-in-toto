rm -rf Alice/mnist-prep/corrupt_data/
rm -rf Alice/mnist-prep/data/
rm -rf Alice/mnist-prep/images/
rm Alice/make-dataset.*.link
rm Alice/root.layout

rm -rf Bob/mnist-train/data/
rm -rf Bob/mnist-train/models/
rm Bob/train-model.*.link

rm -rf Carl/mnist-test/data/
rm -rf Carl/mnist-test/models/
rm -rf Carl/mnist-test/logs/
rm Carl/test-model.*.link

rm -rf Diana/mnist-dist/models/
rm -rf Diana/mnist-dist/logs/
rm -rf Diana/mnist-dist/build/
rm -rf Diana/mnist-dist/dist/
rm Diana/mnist-dist/app.spec
rm Diana/distribute.*.link

rm -rf EndUser/dist/
rm -rf EndUser/models/
rm -rf EndUser/data/
rm EndUser/root.layout
rm EndUser/alice.pub
rm EndUser/make-dataset.*.link
rm EndUser/train-model.*.link
rm EndUser/test-model.*.link
rm EndUser/distribute.*.link
rm EndUser/end-user.link

rm Alice/alice
rm Alice/alice.pub
rm Bob/bob
rm Bob/bob.pub
rm Carl/carl
rm Carl/carl.pub
rm Diana/diana
rm Diana/diana.pub

rm *.link-unfinished
