terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "lw-ru"

    workspaces {
      prefix = "kubernetes-"
    }
  }
}

locals {
  environment = "staging"
}

resource "kubernetes_namespace" "staging" {
  metadata {
    labels = {
      mylabel = local.environment
    }

    name = local.environment
  }
}

resource "kubernetes_secret" "registry-staging" {
  metadata {
    name = "registry"
    namespace = local.environment
  }

  data = {
    ".dockerconfigjson" = base64decode(var.base64_dockerconfigjson)
  }

  type = "kubernetes.io/dockerconfigjson"
}

resource "kubernetes_secret" "mariadb-staging" {
  metadata {
    name = "mariadb"
    namespace = local.environment
  }

  data = {
    lw_user_password = var.mariadb_lw_app_password
  }

  type = "Opaque"
}

resource "kubernetes_secret" "django-staging" {
  metadata {
    name = "django"
    namespace = local.environment
  }

  data = {
    secret_key = var.django_secret_key
  }

  type = "Opaque"
}

resource "helm_release" "mariadb_release" {
  name  = "mariadb-release"
  repository = "https://charts.bitnami.com/bitnami/"
  chart      = "mariadb"
  version    = "7.5.1"
  namespace = local.environment

  values = [
    "${file("./values/mariadb.yaml")}"
  ]

  set {
    name  = "rootUser.password"
    value = var.mariadb_root_password
  }

  set {
    name  = "db.password"
    value = var.mariadb_lw_app_password
  }
}

# resource "helm_release" "prometheus_release" {
#   name  = "prometheus-release"
#   repository = "https://kubernetes-charts.storage.googleapis.com"
#   chart      = "prometheus"
#   version    = "11.6.0"
#   namespace = "staging"

#   values = [
#     "${file("values/prometheus.yaml")}"
#   ]
# }
