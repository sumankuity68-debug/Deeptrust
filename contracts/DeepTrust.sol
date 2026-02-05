// SPDX-License-Identifier: MIT
// Specifies the license type, MIT is open source and permissive.

pragma solidity ^0.8.0;
// Declares the Solidity compiler version. ^0.8.0 means any version from 0.8.0 up to (but not including) 0.9.0.

contract DeepTrust {
    // Defines the smart contract named "DeepTrust".
    
    // Struct to define the data structure for a single media record.
    struct MediaRecord {
        string mediaHash;           // The unique SHA-256 hash of the media file.
        uint256 authenticityScore;  // The AI-generated score (e.g., 0-100 percentage).
        uint256 timestamp;          // The block timestamp when the record was created.
        bool exists;                // A flag to check if the record has been initialized.
    }
    
    // Mapping to store MediaRecords, linked by their unique hash string.
    mapping(string => MediaRecord) public mediaRecords;
    
    // Event emitted when a new media is recorded, allowing off-chain apps to listen for updates.
    event MediaRecorded(string indexed mediaHash, uint256 score, uint256 timestamp);
    
    // Function to store a new media verification result on the blockchain.
    function recordMedia(string memory _mediaHash, uint256 _score) public {
        // specific check: ensure the media hasn't been recorded already to prevent overwrites.
        require(!mediaRecords[_mediaHash].exists, "Media already recorded.");
        
        // Create and store the new MediaRecord in the mapping.
        mediaRecords[_mediaHash] = MediaRecord({
            mediaHash: _mediaHash,
            authenticityScore: _score,
            timestamp: block.timestamp, // Use the current block's timestamp.
            exists: true                // Mark as existing.
        });
        
        // Emit the event to the blockchain log.
        emit MediaRecorded(_mediaHash, _score, block.timestamp);
    }
    
    // Function to retrieve the verification details of a media file by its hash.
    function verifyMedia(string memory _mediaHash) public view returns (bool, uint256, uint256) {
        // Check if the record exists; revert transaction if not found.
        require(mediaRecords[_mediaHash].exists, "Media not found.");
        
        // Retrieve the record from storage.
        MediaRecord memory record = mediaRecords[_mediaHash];
        
        // Return the existence flag, the score, and the timestamp.
        return (true, record.authenticityScore, record.timestamp);
    }
}
