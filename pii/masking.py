import hashlib

def mask_pii_data(data):
    try:
        for record in data:
            # Check and mask 'device_id' if it exists
            if 'device_id' in record:
                record['masked_device_id'] = hashlib.sha256(record['device_id'].encode()).hexdigest()
                del record['device_id']  # Remove original field after masking
            else:
                record['masked_device_id'] = None  # Or handle however you deem appropriate

            # Check and mask 'ip' if it exists
            if 'ip' in record:
                record['masked_ip'] = hashlib.sha256(record['ip'].encode()).hexdigest()
                del record['ip']  # Remove original field after masking
            else:
                record['masked_ip'] = None  # Or handle however you deem appropriate

        return data

    except Exception as e:
        raise Exception(f"Error while masking PII data: {str(e)}") from e

