// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.6.0;

import "https://github.com/smartcontractkit/chainlink/blob/develop/evm-contracts/src/v0.6/ChainlinkClient.sol";

contract Client is ChainlinkClient {
    bytes32 public last_uid;
    // chainlink vars for communicating with the RFID external adapter
    address private oracle;
    bytes32 private jobId;
    uint256 private fee;
    
    /**
     * CUSTOM RFID EXTERNAL ADAPTER PARAMS:
     * Network: Kovan
     * Oracle: Chainlink - 0x42149D794A135989319b66Dbcb770Ad36075a92e
     * Job ID: Chainlink - 785558e0bed6466b9567322cc2f4ca91
     * Fee: 1 LINK
     */
    constructor() public {
        setPublicChainlinkToken();
        oracle = 0x42149D794A135989319b66Dbcb770Ad36075a92e;
        jobId = "785558e0bed6466b9567322cc2f4ca91";
        fee = 1 * 10 ** 18; // 1 LINK
    }
    
    /**
     * Create a Chainlink request to retrieve API response from the RFID reader.
     * _tagUID is the ID of the RFID tag to get the latest scan for
     */
    function requestData() public returns (bytes32 requestId) {
        // creates the Request
        Chainlink.Request memory req = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        // Sends the request
        return sendChainlinkRequestTo(oracle, req, fee);
    }
    
    /**
     * Receive the response in the form of uint256
     */ 
    function fulfill(bytes32 _requestId, bytes32 uid) public recordChainlinkFulfillment(_requestId) {
        last_uid = uid;
    }
}