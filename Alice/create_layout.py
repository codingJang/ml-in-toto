from cryptography.hazmat.primitives.serialization import load_pem_private_key
from securesystemslib.signer import CryptoSigner
from in_toto.models.layout import Layout
from in_toto.models.metadata import Envelope
# https://github.com/in-toto/in-toto/issues/663
from in_toto.models._signer import load_public_key_from_file

def main():
  # Load Alice's private key to later sign the layout
  with open("alice", "rb") as f:
    key_alice = load_pem_private_key(f.read(), None)

  signer_alice = CryptoSigner(key_alice)
  
  # Fetch and load Bob's, Carl's, Diana's, and Elenor's public keys
  key_bob = load_public_key_from_file("../Bob/bob.pub")
  key_carl = load_public_key_from_file("../Carl/carl.pub")
  key_diana = load_public_key_from_file("../Diana/diana.pub")
  key_elenor = load_public_key_from_file("../Elenor/elenor.pub")

  layout = Layout.read({
      "_type": "layout",
      "keys": {
          key_bob["keyid"]: key_bob,
          key_carl["keyid"]: key_carl,
          key_diana["keyid"]: key_diana,
          key_elenor["keyid"]: key_elenor,
      },
      "steps": [{
          "name": "clone",
          "expected_materials": [],
          "expected_products": [["CREATE", "mnist-project/net.py"], ["CREATE", "mnist-project/train.py"], ["DISALLOW", "*"]],
          "pubkeys": [key_bob["keyid"]],
          "expected_command": [
              "git",
              "clone",
              "https://github.com/codingJang/mnist-project.git"
          ],
          "threshold": 1,
        },{
          "name": "train",
          "expected_materials": [["MATCH", "mnist-project/*", "WITH", "PRODUCTS",
                                "FROM", "clone"], ["DISALLOW", "*"]],
          "expected_products": [["MODIFY", "demo-project/foo.py"], ["DISALLOW", "*"]],
          "pubkeys": [key_bob["keyid"]],
          "expected_command": [],
          "threshold": 1,
        },{
          "name": "update-version",
          "expected_materials": [["MATCH", "mnist-project/*", "WITH", "PRODUCTS",
                                "FROM", "clone"], ["DISALLOW", "*"]],
          "expected_products": [["MODIFY", "demo-project/foo.py"], ["DISALLOW", "*"]],
          "pubkeys": [key_bob["keyid"]],
          "expected_command": [],
          "threshold": 1,
        },{
          "name": "update-version",
          "expected_materials": [["MATCH", "mnist-project/*", "WITH", "PRODUCTS",
                                "FROM", "clone"], ["DISALLOW", "*"]],
          "expected_products": [["MODIFY", "demo-project/foo.py"], ["DISALLOW", "*"]],
          "pubkeys": [key_bob["keyid"]],
          "expected_command": [],
          "threshold": 1,
        },{
          "name": "test",
          "expected_materials": [
            ["MATCH", "demo-project/*", "WITH", "PRODUCTS", "FROM", "update-version"], 
            ["DISALLOW", "*"],
          ],
          "expected_products": [
              ["MODIFY", "demo-project/tests/test_foo.py"], ["DISALLOW", "*"],
          ],
          "pubkeys": [key_diana["keyid"]],
          "expected_command": [
              "pytest",
              "demo-project/tests",
          ],
          "threshold": 1,
        },{
          "name": "package",
          "expected_materials": [
            ["MATCH", "demo-project/*", "WITH", "PRODUCTS", "FROM",
             "test"], ["DISALLOW", "*"],
          ],
          "expected_products": [
              ["CREATE", "demo-project.tar.gz"], ["DISALLOW", "*"],
          ],
          "pubkeys": [key_carl["keyid"]],
          "expected_command": [
              "tar",
              "--exclude",
              ".git",
              "-zcvf",
              "demo-project.tar.gz",
              "demo-project",
          ],
          "threshold": 1,
        },{
          "name": "sign-package",
          "expected_materials": [
            ["MATCH", "demo-project.tar.gz", "WITH", "PRODUCTS", "FROM", "package"], 
            ["DISALLOW", "*"],
          ],
          "expected_products": [
              ["MODIFY", "demo-project.tar.gz.sig"], ["DISALLOW", "*"],
          ],
          "pubkeys": [key_elenor["keyid"]],
          "expected_command": [
              "gpg",
              "--output",
              "demo-project.tar.gz.sig",
              "--sign",
              "demo-project.tar.gz",
          ],
          "threshold": 1,
        }],
      "inspect": [{
          "name": "untar",
          "expected_materials": [
              ["MATCH", "demo-project.tar.gz", "WITH", "PRODUCTS", "FROM", "package"],
              ["ALLOW", ".keep"],
              ["ALLOW", "alice.pub"],
              ["ALLOW", "root.layout"],
              ["ALLOW", "*.link"],
              ["DISALLOW", "*"]
          ],
          "expected_products": [
              ["MATCH", "demo-project/foo.py", "WITH", "PRODUCTS", "FROM", "update-version"],
              ["ALLOW", "demo-project/.git/*"],
              ["ALLOW", "demo-project.tar.gz"],
              ["ALLOW", ".keep"],
              ["ALLOW", "alice.pub"],
              ["ALLOW", "root.layout"],
              ["ALLOW", "*.link"],
              ["DISALLOW", "*"]
          ],
          "run": [
              "tar",
              "xzf",
              "demo-project.tar.gz",
          ]
        }],
  })

  metadata = Envelope.from_signable(layout)

  # Sign and dump layout to "root.layout"
  metadata.create_signature(signer_alice)
  metadata.dump("root.layout")
  print('Created demo in-toto layout as "root.layout".')

if __name__ == '__main__':
  main()
