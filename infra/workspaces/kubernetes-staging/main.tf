terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "lw-ru"

    workspaces {
      prefix = "kubernetes-"
    }
  }
}

resource "kubernetes_secret" "registry-staging" {
  metadata {
    name = "registry"
  }

  data = {
    ".dockerconfigjson" = base64decode(var.base64_dockerconfigjson)
  }

  type = "kubernetes.io/dockerconfigjson"
}

resource "kubernetes_secret" "mariadb-staging" {
  metadata {
    name = "mariadb"
  }

  data = {
    lw_user_password = var.mariadb_lw_app_password
  }

  type = "Opaque"
}

resource "kubernetes_secret" "django-staging" {
  metadata {
    name = "django"
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
