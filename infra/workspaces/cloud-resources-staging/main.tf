terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "lw-ru"

    workspaces {
      prefix = "cloud-resources-"
    }
  }
}

locals {
  environment = "staging"
  name = "lw-infra-${local.environment}"
  k3s_version = "v1.18.3+k3s1"
  region = "fra1"
  size   = "s-1vcpu-1gb"
}

resource "digitalocean_ssh_key" "lw-infra" {
  name   = local.name
  public_key = file(".ssh/id_rsa.pub")
}


data "digitalocean_image" "default" {
  slug = "debian-9-x64"
}

resource "digitalocean_droplet" "lw-infra" {
  image  = data.digitalocean_image.default.id
  name   = local.name
  region = local.region
  size   = local.size
  ssh_keys   = [digitalocean_ssh_key.lw-infra.fingerprint]

  provisioner "remote-exec" {
    inline = [
      "apt-get -y update && apt-get -y install curl",
      "curl -sLS https://get.k3s.io | INSTALL_K3S_EXEC='server --tls-san ${self.ipv4_address} --no-deploy traefik' INSTALL_K3S_VERSION=${local.k3s_version} sh -"
    ]

    connection {
      type     = "ssh"
      user     = "root"
      host     = self.ipv4_address
      private_key = file(".ssh/id_rsa")
    }
  }

  depends_on = [
    digitalocean_ssh_key.lw-infra,
  ]
}

resource "digitalocean_firewall" "webserver" {
  name = local.name
  droplet_ids = [digitalocean_droplet.lw-infra.id]

  inbound_rule {
    protocol = "tcp"
    port_range = "22"
    source_addresses = ["0.0.0.0/0"]
  }

  inbound_rule {
    protocol = "tcp"
    port_range = "80"
    source_addresses = ["0.0.0.0/0"]
  }

  inbound_rule {
    protocol = "tcp"
    port_range = "442"
  }

  inbound_rule {
    protocol = "tcp"
    port_range = "6443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol = "tcp"
    port_range = "10250"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "icmp"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  // FIXME: images pulling doesn't without this rule
  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  depends_on = [
    digitalocean_droplet.lw-infra,
  ]
}

resource "digitalocean_project" "lw-infra" {
  name = local.name
  environment = local.environment
  resources = [digitalocean_droplet.lw-infra.urn]
  depends_on = [
    digitalocean_droplet.lw-infra,
  ]
}
