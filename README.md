# PII Scrubber Proof of Concept

## Overview 
Client database often hold PII (Personally Identifiable Information) such as SSN. When LLM are involved it's important to hide PII to protect the clients information. 

This proof of concept is meant to showcase a simple Python function that scrubs PII data out of a known mock database and outputs a sanitized version of the database while preserving relationships between tables. It is designed with a known mock database schema with predefined PII transformation rules.

The sanitized database can act as a security layer between the source database and the LLM. Instead of the LLM having direct access to the real database, it would instead have access to a sanitized version, while still being able to perform useful analysis and joins

The goal of this PoC is to demonstrate concepts such as pseudonymization, masking, generalization, removal of PII, and relationship preservation.

## Mock Database Schema

<img width="1023" height="638" alt="Screenshot 2026-11-04 112550" src="https://github.com/user-attachments/assets/944ca39d-6c0b-4c24-af8d-804e57117a22" />



## Techniques Used 

### PII Handling Per Field
<img width="1075" height="694" alt="Screenshot 2026-11-05 112734" src="https://github.com/user-attachments/assets/f5d65a34-2227-4e4e-a0c0-40e376cbaabf" />


### HMAC-Based Psuedonymization
HMAC-based pseudonymization is used on identifier fields such as client_id to protect the original identifiers while preserving relationships between tables.

HMAC is useful for this PoC because the original client ID does not need to be recovered. Given the same secret key and input, HMAC produces the same output, allowing the same client_id to remain consistent across the clients and policies tables.

#### Key Storage 
For the purpose of this simple PoC I stored the key as an environment variable since it best for local development. For production and highest security an enterprise key management system would be best. 

## Results 

### Converting source data to sanitized data 

<img width="1954" height="449" alt="Screenshot 2026-11-06 162357" src="https://github.com/user-attachments/assets/cb97be3a-3fd4-4073-a753-d1e9343ad1e0" />

### Testing Table Relationship with sanitized database 

<img width="780" height="439" alt="Screenshot 2026-11-06 162815" src="https://github.com/user-attachments/assets/119135ed-c9f2-418a-aeb4-80d1d08b1617" />

The results demonstrate that the same client_id consistently produces the same pseudonymized value. This allows relationships between the clients and policies tables to be preserved after sanitization.

Although the original client IDs were replaced, the sanitized tables can still be joined using the pseudonymized client_id. For example, the results show that client CUST_a521cd2d is associated with Life, Home, and Health policies. This demonstrates that the PII can be protected while retaining the relationships needed for analysis.

## Limitations
- The current implementation is designed specifically for the schema of the mock insurance database.
- PII fields and their transformations are predefined in the Python code.
- The tool does not automatically detect PII or determine how an unknown column should be sanitized.
- A database with a different schema would require the sanitization rules to be updated.
- This implementation is intended to demonstrate the PII-scrubbing concept and is not a production-ready security solution.