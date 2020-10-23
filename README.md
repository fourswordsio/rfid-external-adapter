# RFID External Adapter

Demo you can do right now! [Deploy this contract](https://remix.ethereum.org/#version=soljson-v0.6.0+commit.26b70077.js&optimize=false&evmVersion=null&gist=15eae06de1a102701ac6c8cb23eb48e5)

[![](http://img.youtube.com/vi/NdmyUhuQpgI/0.jpg)](http://www.youtube.com/watch?v=NdmyUhuQpgI "")


This external adapter will interface with a MiFare RC522 RFID scanner (or simulate the scanner when no hardware is connected).

The adapter is a simple flask server which will return the UID of an RFID card on a POST request.

**Contents**:

- `rfid_adapter.py`: main adapter class for the scanner. Parses POST requests and serializes responses. Uses either real or virtual hardware, depending on the `VIRTUAL` flag.
- `rfid.py`: software driver for the RFID scanner. Not needed for simulated scanner.
- `test.sh`: run the flask server and make an example POST request.
- `contract.sol`: ready to go solidity contract to run this external adapter on our chainlink node. Made for kovan testnet.
- `app.py`: flask server to recieve POST requests and route them to the adapter.
- `jobspecs.json`: jobspecs used to add this adapter to a chainlink node.


## Using simulated scanner

The easiest way to use the adapter is with the virtual hardware backend. This will simulate an RFID scanner and return a sample UID.

**USE THE ADAPTER NOW**: we're hosting the adapter on the Kovan testnet on [this](https://market.link/nodes/305e6143-288c-4acc-bf23-e9524549d3e8?start=1602645057&end=1603249857) chainlink node. Deploy `contract.sol` and fund with LINK to get started immediately.

**Host this adapter**: to host the simulated adapter on any chainlink node, the `app.py` flask server needs to be run and added as a bridge on the node. We won't include detailed instructions on this (see other guides for adding an external adapter to a node), but some tools that will come in handy:

- [localtunnel](https://localtunnel.github.io/www/): exposes a local port on a publicly accesible URL. Handy for testing.
- [Zappa](https://github.com/Miserlou/Zappa): tool for running a flask application on AWS lambda. Handy for production.

## Using real scanner

If you have a MiFare RC522 RFID scanner and want to run it on the blockchain.

**Disclaimer**: this is much more involved than running the simulated scanner. Experience with arduino programming and python is important. There could be bugs here, and this functionality is currently being developed. Post an issue if you run into anything and we'll be on it!

Steps:

1. Use [this](https://github.com/miguelbalboa/rfid) rfid library. Flash the `DumpInfo` example code onto the board. That's it for hardware!

2. Set the `VIRTUAL` flag in `rfid_adapter.py` to false.

3. Test hardware: run `test.sh`. This will start the flask server and send a POST request. If successful, a response with a UID should be returned.

	- The `get_hardware` method in `rfid.py` might have some problems. This is where the serial interface to the arduino board is established. We developed this to run on our computers, so some modification might be necessary.

	- Note: this script will leave the `app.py` process running in the background. Use `ps` and `kill` to get rid of it.

4. Deploy: we reccomend using [localtunnel](https://localtunnel.github.io/www/) to expose your flask server remotely. Other solutions are also possible, but we found this to be optimal since the flask server must be run locally (to interface with the hardware).


