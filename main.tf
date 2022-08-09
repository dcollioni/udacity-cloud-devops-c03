provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name  = "cloud-shell-storage-northeurope"
    storage_account_name = "csa100320020e4a6a1a"
    container_name       = "test"
    key                  = "sp=racwdli&st=2022-08-02T13:57:10Z&se=2022-08-02T21:57:10Z&spr=https&sv=2021-06-08&sr=c&sig=2CiJM8FuXeP04OliIlUs9E6LL3nMJegzhoklHDGiFV0%3D"
  }
}

module "resource_group" {
  source               = "./modules/resource_group"
  resource_group       = "${var.resource_group}"
  location             = "${var.location}"
}

module "network" {
  source               = "./modules/network"
  resource_group       = "${module.resource_group.resource_group_name}"
  location             = "${var.location}"
  address_space        = "${var.address_space}"
  virtual_network_name = "${var.virtual_network_name}"
  application_type     = "${var.application_type}"
  address_prefix_test  = "${var.address_prefix_test}"
  resource_type        = "NET"
}

# module "nsg-test" {
#   source              = "./modules/networksecuritygroup"
#   resource_group      = "${module.resource_group.resource_group_name}"
#   location            = "${var.location}"
#   application_type    = "${var.application_type}"
#   subnet_id           = "${module.network.subnet_id_test}"
#   address_prefix_test = "${var.address_prefix_test}"
#   resource_type       = "NSG"
# }

module "appservice" {
  source           = "./modules/appservice"
  resource_group   = "${module.resource_group.resource_group_name}"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "AppService"
}

module "publicip" {
  source           = "./modules/publicip"
  resource_group   = "${module.resource_group.resource_group_name}"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "publicip"
}

module "vm" {
  source               = "./modules/vm"
  resource_group       = "${module.resource_group.resource_group_name}"
  location             = "${var.location}"
  application_type     = "${var.application_type}"
  subnet_id            = "${module.network.subnet_id_test}"
  public_ip_address_id = "${module.publicip.public_ip_address_id}"
  resource_type        = "VM"
}
