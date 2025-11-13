// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title GOATVaultAnchor
 * @dev Anchors Merkle roots of GOAT vault glyphs on-chain for immutable provenance
 */
contract GOATVaultAnchor {
    // Mapping of Merkle root => timestamp
    mapping(bytes32 => uint256) public anchors;
    
    // Event emitted when a new root is anchored
    event Anchored(bytes32 indexed root, uint256 timestamp, address indexed anchorer);
    
    /**
     * @dev Anchor a new Merkle root
     * @param root The Merkle root hash to anchor
     */
    function anchor(bytes32 root) external {
        require(anchors[root] == 0, "Root already anchored");
        
        anchors[root] = block.timestamp;
        
        emit Anchored(root, block.timestamp, msg.sender);
    }
    
    /**
     * @dev Check if a root has been anchored
     * @param root The Merkle root to check
     * @return bool True if the root is anchored
     */
    function isAnchored(bytes32 root) external view returns (bool) {
        return anchors[root] > 0;
    }
    
    /**
     * @dev Get the timestamp when a root was anchored
     * @param root The Merkle root to query
     * @return uint256 The timestamp (0 if not anchored)
     */
    function getAnchorTimestamp(bytes32 root) external view returns (uint256) {
        return anchors[root];
    }
    
    /**
     * @dev Batch anchor multiple roots (gas-efficient)
     * @param roots Array of Merkle roots to anchor
     */
    function anchorBatch(bytes32[] calldata roots) external {
        for (uint256 i = 0; i < roots.length; i++) {
            bytes32 root = roots[i];
            
            if (anchors[root] == 0) {
                anchors[root] = block.timestamp;
                emit Anchored(root, block.timestamp, msg.sender);
            }
        }
    }
}
