The following tables list the network ports that Anbox Cloud exposes.

For the regular Anbox Cloud deployment, these port are used for communication between components, and to allow accessing the Anbox Cloud interface. For the Anbox Cloud Appliance, all components are installed on the same machine. Therefore, there is no need to expose ports for internal communication.

<a name="anbox-cloud"></a>
## Anbox Cloud

| Service               | Port(s)     | Protocol  | Exposed externally | Required                     | Description                           |
|-----------------------|-------------|-----------|--------------------|------------------------------|---------------------------------------|
| AMS                   | 8444        | TCP       | no                 | yes                          | HTTPS API                             |
| AMS                   | 20002       | TCP       | no                 | no                           | HTTPS Prometheus endpoint             |
| AMS node controller   | 10000-11000 | UDP & TCP | yes                | no                           | Container service ports               |
| Anbox Cloud Dashboard | 5000        | TCP       | no                 | no                           | HTTPS website                         |
| Anbox Stream Agent    | 443         | TCP       | no                 | yes                          | HTTPS API                             |
| Anbox Stream Gateway  | 4000        | TCP       | no                 | yes                          | HTTPS API                             |
| Anbox Stream Gateway  | 7000        | TCP       | no                 | yes                          | Dqlite HA and API                     |
| Coturn                | 5349        | TCP       | yes                | yes                          | STUN/TURN                             |
| Coturn                | 5349        | UDP       | yes                | yes                          | STUN/TURN                             |
| Coturn                | 50000-51000 | UDP       | yes                | no (unless TURN is required) | TURN relay ports                      |
| etcd                  | 2379        | TCP       | no                 | yes                          | gRPC API                              |
| HAProxy               | 80          | TCP       | yes                | no                           | HTTP (redirects to HTTPS on port 443) |
| HAProxy               | 443         | TCP       | yes                | no                           | redirects to HTTPS website            |
| LXD                   | 8443        | TCP       | no                 | yes                          | HTTPS API                             |
| NATS                  | 4222        | TCP       | no                 | yes                          | NATS API                              |


<a name="appliance"></a>
## Anbox Cloud Appliance

| Service             | Port(s)     | Protocol  | Required | Description                            |
|---------------------|-------------|-----------|----------|----------------------------------------|
| AMS node controller | 10000-11000 | UDP & TCP | no       | Container service ports                |
| Coturn              | 5349        | UDP       | yes      | STUN/TURN                              |
| Coturn              | 60000-60100 | UDP       | yes      | TURN relay ports                       |
| Traefik             | 80          | TCP       | yes      | HTTP (redirects to HTTPS on port 443)  |
| Traefik             | 443         | TCP       | yes      | redirects to the Anbox Cloud dashboard |
