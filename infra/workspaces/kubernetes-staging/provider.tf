variable "kubernetes_host" {}

variable "kubernetes_username" {}

variable "kubernetes_password" {}

variable "cluster_ca_certificate" {}

provider "kubernetes" {
  load_config_file = "false"

  host = var.kubernetes_host
  username = var.kubernetes_username
  password = var.kubernetes_password

  cluster_ca_certificate = var.cluster_ca_certificate
}


provider "helm" {
  kubernetes {
    load_config_file = "false"

    host = var.kubernetes_host

    username = var.kubernetes_username
    password = var.kubernetes_password

    cluster_ca_certificate = var.cluster_ca_certificate
  }
}
