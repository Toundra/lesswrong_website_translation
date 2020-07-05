variable "mariadb_root_password" {
  type = string
}

variable "mariadb_lw_app_password" {
  type = string
}

variable "base64_dockerconfigjson" {
  type = string
}

variable "django_secret_key" {
  type = string
}
