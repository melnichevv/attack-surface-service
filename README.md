# Attack surface service


This is service which users can query and get the attack surface of a VM - meaning which other virtual machines in the account can access and attack it.

Main technical stack:
- Python 3.8, Django 3, DRF
- PostgreSQL 11
- Docker
- Memcached
- pytest (for running tests)

### Description
The input for the service is a JSON document describing the cloud environment of a customer.
A cloud environment is described using 2 types of objects: VMs and firewall rules.
The structure of the cloud environment JSON is:
```
{
    “vms”: [ virtual machines ],
    “fw_rules”: [ firewall rules ]
}
```
#### Virtual Machine
A virtual machine has the following structure:
```
{
    "vm_id": "vm-xxxxxxx",
    "name": "jira server",
    "tags": ["tag1", ..]
}
```
`vm_id` - an identifier that uniquely identifies a virtual machines

`name` - a user-friendly display name

`tags` - a list of zero or more tag strings
#### Firewall Rule
By default, a virtual machine has no access from external sources.
If an administrator wants to make a virtual machine accessible to other machines, it defines a
firewall rule to allow traffic
Firewall rules have the following structure:
```
{
    "fw_id": "fw-xxxxx",
    "source_tag": "tag1",
    "dest_tag": "tag2"
}
```
`fw_id` - an identifier that uniquely identifies a firewall rule

`source_tag` - a string that represents the source tag of a traffic

`dest_tag` - a string that represents the destination tag of a traffic

In the example above, all traffic from virtual machines that have “tag1” is allowed to virtual
machines that have “tag2”.


Service that has two REST endpoints:
- `/attack` - which gets a vm_id as a query parameter and returns a JSON list of the virtual
machine ids that can potentially attack it
- `/stats` - which returns service statistics in a JSON format: number of virtual machines
in the cloud environment, number of requests to all endpoints & average request
processing time (in milliseconds). Statistics are reset on process startup.

#### Running prod env:
```
docker-compose -f docker-compose.prod.yml up --build
./scripts/reset_local_data.sh prod <path_to_data_input_file>
```
Then simply do a GET request to `http://localhost/api/v1/attack?vm-id=<any_vm_id_from_input_file>`

Stats info is accessible at `http://localhost/api/v1/stats`

#### Running tests
```
docker-compose down -v
docker-compose up -d --build django
docker-compose run --rm django pytest
```

##### TODO:
- Improve coverage
- Add Python type checking support
- Add code documentation
- Add support of recursive firewall rules for possible attacker calculations