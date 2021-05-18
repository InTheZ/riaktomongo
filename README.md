# riaktomongo
RiakDB to MongoDB Example

## Environment Setup
This example is developed to work with MongoDB 4.4.x, Python 3.5.x and RiakDB KV 2.2.3 version.
```bash
pip install -r requirements.txt
```

## Configuration

### RiakDB Configuration
HTTP connection type on port 8098

### MongoDB Configuration
Please don't use this in a production environment! This should be executed by an admin (root) user over the entire database.
```
use example_api
db.createUser({"user": "example_api", "pwd": "example_api", roles: ["readWrite"]})
```