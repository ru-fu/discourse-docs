Anbox Cloud has support for managing GPUs and can provide them to individual containers for rendering and video encoding functionality.

If no GPU is available, Anbox Cloud automatically falls back to the [`null` platform](https://discourse.ubuntu.com/t/anbox-platforms/18733) that does not perform any rendering. However, you can enable software rendering and video encoding by launching your application with the `--enable-graphics` flag. This makes it possible to run entirely without a GPU and still use rendering.

<a name="supported-gpus"></a>
## Supported GPUs

Anbox Clouds allows access to GPUs from Intel, AMD and NVIDIA inside the Anbox container. Concrete support for the individual GPU depends on the platform being using for Anbox. The included `webrtc` platform currently supports the following GPUs:

| Vendor | Model                 | Render | Hardware video encode |
|--------|-----------------------|--------|-----------------------|
| AMD    | WX5100, WX4100        | Yes    | No                    |
| NVIDIA | Quadro, Tesla, Ampere | Yes    | Yes                   |

For GPUs on which Anbox Cloud doesn't support hardware video encoding, a software-based video encoding fallback is available.

## Enable support for GPUs in Anbox Cloud

Anbox Cloud automatically detects GPU devices during the deployment and configures the cluster to use them.

[note type="information" status="Important"]
You cannot mix GPUs from different vendors in a single deployment.
[/note]

## Required GPU slots

GPUs have limited capacity that can be shared amongst multiple containers. To fine-tune how many containers can run on a given node, configure the number of available GPU slots on the node.

See [GPU slots](https://discourse.ubuntu.com/t/about-capacity-planning/28717#gpu-slots) for detailed information.

## Using GPUs inside a container

AMS configures each LXD container to pass through a GPU device from the host. As of right now, all GPUs that are available to a machine are passed to every container that owns a GPU slot. For NVIDIA GPUs, LXD uses the [NVIDIA container runtime](https://github.com/NVIDIA/nvidia-container-runtime) to make the GPU driver of the host available to the container.

Check the [list of supported GPUs](#supported-gpus) to see if Anbox Cloud includes a driver for your GPU device. If a GPU driver is available inside the container, there are no further differences in how to use it in comparison to a regular environment. If no GPU driver is available, you must provide it through an [addon](https://discourse.ubuntu.com/t/managing-addons/17759).

If you want to let an application use the GPU (even if you are not interested in streaming the visual output), launch it with the `--enable-graphics` flag. With this flag, the command will launch the container using the `webrtc` platform, which will automatically detect the underlying GPU and make use of it.

    amc launch --enable-graphics my-application

## Force software rendering and video encoding

[note type="information" status="Note"]Software rendering and video encoding will utilise the CPU. This will mean you can run less containers on a system than you can when you have a GPU.[/note]

It is possible to tell a container to run with software rendering. For that, simply change the [instance type](https://discourse.ubuntu.com/t/instance-types/17764) or [resources](https://discourse.ubuntu.com/t/configure-available-resources/24960) of the application to not require a GPU. Anbox will then automatically determine that no GPU is available and use software rendering instead if a container is launched with graphics enabled.
