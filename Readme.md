# BIG-IP Upgrades (ansible)

## Docker

  * git clone git@github.com:arunhotra/ansible-bigip-upgrades.git
  * modify inventory file according to your needs
  * docker-compose run upgrade-bigip
  * [from shell] ansible-playbook playbooks/upgrade_bigip.yml -vvv


## Non Docker 
## Prerequisites

  * Ansible 2.9
  * Latest ansible collection installed - https://galaxy.ansible.com/f5networks/f5_modules. Use the command "ansible-galaxy collection install f5networks.f5_modules -p ./collections" so that the collections can be installed locally. The ansible config file currently points to the collections which are local.
  * f5-sdk - pip3 install f5-sdk
  * objectpath module (for sync) - pip3 install objectpath
  * Inventory populated
  * Ansible controller with access to internal BIG-IP and reachable to F5 license server
  * Ensure that there is an UPGRADES directory inside the parent folder (same level as inventory, playbooks and roles)
  * Inside the Upgrades directory, there is a SCRIPTS directory with compare.py 
  * Create another direcory called ISO inside of UPGRADES and add the target BIG-IP image inside the ISO directory

## Usage

  * Populate the inventory file with the hosts, both A and B. An example is provided in the invnetory file
  * From the parent directory , run the command ansible-playbook playbooks/upgrade_bigip.yml
  * Verbosity levels can be used (-v,-vv,-vvv)
  * Each role uses a tag (except init which runs always), the tags feature can be leveraged if you only want to run a certain role for testing. For example, ansible-playbook playbooks/upgrade_bigip.yml --tags "pre-upgrade" -vvv


## Documentation

### General upgrade process

#### General guideline - work on standby first, compare with active. If things look good faiover and repeat process on active.

  * Upload the image with the version that you will be upgrading to 
  * Take backups ucs, qkview 
  * Disable traps 
  * Select inactive volume, delete it
  * Install software into deleted volume and  activate 
  * Once BIG-IP is booted into the new version, compare stats with the active device (log these stats as well)
  * Note - currently the pool status is being compared - modify accordingly based on your needs
  * If everthing looks good, failover and repeat the process on the other device


### Playbook - upgrade.yml

  * Roles run first and then after the success criteria is true.
  * The upgrade_success variable indicates that that particular upgrade (box A or B) was successful based on the comparison criteria (pool status comparison in this case)
  * Description of roles below

### Roles 

### init-hosts - initializing and populating some variables to be used later 

  * Initializes variables, initializes success variable seperately, populates hosts from the inventory, populates the active standby pairs. 
  
  * Note that all the tasks in the init-hosts always run
  
  * The standby_host variable controls

### pre-upgrade

  * Uploads image, takes qkview, ucs and re-licences
  
  * Pauses for 60 seconds after the volume is deleted

### upgrade  - 

  * prepare the volume - delete the nearest inacvive volume
  
  * If there is only one volume - it chooses "HD1.10" as a safe bet and installs the software on that volume

  * upgrade the guest - install software on the chosen volume and boot into that volume


### post upgrade 

  * compares the pool status and sets the upgrade_success variable accordingly.

  * It gets pool status output from active and standby and writes them to a file, then a python script compares the two files and writes a file called compare_status.json. If any of the guests fail to show successful comparison, then the upgrade success value is set to false.


### sync

  * Post upgrade sync - sync's from active to standby by using the bigip_configsync_action module. This is to get rid of the "changes pending" message after the upgrade.
