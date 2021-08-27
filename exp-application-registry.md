# About the application registry

The AMS service can be configured to regularly look at an application registry and import any new application versions found there. When a new application version is found AMS starts to import it and once done, makes it available for use. An imported application is immutable and cannot be changed other than through the registry itself. If an application is removed from the registry it is removed from AMS on the next update as well.

AMS can act in two different roles when working with the registry:

* `publisher`
* `client`

The `publisher` role allows both read and write access to the registry. AMS instances registered as clients act in `push` mode and are meant to push new applications and updates of these to the registry so that they can be consumed by regular read-only `clients`.

It is important to note that a single AMS instance can only act as a publisher or as a client, but not both. We recommend you have one publishing AMS instance per architecture, e.g. one for `amd64` and one for `arm64`. These should not be used to host regular containers but only to manage applications. Regular users should be directed to AMS instances acting in `client` mode.
