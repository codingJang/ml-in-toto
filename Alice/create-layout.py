from cryptography.hazmat.primitives.serialization import load_pem_private_key
from securesystemslib.signer import CryptoSigner
from in_toto.models.layout import Layout, Step, Inspection
from in_toto.models.metadata import Envelope, Metablock
# https://github.com/in-toto/in-toto/issues/663
from in_toto.models._signer import load_public_key_from_file

def main():
  # Load Alice's private key to later sign the layout
  with open("alice", "rb") as f:
    pvkey_alice = load_pem_private_key(f.read(), None)

  signer_alice = CryptoSigner(pvkey_alice)
  
  # Fetch and load Bob's, Carl's, Diana's, and Elenor's public keys
  key_alice = load_public_key_from_file("../Alice/alice.pub")
  key_bob = load_public_key_from_file("../Bob/bob.pub")
  key_carl = load_public_key_from_file("../Carl/carl.pub")
  key_diana = load_public_key_from_file("../Diana/diana.pub")

  print(key_bob)

  layout = Layout()
  for key in [key_alice, key_bob, key_carl, key_diana]:
    layout.add_functionary_key(key) ### ?
  layout.set_relative_expiration(months=4)

  make_dataset = Step(name="make-dataset")
  make_dataset.pubkeys = [key_alice['keyid']]
  make_dataset.set_expected_command_from_string("python mnist-prep/src/build_dataset.py")
  make_dataset.add_material_rule_from_string("REQUIRE mnist-prep/src/build_dataset.py")
  make_dataset.add_material_rule_from_string("REQUIRE mnist-prep/src/check_dataset.py")
  make_dataset.add_material_rule_from_string("DISALLOW *")
  make_dataset.add_product_rule_from_string("REQUIRE mnist-prep/src/build_dataset.py")
  make_dataset.add_product_rule_from_string("REQUIRE mnist-prep/src/check_dataset.py")
  for i in ['train', 't10k']:
    for j in ['images', 'labels']:
      k = 'idx3' if j == 'images' else 'idx1'
      make_dataset.add_product_rule_from_string(f"CREATE mnist-prep/data/MNIST/raw/{i}-{j}-{k}-ubyte")
      make_dataset.add_product_rule_from_string(f"CREATE mnist-prep/data/MNIST/raw/{i}-{j}-{k}-ubyte.gz")
      make_dataset.add_product_rule_from_string(f"CREATE mnist-prep/corrupt_data/MNIST/raw/{i}-{j}-{k}-ubyte")
      make_dataset.add_product_rule_from_string(f"CREATE mnist-prep/corrupt_data/MNIST/raw/{i}-{j}-{k}-ubyte.gz")
  make_dataset.add_product_rule_from_string(f"CREATE mnist-prep/images/random_mnist_samples.png")
  make_dataset.add_product_rule_from_string("DISALLOW *")

  train_model = Step(name="train-model")
  train_model.pubkeys = [key_bob['keyid']]
  train_model.set_expected_command_from_string("python mnist-train/src/train.py")
  train_model.add_material_rule_from_string("REQUIRE mnist-train/src/train.py")
  train_model.add_material_rule_from_string("REQUIRE mnist-train/src/net.py")
  train_model.add_material_rule_from_string("MATCH mnist-train/data/* WITH PRODUCTS FROM make-dataset")
  train_model.add_material_rule_from_string("DISALLOW *")
  train_model.add_product_rule_from_string("REQUIRE mnist-train/src/train.py")
  train_model.add_product_rule_from_string("REQUIRE mnist-train/src/net.py")
  train_model.add_product_rule_from_string("CREATE mnist-train/models/mnist_cnn.pt")
  train_model.add_product_rule_from_string("DISALLOW *")

  test_model = Step(name="test-model")
  test_model.pubkeys = [key_carl['keyid']]
  test_model.set_expected_command_from_string("python mnist-test/src/test.py")
  test_model.add_material_rule_from_string("REQUIRE mnist-test/src/test.py")
  test_model.add_material_rule_from_string("MATCH mnist-test/src/net.py WITH PRODUCTS FROM train-model")
  test_model.add_material_rule_from_string("MATCH mnist-test/data/* WITH PRODUCTS FROM make-dataset")
  test_model.add_material_rule_from_string("MATCH mnist-test/models/* WITH PRODUCTS FROM train-model")
  test_model.add_material_rule_from_string("DISALLOW *")
  test_model.add_product_rule_from_string("REQUIRE mnist-test/src/test.py")
  test_model.add_product_rule_from_string("REQUIRE mnist-test/src/net.py")
  test_model.add_product_rule_from_string("CREATE mnist-test/logs/test_result.json")
  test_model.add_product_rule_from_string("DISALLOW *")

  distribute = Step(name="distribute")
  distribute.pubkeys = [key_diana['keyid']]
  distribute.set_expected_command_from_string("python mnist-dist/src/dist.py")
  distribute.add_material_rule_from_string("REQUIRE mnist-dist/src/dist.py")
  distribute.add_material_rule_from_string("REQUIRE mnist-dist/src/app.py")
  distribute.add_material_rule_from_string("REQUIRE mnist-test/src/net.py")
  distribute.add_material_rule_from_string("REQUIRE mnist-dist/src/build_dist.sh")
  distribute.add_material_rule_from_string("MATCH mnist-dist/src/net.py WITH PRODUCTS FROM train-model")
  distribute.add_material_rule_from_string("MATCH mnist-dist/models/* WITH PRODUCTS FROM train-model")
  distribute.add_material_rule_from_string("MATCH mnist-dist/logs/* WITH PRODUCTS FROM test-model")
  distribute.add_material_rule_from_string("DISALLOW *")
  distribute.add_product_rule_from_string("REQUIRE mnist-dist/src/dist.py")
  distribute.add_product_rule_from_string("REQUIRE mnist-dist/src/app.py")
  distribute.add_product_rule_from_string("REQUIRE mnist-dist/src/net.py")
  distribute.add_product_rule_from_string("REQUIRE mnist-dist/src/build_dist.sh")
  distribute.add_product_rule_from_string("CREATE mnist-dist/build/*")
  distribute.add_product_rule_from_string("CREATE mnist-dist/dist/*")
  distribute.add_product_rule_from_string("DISALLOW *")

  inspection = Inspection(name="before execution")
#  inspection.add_material_rule_from_string("MATCH demo-project.tar.gz WITH PRODUCTS FROM package")
#  inspection.add_product_rule_from_string("MATCH demo-project/foo.py WITH PRODUCTS FROM update-version")


  # Add steps and inspections to layout
  layout.steps = [make_dataset, train_model, test_model, distribute]
  layout.inspect = [inspection]
    
  metadata = Envelope.from_signable(layout)

  # Sign and dump layout to "root.layout"
  metadata.create_signature(signer_alice)
  metadata.dump("root.layout")
  print('Created demo in-toto layout as "root.layout".')

if __name__ == '__main__':
  main()
