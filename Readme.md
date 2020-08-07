# BIG-IP Upgrades (ansible)

## Prerequisites

  * Ansible 2.9
  * Latest ansible collection installed - https://galaxy.ansible.com/f5networks/f5_modules
  * Inventory populated
  * Ansible controller with access to internal BIG-IP and reachable to F5 license server
  * Ensure that there is an UPGRADES directory inside the parent folder (same level as inventory, playbooks and roles)
  * Inside the Upgrades directory, there is a SCRIPTS directory with compare.py 
  * Create another direcory called ISO inside of UPGRADES and add the target BIG-IP image inside the ISO directory

## Usage

  * Populate the inventory file with the hosts, both A and B. An example is provided in the invnetory file
  * From the parent directory , run the command ansible-playbook playbooks/upgrade.yml
  * Verbosity levels can be used (-v,-vv,-vvv)
  * Each role uses a tag (except init which runs always), the tags feature can be leveraged if you only want to run a certain role for testing. For example, ansible-playbook playbooks/upgrade.yml --tags "pre-upgrade" -vvv


## Documentation

### Playbook - upgrade.yml

  * Roles run first and then after the success criteria is true. Following are the roles.

### Roles 

### init-hosts - initializing and populating some variables to be used later 

  * Initializes variables, initializes success variable seperately, populates hosts from the inventory, populates the guests from the hosts, populates the active standby guest pairs. It also assigns the standby host - in the first iteration based on the second host in the list. Then it also checks if the success criteria is working or not, and based on that it assigns the first host as standby host.

  * Note that all the tasks in the init-hosts always run

### pre-upgrade

  * Uploads image, takes qkview, ucs and re-licences

### upgrade  - 

  * prepare the volume

  * upgrade the guest


### post upgrade guests

  * compares the pool status and sets the upgrade_success variable accordingly.

  * It gets pool status output from active and standby and writes them to a file, then a python script compares the two files and writes a file called compare_status.json. If any of the guests fail to show successful comparison, then the upgrade success value is set to false.

